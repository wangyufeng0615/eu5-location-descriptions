"""Render precise vector badge layouts and transparent PNG exports."""
from pathlib import Path
import hashlib
import html
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SCALE = 4
HEIGHT, PADDING, GAP, RADIUS, FONT_SIZE = 40, 16, 12, 5, 20
FONT = Path('C:/Windows/Fonts/msyhbd.ttc')
font = ImageFont.truetype(str(FONT), FONT_SIZE * SCALE)
rows = {
    'en': [('coverage', '100%', '#238636'), ('languages', 'English + Chinese', '#1f6feb')],
    'zh-CN': [('覆盖率', '100%', '#238636'), ('支持语言', '英文 + 简中', '#1f6feb')],
}

def bounds(text):
    return font.getbbox(text, anchor='ls')

def width(text):
    box = bounds(text)
    return (box[2] - box[0] + SCALE - 1) // SCALE

# Corresponding segments share geometry across both languages.
widths = [[max(width(rows[lang][i][j]) for lang in rows) + 2 * PADDING
           for j in range(2)] for i in range(2)]
canvas_width = sum(sum(pair) for pair in widths) + GAP
metadata = {'renderer': 'SVG geometry and Pillow raster export', 'scale': SCALE,
            'height': HEIGHT, 'horizontal_padding_minimum': PADDING,
            'gap': GAP, 'radius': RADIUS, 'font': FONT.name, 'files': {}}

for lang, badges in rows.items():
    image = Image.new('RGBA', (canvas_width * SCALE, HEIGHT * SCALE))
    draw = ImageDraw.Draw(image)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{HEIGHT}" viewBox="0 0 {canvas_width} {HEIGHT}">']
    x = 0
    for index, (label, value, color) in enumerate(badges):
        left, right = widths[index]
        total = left + right
        mask = Image.new('L', image.size)
        ImageDraw.Draw(mask).rounded_rectangle((x*SCALE, 0, (x+total)*SCALE-1, HEIGHT*SCALE-1), RADIUS*SCALE, fill=255)
        fills = Image.new('RGBA', image.size)
        fill_draw = ImageDraw.Draw(fills)
        fill_draw.rectangle((x*SCALE, 0, (x+left)*SCALE-1, HEIGHT*SCALE-1), fill='#34383d')
        fill_draw.rectangle(((x+left)*SCALE, 0, (x+total)*SCALE-1, HEIGHT*SCALE-1), fill=color)
        image.paste(fills, (0, 0), mask)
        svg += [f'<defs><clipPath id="b{index}"><rect x="{x}" width="{total}" height="{HEIGHT}" rx="{RADIUS}"/></clipPath></defs>',
                f'<g clip-path="url(#b{index})"><path fill="#34383d" d="M{x} 0h{left}v{HEIGHT}H{x}z"/><path fill="{color}" d="M{x+left} 0h{right}v{HEIGHT}H{x+left}z"/></g>']
        for text, start, segment_width in [(label, x, left), (value, x+left, right)]:
            box = bounds(text)
            ink_width, ink_height = box[2]-box[0], box[3]-box[1]
            text_x = start*SCALE + (segment_width*SCALE-ink_width)/2-box[0]
            baseline = (HEIGHT*SCALE-ink_height)/2-box[1]
            draw.text((text_x, baseline), text, font=font, fill='white', anchor='ls')
            svg.append(f'<text x="{text_x/SCALE:.3f}" y="{baseline/SCALE:.3f}" font-family="Microsoft YaHei" font-weight="700" font-size="{FONT_SIZE}" fill="white">{html.escape(text)}</text>')
        x += total + GAP
    svg.append('</svg>')
    (ROOT/f'badges.{lang}.svg').write_text('\n'.join(svg)+'\n', encoding='utf-8')
    image.resize((canvas_width*2, HEIGHT*2), Image.Resampling.LANCZOS).save(ROOT/f'badges.{lang}.png')
    for extension in ['svg', 'png']:
        path = ROOT/f'badges.{lang}.{extension}'
        metadata['files'][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
(ROOT/'provenance.json').write_text(json.dumps(metadata, indent=2)+'\n', encoding='utf-8')
print(f'Rendered two language variants: {canvas_width} x {HEIGHT} logical pixels, 2x PNG.')
