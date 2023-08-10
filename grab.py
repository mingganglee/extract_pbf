import os
import requests
from lxml import etree


class GrabOsmToday:

    osm_today_url = "https://osmtoday.com"
    china_uri = "/asia/china.html"

    @ classmethod
    def write_file(cls, path, content):
        dir = os.path.dirname(path)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        with open(path, "w+") as f:
            f.write(content)

    @classmethod
    def generate_url(cls, uri: str) -> str:
        if not uri.startswith('/'):
            uri = f"/{uri}"

        return f"{cls.osm_today_url}{uri}"

    @classmethod
    def grab_polys(cls):
        url = cls.generate_url(cls.china_uri)
        response = requests.get(url)
        root = etree.HTML(response.content)
        polys = root.xpath(
            '/html/body/div[2]/div[2]/div[1]/table/tbody/tr/td[3]/a/@href')

        for i, poly in enumerate(polys):
            print(f"总进度: {len(polys)}, 当前进度: {i+1}")
            poly_url = cls.generate_url(poly)
            poly_text = requests.get(poly_url).content.decode()
            poly_save_path = f"polys/{os.path.basename(poly_url)}"
            cls.write_file(poly_save_path, poly_text)


if __name__ == "__main__":
    GrabOsmToday.grab_polys()
