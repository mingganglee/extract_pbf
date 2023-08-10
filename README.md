# Extract data using .poly in .pbf

## Description

脚本功能说明

- `grab.py` 抓取中国省份的 `.poly` 文件
  - 运行后输出文件将保存到 `polys`
- `extract.py` 从 `.pbf` 文件中, 提取指定区域, 并保存到新的 `.pbf` 文件中
  - 运行后输出文件将保存到 `pbfs`
- `convert.py` 将 `.pbf` 文件, 转换为 `.mbtiles`
  - 运行后输出文件将保存到 `mbtiles`

下载文件 **(建议使用下载器下载)**

- 下载中国区的地图数据 - 993M [china-latest.osm.pbf](https://download.geofabrik.de/asia/china-latest.osm.pbf)
- 下载海洋信息数据 - 775M [water-polygons-split-4326.zip](https://osmdata.openstreetmap.de/download/water-polygons-split-4326.zip)
- 下载 `natural-earth-vector` 数据 - 1.5G [natural-earth-vector 5.1.2](https://github.com/nvkelso/natural-earth-vector/archive/refs/tags/v5.1.2.zip)

运行环境准备 **将下载文件移动到本项目中**

```bash
# 安装 tilemaker
git clone https://github.com/systemed/tilemaker.git
cd tilemaker
docker build -t tilemaker .
cd ..

# 水域数据处理
unzip water-polygons-split-4326.zip
mv water-polygons-split-4326 coastline

# natural earth vector 数据处理
unzip v5.1.2.zip
mkdir -p landcover/ne_10m_urban_areas
cp natural-earth-vector-5.1.2/10m_cultural/ne_10m_urban_areas.* landcover/ne_10m_urban_areas
mkdir -p landcover/ne_10m_antarctic_ice_shelves_polys
cp natural-earth-vector-5.1.2/10m_physical/ne_10m_antarctic_ice_shelves_polys.* landcover/ne_10m_antarctic_ice_shelves_polys
mkdir -p landcover/ne_10m_glaciated_areas
cp natural-earth-vector-5.1.2/10m_physical/ne_10m_glaciated_areas.* landcover/ne_10m_glaciated_areas
```

开始处理程序

```bash
# 抓取中国省份区域 .poly 文件
python3 grab.py

# 获取所有 .poly 文件, 从 china-latest.osm.pbf 文件中将对应省份数据抓取到新的 .osm.pbf 文件中
python3 extract.py china-latest.osm.pbf

# 获取所有 .osm.pbf 文件, 将文件转换为 .mbtiles
python3 convert.py
```

展示矢量瓦片数据

```bash
mkdir ~/tileserver && cd ~/tileserver
# 将项目中的 mbtiles 文件夹, 复制到 ~/tileserver 文件夹中

wget https://github.com/maptiler/tileserver-gl/releases/download/v1.3.0/test_data.zip
unzip test_data.zip
# 在此之前, 修改 config.json 文件中的 mbtiles 的值, 指定到要展示的 .mbtiles 文件
docker run --rm -it -v $(pwd):/data -p 8080:8080 maptiler/tileserver-gl

# 运行后再浏览器打开 localhost:8080 地址
```
