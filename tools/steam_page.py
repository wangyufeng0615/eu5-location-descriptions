"""Inspect/update this existing Workshop page through the running Steam client.

No credentials, visibility changes or new-item creation.
Content upload requires an explicit --content folder in addition to --assets.
Writes require explicit --assets, --descriptions, --host-badges or --clean-gallery.
Windows/game DLL required.
"""
import argparse
import ctypes as C
import json
import os
from pathlib import Path
import time
import hashlib
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
APP, ITEM = 3450310, 3830305546
P, U64, U32, I, B, S = C.c_void_p, C.c_uint64, C.c_uint32, C.c_int, C.c_bool, C.c_char_p

class QueryResult(C.Structure):
    _fields_ = [('handle', U64), ('result', I), ('returned', U32), ('total', U32), ('cached', B), ('cursor', C.c_char*256)]

class UpdateResult(C.Structure):
    _fields_ = [('result', I), ('agreement', B), ('item', U64)]

class ShareResult(C.Structure):
    _fields_ = [('result', I), ('file', U64), ('filename', C.c_char*260)]

class DetailsPrefix(C.Structure):
    _fields_ = [('item', U64), ('result', I), ('kind', I), ('creator_app', U32), ('consumer_app', U32),
                ('title', C.c_char*129), ('description', C.c_char*8000), ('owner', U64),
                ('created', U32), ('updated', U32), ('added', U32), ('visibility', I)]

