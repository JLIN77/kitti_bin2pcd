import argparse
import numpy as np
from tqdm import tqdm
from pathlib import Path
from pclpy import pcl


def bin2pcd(bin_folder: Path, pcd_folder: Path) -> None:
    '''将 bin_folder 文件夹中的 .bin 文件转为
       .pcd 文件并输出到 pcd_folder 文件夹中
    '''
    # 获取所有的 .bin 文件
    bin_files = list(bin_folder.glob("*.bin"))
    print("开始转换：")
    for bin_file in tqdm(bin_files):
        # 读取 .bin 文件，这里每个点是 (x, y, z, intensity) 共4个字段
        # 根据自己的数据改变 reshape() 的参数
        points = np.fromfile(bin_file, dtype="float32").reshape((-1, 4))
        print(points)
        print(points.shape)
        # 载入所有点
        pcd = pcl.PointCloud.PointXYZI().from_array(points)
        # 输出文件的文件名
        pcd_file = Path(pcd_folder, bin_file.name).with_suffix(".pcd")
        # 保存 .pcd 文件
        pcl.io.savePCDFileBinary(str(pcd_file), pcd)


def main():
    # 创建一个参数解析器
    parse = argparse.ArgumentParser()
    parse.add_argument('--bin', type=str, default="bin", help='input bin file path.')
    parse.add_argument('--pcd', type=str, default="pcd", help='output pcd file path, will be created if not exists.')
    args = parse.parse_args()

    # 判断文件夹是否存在
    bin_folder = Path(args.bin)
    if not bin_folder.exists():
        print(f"文件夹 {bin_folder.absolute()} 不存在，请确认后重试！")
        return
    pcd_folder = Path(args.pcd)
    if not pcd_folder.exists():
        pcd_folder.mkdir(parents=True, exist_ok=True)

    bin2pcd(bin_folder, pcd_folder)


if __name__ == '__main__':
    main()
