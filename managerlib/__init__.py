import os
import json
from . import file
from . import algo
from algo import info
from .argv import ArgvParser


# 数据管理器
class Manager:

    def __init__(self, global_config):
        # self.file_path = file_path  # 文件夹路径源文件夹路径
        """self._load_config(global_config)
        self.tag_manager = algo.info.tag.TagManager(self.tags)
        self._format_data()"""
        self._load_global_config(global_config)

    '''def __repr__(self):
        return f"Manager(file_path='{self.file_path}', tags='{self.tags}')"'''

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
        if not os.path.exists(os.path.join(self.data_folder)):
            # 不存在数据文件夹时
            os.makedirs(self.data_folder)
        json.dump(self.config, open(os.path.join(self.data_folder, "config.json"),  # 写入文件
                  "w", encoding=self.global_config["encoding"]), sort_keys=True, indent=4, ensure_ascii=False)

        return exc, info_folder, encoding, tag_file

    def _init_tag(self, tag_file) -> dict:
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

    def _load_global_config(self, global_config):
        self.global_config = json.load(  # 全局配置
            open(os.path.join(global_config, "config.json"), "r", encoding="utf-8"))
        self.argv_parser = ArgvParser(json.load(  # 命令行参数
            open(os.path.join(global_config, "prog_argv.json"), "r", encoding="utf-8")))

    def _load_config(self, file_path):
        """self.global_config = json.load(  # 全局配置
            open(os.path.join(global_config, "config.json"), "r", encoding="utf-8"))
        self.argv_parser = ArgvParser(json.load(  # 命令行参数
            open(os.path.join(global_config, "prog_argv.json"), "r", encoding="utf-8")))"""
        self.file_path = file_path  # 文件夹路径源文件夹路径
        self.data_folder = os.path.join(  # 数据文件夹路径
            self.file_path, self.global_config["data_folder"])
        # 局部配置
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

        self.info_folder = os.path.join(
            self.data_folder, info_folder)  # 文件信息文件夹

        self.encoding = encoding  # 编码
        # 获取标签
        if not os.path.exists(tag_path := os.path.join(self.data_folder, tag_file)):
            # 不存在标签文件时
            self.tags = algo.info.tag.format_tags(self._init_tag(tag_path))
        else:
            self.tags = algo.info.tag.format_tags(json.load(
                open(tag_path, "r", encoding=self.encoding)))
        self.info_parser = algo.info.InfoParser(self.tags, None)  # 信息管理器
        self._format_data()  # 格式化数据

    def _format_data(self):
        # 格式化数据
        json.dump(self.config, open(os.path.join(self.data_folder, "config.json",),  # 配置文件
                  "w", encoding="utf-8"), indent=4, ensure_ascii=False, sort_keys=True)
        json.dump(self.info_parser.get_tag_dict(), open(os.path.join(  # 标签文件
            self.data_folder, self.config["tags"]), "w", encoding=self.encoding), indent=4, ensure_ascii=False, sort_keys=True)

    def _creat_info_text(self, write_list) -> str:
        # 创建写入文本
        output = f":{write_list[0]}\n{write_list[1]}\n{write_list[2]}\n:"
        for n in range(3, 6):
            for i in write_list[n]:
                output += f"'{i}',"
            output += "\n"
        return output

    def _write_info(self, file_path: list[str], info_folder_path: str, encoding: str = "utf-8", input_data: dict | None = None) -> list:
        """
        write_list[
        file_size
        file_hash
        file_name
        file_tag
        file_path
        file_link]
        """
        file_site = file.set_file_site(  # 获取文件数据信息
            fp := os.path.join(*file_path))
        file_tag = self.info_parser.parse(fp)  # 获取文件标签

        # 创建文件夹
        p = os.path.join(info_folder_path, file_site[0][0]+file_site[0][-1])
        old_data = {"name": "",  # 文件名
                    "tag": [],  # 文件标签
                    "path": [],  # 文件路径
                    "link": []}  # 文件链接
        if input_data:
            # 有输入数据时
            old_data.update(input_data)

        i = os.path.join(p, file_site[0]+".0")
        if os.path.exists(p):
            n = 0
            while True:
                if not os.path.exists(i):
                    break
                info = json.load(
                    open(i := os.path.join(p, file_site[0]+f".{n}")))
                if file_site[1] == info["size"] and file_site[2] == info["hash"]:
                    # 读取旧数据
                    old_data = json.load(open(i, "r", encoding=encoding))
                    break
                n += 1
            # 检查文件
            for f in old_data["path"]:
                # if not file.check_file(fp := os.path.join(self.file_path, f), file_site[1:]):
                fs = file.set_file_site(f)
                info = json.load(open(i, "r", encoding=encoding))
                if fs[1] != info["size"] or fs[2] != info["hash"]:
                    old_data["path"].remove(f)
                    if not file.file_except(f, self.exc):
                        self._write_info(
                            [file_path[0], f], self.info_folder, self.encoding)
        else:
            os.makedirs(p)

        # 检查数据
        old_data["path"] = algo.merge_item_str(
            old_data["path"], [file_path[1]])
        """
        if "" in old_data["path"]:
            old_data["path"].remove("")"""

        # 写入数据文件
        with open(i, 'w', encoding=encoding) as f:
            write_dic = {"size": file_site[1],
                         "hash": file_site[2],
                         "name": old_data["name"],
                         "tag": sorted(algo.merge_item_str(
                             old_data["tag"], file_tag)),
                         "path": old_data["path"],
                         "link": old_data["link"]}
            json.dump(write_dic, f, indent=4,
                      ensure_ascii=False, sort_keys=True)
        return write_dic

    def write_info(self, file_path, input_data=None) -> list:
        # 写入文件信息
        if os.path.isdir(file_path):
            # 写入目录信息
            for f in file.list_files(file_path):
                if not file.file_except(f, self.exc):
                    self._write_info([file_path, f],
                                     self.info_folder, self.encoding, input_data)
        else:
            # 写入单个文件信息
            self._write_info(["", file_path],
                             self.info_folder, self.encoding, input_data)

    def get_info(self, file_path):
        # 获取文件信息
        return self._write_info(["", file_path], self.info_folder, self.encoding)

    def input_command(self, argv):
        argv = self.argv_parser(argv)
        print(argv)


def get_default(config, default_config, keys):
    # 获取配置
    values = []
    for key in keys:
        if key not in config:
            values.append(default_config[key])
        else:
            values.append(config[key])
    return values
