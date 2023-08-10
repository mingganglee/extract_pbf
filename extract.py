import os
import sys
import glob
from pathlib import Path


class Extract:

    @classmethod
    def run(cls, source_path: str):
        if not os.path.isdir("pbfs"):
            os.makedirs("pbfs")
        polys = glob.glob("polys/*")
        polys.sort()
        for i, poly in enumerate(polys):
            poly_name = Path(os.path.basename(poly)).stem
            print(f"总进度: {len(polys)}, 当前进度: {i+1}, 正在提取: {poly_name}")

            target_path = f"pbfs/{poly_name}.osm.pbf"
            if not os.path.exists(target_path):
                command = f"osmium extract --polygon polys/{poly_name}.poly --set-bounds {source_path} -o {target_path}"
                os.system(command)
            else:
                print(f"{poly_name} 已存在, 跳过本次提取")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        Extract.run(sys.argv[1])
    else:
        print("python3 extract.py xxx.osm.pbf, 未输入 osm.pbf 文件路径")
