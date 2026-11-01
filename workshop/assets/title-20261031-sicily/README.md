# 西西里岛轮廓版封面

2026-10-31按作者要求，将原来的任意地图外边缘改为真实地理轮廓，中英文地图构图保持一致，继续强调 EVERY TILE 和所有地块。

- [英文图](cover.en.png)、[中文图](cover.zh-CN.png)：1254×1254 PNG，使用内置 image_gen 编辑，保留未后处理的生成原图。
- 外轮廓以西西里岛主岛的真实海岸线为参考，北向上；内部划线仅表示模组的地块主题，不对应现实行政边界，也不声明与EU5具体地块逐条对应。
- 先修改英文图，再以完成的英文图为底稿仅改中文文字，锁定下部地图；已目视确认地图的位置、大小和分块布局一致。生成器仍可能改变边缘像素，不能声称两图地图逐像素相同；实际比较结果见 [provenance.json](provenance.json)。

## 地理来源与复现

海岸线来自 [Natural Earth 1:50m国家数据](https://github.com/nvkelso/natural-earth-vector/blob/ca96624a56bd078437bca8184e78163e5039ad19/geojson/ne_50m_admin_0_countries.geojson)，从意大利的MultiPolygon中提取西西里主岛，共90个坐标。Natural Earth数据为[公有领域](https://www.naturalearthdata.com/about/terms-of-use/)。地图为封面图形，不作为精确测绘成果。

提取数据保存在 [sicily.geojson](sicily.geojson)，坐标绘制的参考图为 [PNG](sicily-reference.png) 和 [SVG](sicily-reference.svg)。版本、原数据哈希及投影见 [map-source.json](map-source.json)，实际两次图像编辑的完整提示词见 [prompts.json](prompts.json)。

英文与中文封面均已检查文字准确性、标题强调、留白及地图轮廓。2026-10-31作者确认后已接入发布工程：英文导出为 [主封面](../cover.jpg) 和 [包内缩略图](../thumbnail.png)，中文导出为 [中文封面](../cover.zh-CN.jpg)，用于中文README及配套工坊素材。此前素材保留；本轮不修改词条，也不安装或上传。派生格式与哈希见上级 [provenance.json](../provenance.json)，素材的其他权利说明继承上级 [README](../README.md)。
