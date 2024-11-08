import os
import json
from . import algo
from . import file


# 数据管理器
class Manager:

    def __init__(self, file_path, global_config_path):
        self.file_path = file.get_abs_path(file_path, os.getcwd())  # 源文件夹路径
        self.global_config = json.load(  # 全局配置
            open(global_config_path, "r", encoding="utf-8"))
        self.data_folder = os.path.join(  # 数据文件夹路径
            self.file_path, self.global_config["data_folder"])
        self._load_config()
        self.tag_manager = algo.tag.TagManager(self.tags)
        self._format_data()

    def __repr__(self):
        return f"Manager(file_path='{self.file_path}', tags='{self.tags}')"

    def _init_config(self):
        # 当配置文件不存在时
        exc, info_folder, encoding, tag_file = [self.global_config.get(
            k) for k in ["except", "info_folder", "encoding", "tag"]]
        self.config = {
            "except": exc,
            "info_folder": info_folder,
            "encoding": encoding,
            "tags": tag_file
        }
        json.dump(self.config, open(os.path.join(self.data_folder, "config.json"),  # 写入文件
                  "w", encoding=self.global_config["encoding"]), sort_keys=True, indent=4, ensure_ascii=False)

        return exc, info_folder, encoding, tag_file

    def _init_tag(self, tag_file):
        # 初始化标签
        tag = {
            "same": {},
            "tags": {},
            "trait": {},
            "type": {}
        }
        json.dump(tag, open((tag_file), "w", encoding=self.encoding),  # 标签
                  indent=4, ensure_ascii=False, sort_keys=True)
        return tag

    def _load_config(self):
        if not os.path.exists(os.path.join(self.data_folder, "config.json")):
            # 不存在时
            exc, info_folder, encoding, tag_file = self._init_config()
        else:
            # 读取配置文件
            self.config = json.load(
                open(os.path.join(self.data_folder, "config.json"), "r", encoding=self.global_config["encoding"]))
            exc, info_folder, encoding, tag_file = get_default(
                self.config, self.global_config, ["except", "info_folder", "encoding", "tag"])

        self.exc = exc  # 排除对象

        self.info_folder = file.get_abs_path(
            info_folder, self.data_folder)  # 文件信息文件夹

        self.encoding = encoding  # 编码
        # 获取标签
        if not os.path.exists(tag_path := file.get_abs_path(tag_file, self.data_folder)):
            # 不存在时
            self.tags = algo.tag.format_tags(self._init_tag(tag_path))
        else:
            self.tags = algo.tag.format_tags(json.load(
                open(tag_path, "r", encoding=self.encoding)))

    def _format_data(self):
        # 格式化数据
        json.dump(self.config, open(os.path.join(self.data_folder, "config.json",),
                  "w", encoding="utf-8"), indent=4, ensure_ascii=False, sort_keys=True)
        json.dump(self.tag_manager.get_tag_dict(), open(file.get_abs_path(
            self.config["tags"], self.data_folder), "w", encoding=self.encoding), indent=4, ensure_ascii=False, sort_keys=True)

    def _creat_info_text(self, write_list):
        # 创建写入文本
        output = f":{write_list[0]}\n:{write_list[1]}\n:{write_list[2]}\n:"
        for i in write_list[3]:
            output += f"'{i}',"
        output += "\n:"
        for i in write_list[4]:
            output += f"'{i}',"
        return output

    def _read_info(self, file_folder, encoding="utf-8"):
        for f in os.listdir(folder := file.get_abs_path(file_folder, self.info_folder)):
            yield open(os.path.join(folder, f), 'r', encoding=encoding).read()[1:].replace("\n", "").split(":")

    def _write_info(self, file_path, info_foloder_path, encoding="utf-8"):
        """
        :file_size
        :file_hash
        :file_name
        :file_tag
        :file_path
        """
        file_site = file.set_file_site(fp := os.path.join(*file_path))
        file_tag = self.tag_manager.tag_matcher.match(fp)
        # 创建文件夹
        p = os.path.join(info_foloder_path, file_site[0])
        old_data = ["", "", ""]
        i = "0"
        if os.path.exists(p):
            # 查找相同文件
            """for i in os.listdir(p):
                fw = open(os.path.join(p, i), 'r+',
                          encoding=encoding).read()[1:].replace("\n", "").split(":")
                if fw[:2] == file_site[1:3]:
                    old_data = fw[2:5]"""
            n = 0
            for k in self._read_info(p, encoding):
                if k[:2] == file_site[1:3]:
                    old_data = k[2:5]
                    i = str(n)
                    break
                n += 1
            else:
                i = str(n)
        else:
            os.makedirs(p)

        # 检查数据
        old_data[2] = sorted(algo.merge_item_str([i[1:-1]
                             for i in old_data[2].split(",")], [file_path[1]]))
        if "" in old_data[2]:
            old_data[2].remove("")

        for f in old_data[2]:
            if not file.check_file(fp := os.path.join(self.file_path, f), file_site[1:], self.exc):
                old_data[2].remove(f)
                if not file.file_except(f, self.exc):
                    self._write_info([self.file_path, f],
                                     self.info_folder, self.encoding)

        # 写入数据文件
        with open(os.path.join(p, i), 'w', encoding=encoding) as f:
            write_list = [file_site[1],
                          file_site[2],
                          old_data[0],
                          sorted(algo.merge_item_str(
                              [i[1:-1] for i in old_data[1].split(",")], file_tag)),
                          old_data[2]]
            f.write(self._creat_info_text(write_list))
        return write_list

    def write_info(self):
        # 写入信息文件夹
        for f in file.list_files(self.file_path):
            if not file.file_except(f, self.exc):
                self._write_info([self.file_path, f],
                                 self.info_folder, self.encoding)

    def get_info(self, file_path):
        # 获取文件信息
        file_site = file.set_file_site(file_path)
        for f in self._read_info(os.path.join(self.info_folder, file_site[0])):
            if f[:2] == file_site[1:3]:
                return f[2:5]


def get_default(config, default_config, keys):
    # 获取配置
    values = []
    for key in keys:
        if key not in config:
            values.append(default_config[key])
        else:
            values.append(config[key])
    return values