class Steam:
    def __init__(self):
        os.environ['SteamAppId'] = str(APP)
        os.environ['SteamGameId'] = str(APP)
        self.dll = C.CDLL('C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis V/binaries/steam_api64.dll')
        if not self.bind('SteamAPI_Init', B)():
            raise RuntimeError('Steam API initialization failed')
        self.ugc = self.bind('SteamAPI_SteamUGC_v016', P)()
        self.utils = self.bind('SteamAPI_SteamUtils_v010', P)()
        user = self.bind('SteamAPI_SteamUser_v021', P)()
        self.owner = self.bind('SteamAPI_ISteamUser_GetSteamID', U64, P)(user)
        if not self.ugc or not self.utils or not self.owner:
            raise RuntimeError('Required Steam session is unavailable')

    def bind(self, name, result, *args):
        f = getattr(self.dll, name)
        f.restype, f.argtypes = result, list(args)
        return f

    def ug(self, name, result, args, *values):
        return self.bind('SteamAPI_ISteamUGC_'+name, result, P, *args)(self.ugc, *values)

    def wait(self, call, cls, callback):
        if not call:
            raise RuntimeError('Steam returned invalid API call')
        done = self.bind('SteamAPI_ISteamUtils_IsAPICallCompleted', B, P, U64, C.POINTER(B))
        end = time.monotonic()+180
        failed = B()
        while not done(self.utils, call, C.byref(failed)):
            if time.monotonic()>end:
                raise TimeoutError('Steam call timed out; inspect remote state before retrying')
            self.bind('SteamAPI_RunCallbacks', None)()
            time.sleep(.2)
        if failed.value:
            raise RuntimeError('Steam asynchronous call failed')
        result = cls()
        ok = self.bind('SteamAPI_ISteamUtils_GetAPICallResult', B, P, U64, P, I, I, C.POINTER(B))(
            self.utils, call, C.byref(result), C.sizeof(result), callback, C.byref(failed))
        if not ok or failed.value or result.result != 1:
            raise RuntimeError(f'Steam result failure: retrieved={ok}, result={result.result}')
        return result

    def query(self, language):
        ids = (U64*1)(ITEM)
        handle = self.ug('CreateQueryUGCDetailsRequest', U64, [C.POINTER(U64), U32], ids, 1)
        try:
            assert self.ug('SetLanguage', B, [U64, S], handle, language.encode())
            assert self.ug('SetAllowCachedResponse', B, [U64, U32], handle, 0)
            assert self.ug('SetReturnLongDescription', B, [U64, B], handle, True)
            assert self.ug('SetReturnAdditionalPreviews', B, [U64, B], handle, True)
            self.wait(self.ug('SendQueryUGCRequest', U64, [U64], handle), QueryResult, 3401)
            buffer = C.create_string_buffer(65536)
            assert self.ug('GetQueryUGCResult', B, [U64, U32, P], handle, 0, buffer)
            item = DetailsPrefix.from_buffer(buffer)
            if item.item != ITEM or item.consumer_app != APP or item.owner != self.owner or item.result != 1:
                raise RuntimeError('Item identity, game or signed-in owner does not match')
            count = self.ug('GetQueryUGCNumAdditionalPreviews', U32, [U64, U32], handle, 0)
            previews = []
            for index in range(count):
                url, filename, kind = C.create_string_buffer(4096), C.create_string_buffer(1024), I()
                assert self.ug('GetQueryUGCAdditionalPreview', B, [U64,U32,U32,P,U32,P,U32,C.POINTER(I)],
                               handle, 0, index, url, len(url), filename, len(filename), C.byref(kind))
                previews.append({'index':index,'url':url.value.decode(),'file':filename.value.decode(),'type':kind.value})
            cover = C.create_string_buffer(4096)
            assert self.ug('GetQueryUGCPreviewURL', B, [U64,U32,P,U32], handle, 0, cover, len(cover))
            return {'item':item.item,'owner_matches':True,'language':language,'title':item.title.decode(),
                    'description':item.description.decode(),'visibility':item.visibility,'updated':item.updated,
                    'cover':cover.value.decode(),'previews':previews}
        finally:
            self.ug('ReleaseQueryUGCRequest', B, [U64], handle)

    def submit(self, handle, note=None):
        result = self.wait(self.ug('SubmitItemUpdate', U64, [U64,S], handle, note.encode() if note else None), UpdateResult, 3404)
        if result.result != 1:
            raise RuntimeError(f'SubmitItemUpdate failed with Steam result {result.result}')
        if result.item != ITEM or result.agreement:
            raise RuntimeError('Update requires owner terms acceptance or item mismatch')
        return result.result

    def assets(self, before, content=None):
        handle = self.ug('StartItemUpdate', U64, [U32,U64], APP, ITEM)
        assert self.ug('SetItemPreview', B, [U64,S], handle, str(ROOT/'workshop/assets/cover.jpg').encode())
        if content:
            path = Path(content).resolve()
            if not (path/'.metadata/metadata.json').is_file():
                raise ValueError('Content must be the built mod folder')
            assert self.ug('SetItemContent', B, [U64,S], handle, str(path).encode())
        # Body-only badges must not be reintroduced into the screenshot gallery.
        paths = ['workshop/assets/cover.zh-CN.jpg']
        for relative in paths:
            path = ROOT/relative
            assert path.is_file() and path.stat().st_size < 1_000_000
            existing = [p for p in before['previews'] if Path(p['file']).name == path.name]
            if len(existing)>1:
                raise RuntimeError('Ambiguous duplicate preview name')
            if existing:
                assert self.ug('UpdateItemPreviewFile', B, [U64,U32,S], handle, existing[0]['index'], str(path).encode())
            else:
                assert self.ug('AddItemPreviewFile', B, [U64,S,I], handle, str(path).encode(), 0)
        self.submit(handle)

    def clean_gallery(self, before, descriptions):
        names = {'badges.en.png', 'badges.zh-CN.png'}
        targets = [p for p in before['previews'] if Path(p['file']).name in names]
        if any(p['url'] in description for p in targets for description in descriptions):
            raise RuntimeError('Move body images to independent hosting before removing gallery references')
        if any(p['type'] != 0 for p in targets):
            raise RuntimeError('Badge gallery entries must be images')
        if not targets:
            return
        handle = self.ug('StartItemUpdate', U64, [U32,U64], APP, ITEM)
        for preview in sorted(targets, key=lambda p:p['index'], reverse=True):
            if not self.ug('RemoveItemPreview', B, [U64,U32], handle, preview['index']):
                raise RuntimeError('Could not stage badge preview removal')
        self.submit(handle)

    def host_badges(self):
        storage = self.bind('SteamAPI_SteamRemoteStorage_v016', P)()
        if not storage:
            raise RuntimeError('Steam Remote Storage is unavailable')
        results = {}
        for language, suffix in [('english','en'), ('schinese','zh-CN')]:
            source = ROOT/f'workshop/assets/badges-20261031-vector/badges.{suffix}.png'
            content = source.read_bytes()
            sha256 = hashlib.sha256(content).hexdigest()
            filename = f'eu5_description_badges_{suffix}_{sha256[:16]}.png'.encode()
            exists = self.bind('SteamAPI_ISteamRemoteStorage_FileExists', B, P, S)(storage, filename)
            if exists:
                size = self.bind('SteamAPI_ISteamRemoteStorage_GetFileSize', I, P, S)(storage, filename)
                if size != len(content):
                    raise RuntimeError('Existing badge storage file has unexpected size')
                buffer = C.create_string_buffer(size)
                count = self.bind('SteamAPI_ISteamRemoteStorage_FileRead', I, P, S, P, I)(storage, filename, buffer, size)
                if count != size or buffer.raw != content:
                    raise RuntimeError('Existing badge storage file does not match')
            else:
                buffer = C.create_string_buffer(content)
                if not self.bind('SteamAPI_ISteamRemoteStorage_FileWrite', B, P, S, P, I)(storage, filename, buffer, len(content)):
                    raise RuntimeError('Could not store the badge image in Steam Cloud')
            call = self.bind('SteamAPI_ISteamRemoteStorage_FileShare', U64, P, S)(storage, filename)
            shared = self.wait(call, ShareResult, 1307)
            url = f'https://images.steamusercontent.com/ugc/{shared.file}/{hashlib.sha1(content).hexdigest().upper()}/'
            request = urllib.request.Request(url, headers={'Cache-Control':'no-cache'})
            with urllib.request.urlopen(request, timeout=25) as response:
                if response.status != 200 or response.read() != content:
                    raise RuntimeError('Shared badge CDN content did not match')
            results[language] = {'cloud_file':filename.decode(), 'ugc_handle':shared.file,
                                 'url':url, 'sha256':sha256, 'source':str(source.relative_to(ROOT))}
        return results

    def description(self, lang, text, title):
        handle = self.ug('StartItemUpdate', U64, [U32,U64], APP, ITEM)
        assert self.ug('SetItemUpdateLanguage', B, [U64,S], handle, lang.encode())
        assert self.ug('SetItemTitle', B, [U64,S], handle, title.encode())
        assert self.ug('SetItemDescription', B, [U64,S], handle, text.encode())
        self.submit(handle)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--assets', action='store_true')
    parser.add_argument('--descriptions', action='store_true')
    parser.add_argument('--clean-gallery', action='store_true', help='Remove only the two badge previews')
    parser.add_argument('--host-badges', action='store_true', help='Share only the two badge PNGs via Steam Cloud')
    parser.add_argument('--content', help='Optional built mod folder, only with --assets')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.content and not args.assets:
        parser.error('--content requires --assets')
    if args.clean_gallery and (args.assets or args.descriptions):
        parser.error('--clean-gallery must run separately so changes can be verified')
    if args.host_badges and (args.assets or args.descriptions or args.clean_gallery):
        parser.error('--host-badges must run separately')
    output = Path(args.output)
    if output.exists():
        raise FileExistsError('Choose a new record path')
    steam = Steam()
    try:
        before = {lang:steam.query(lang) for lang in ['english','schinese']}
        output.write_text(json.dumps({'before':before},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if args.assets:
            steam.assets(before['english'], args.content)
        if args.clean_gallery:
            steam.clean_gallery(before['english'], [p['description'] for p in before.values()])
        hosted = steam.host_badges() if args.host_badges else None
        if args.descriptions:
            titles = json.loads((ROOT/'workshop/page.json').read_text(encoding='utf-8'))['titles']
            for lang, file in [('english','description.en.txt'),('schinese','description.zh-CN.txt')]:
                steam.description(lang, (ROOT/'workshop'/file).read_text(encoding='utf-8'), titles[lang])
        after = {lang:steam.query(lang) for lang in ['english','schinese']}
        output.write_text(json.dumps({'before':before,'after':after,'hosted_badges':hosted},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        for lang in after:
            expected_title = titles[lang] if args.descriptions else before[lang]['title']
            if after[lang]['title'] != expected_title or after[lang]['visibility'] != before[lang]['visibility']:
                raise RuntimeError('Unexpected title or visibility change')
            if args.clean_gallery:
                expected = [p for p in before[lang]['previews'] if Path(p['file']).name not in {'badges.en.png','badges.zh-CN.png'}]
                canonical = lambda items:[(p['file'],p['url'],p['type']) for p in items]
                if canonical(after[lang]['previews']) != canonical(expected):
                    raise RuntimeError('Gallery readback differs from the intended badge-only removal')
                if after[lang]['description'] != before[lang]['description'] or after[lang]['cover'] != before[lang]['cover']:
                    raise RuntimeError('Unexpected description or primary cover change')
            if args.descriptions:
                filename = 'description.en.txt' if lang == 'english' else 'description.zh-CN.txt'
                expected = (ROOT/'workshop'/filename).read_text(encoding='utf-8').replace('\r\n','\n').strip()
                if after[lang]['description'].replace('\r\n','\n').strip() != expected:
                    raise RuntimeError('Uploaded description does not match local file')
        output.write_text(json.dumps({'before':before,'after':after,'hosted_badges':hosted},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if hosted:
            print(json.dumps(hosted,ensure_ascii=False,indent=2))
        print(json.dumps(after,ensure_ascii=False,indent=2))
    finally:
        steam.bind('SteamAPI_Shutdown', None)()

if __name__ == '__main__':
    main()
