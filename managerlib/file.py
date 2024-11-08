import os
import hashlib
import os
import bz2
from fnmatch import fnmatch


def get_file_name(file) -> str:
    # 获取文件名
    return os.path.splitext(os.path.basename(file))[0]


def file_except(file, exc) -> bool:
    # 判断文件是否在排除列表中
    for i in exc:
        if fnmatch(file, i):
            return True
    return False


def list_files(path):
    # 读取文件架中所有文件
    files = []
    for file in os.listdir(path):
        if os.path.isfile(p := os.path.join(path, file)):
            files.append(file)
        else:
            files.extend([os.path.join(file, f) for f in list_files(p)])
    return files


def get_file_sha3(file_path):
    # 获取文件sha256 hash值
    with open(file_path, 'rb') as f:
        return hashlib.sha3_256(f.read()).hexdigest()


def compress_file(file_path):
    # 压缩文件
    return bz2.compress(open(file_path, 'rb').read())


def set_file_site(file_path):
    # 设置文件信息路径
    output = []
    append = output.append
    # 获取文件hash, 大小
    file_hash = get_file_sha3(file_path)
    append(file_hash[:5]+file_hash[-5:])
    append(str(os.path.getsize(file_path)))
    append(hashlib.sha3_256(compress_file(file_path)).hexdigest())
    return output


def check_file(file_path, data, exc):
    # 检查文件
    if not os.path.exists(file_path):
        return False
    elif os.path.getsize(file_path) != int(data[0]):
        return False
    elif hashlib.sha3_256(compress_file(file_path)).hexdigest() != data[1]:
        return False
    elif file_except(file_path, exc):
        return False
    return True


def get_abs_path(path, folder_path):
    # 获取文件绝对路径
    return path if os.path.isabs(path) else os.path.join(folder_path, path)
