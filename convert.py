import os
import glob
import time
import subprocess
from pathlib import Path


class Convert:

    @classmethod
    def run(cls):
        if not os.path.isdir("mbtiles"):
            os.makedirs("mbtiles")
        pbfs = glob.glob("pbfs/*")
        pbfs.sort()
        for i, poly in enumerate(pbfs):
            poly_name = Path(Path(os.path.basename(poly)).stem).stem

            source_path = f"pbfs/{poly_name}.osm.pbf"
            target_path = f"mbtiles/{poly_name}.mbtiles"
            print(
                f"总进度: {len(pbfs)}, 当前进度: {i+1}, 正在转换: {poly_name} - {source_path} -> {target_path}")
            if not os.path.exists(target_path):

                command = f"time docker run -v $(pwd)/coastline:/coastline -v $(pwd)/landcover:/landcover -v $(pwd):/data -i -t --rm tilemaker --input=/data/{source_path} --output=/data/{target_path}"
                # os.system(command)
                statr_time = time.time()
                subprocess.check_output(
                    command, shell=True, stderr=subprocess.STDOUT)
                elapsed_time = round(time.time() - statr_time, 3)
                print(f"处理: {target_path}, 耗时: {elapsed_time} 秒")
            else:
                print(f"{target_path} 已存在, 跳过本次转换")


if __name__ == "__main__":
    Convert.run()
