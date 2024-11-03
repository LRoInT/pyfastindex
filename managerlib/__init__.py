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
        self.folder_path = os.path.join(  # 数据文件夹路径
            self.file_path, self.global_config["data_folder"])
        self.load_data()
        self.tag_manager = algo.tag.TagManager(self.tags)
        self._format_data()

    def __repr__(self):
        return f"Manager(file_path='{self.file_path}', tags='{self.tags}')"

    def load_data(self):
        # 配置文件
        self.config = json.load(
            open(os.path.join(self.folder_path, "config.json"), "r", encoding=self.global_config["encoding"]))
        exc, info_folder, encoding, tag_file = get_config(
            self.config, self.global_config, ["except", "info_folder", "encoding", "tag"])
        # 排除对象
        self.exc = exc
        # 文件信息文件夹
        self.info_folder = file.get_abs_path(info_folder, self.folder_path)
        # 编码
        self.encoding = encoding
        # 标签
        self.tags = algo.tag.format_tags(json.load(open(file.get_abs_path(
            tag_file, self.folder_path), "r", encoding=self.encoding) if "tags" in self.config else {}))

    def _format_data(self):
        # 格式化数据
        json.dump(self.config, open(os.path.join(self.folder_path, "config.json",),
                  "w", encoding="utf-8"), indent=4, ensure_ascii=False, sort_keys=True)
        json.dump(self.tag_manager.get_tag_dict(), open(file.get_abs_path(
            self.config["tags"], self.folder_path), "w", encoding=self.encoding), indent=4, ensure_ascii=False, sort_keys=True)

    def _creat_text(self, write_list):
        # 创建写入文本
        output = f":{write_list[0]}\n:{write_list[1]}\n:{write_list[2]}\n:"
        for i in write_list[3]:
            output += f"'{i}',"
        output += "\n:"
        for i in write_list[4]:
            output += f"'{i}',"
        return output

    def write_file_data(self, file_path, data_foloder_path, encoding="utf-8"):
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
        os.makedirs(p := os.path.join(
            data_foloder_path, file_site[0]), exist_ok=True)
        # 查找相同文件
        old_data = ["","",""]
        i = "0"
        for i in os.listdir(p):
            fw = open(os.path.join(p, i), 'r+',
                      encoding=encoding).read()[1:].replace("\n", "").split(":")
            if fw[:2] == file_site[1:3]:
                old_data = fw[2:5]

        # 检查数据
        old_data[2] = sorted(algo.merge_item_str([i[1:-1]
                             for i in old_data[2].split(",")], [file_path[1]]))
        if "" in old_data[2]:
            old_data[2].remove("")

        for f in old_data[2]:
            if not file.check_file(fp := os.path.join(self.file_path, f), file_site[1:], self.exc):
                old_data[2].remove(f)
                if not file.file_except(f, self.exc):
                    self.write_file_data([self.file_path, f],
                                         self.info_folder, self.encoding)

        # 写入数据文件
        with open(os.path.join(p, i), 'w', encoding=encoding) as f:
            write_list = [file_site[1],
                          file_site[2],
                          old_data[0],
                          sorted(algo.merge_item_str(
                              [i[1:-1] for i in old_data[1].split(",")], file_tag)),
                          old_data[2]]
            f.write(self._creat_text(write_list))
        return write_list

    def write_data(self):
        # 写入信息文件夹
        for f in file.list_files(self.file_path):
            if not file.file_except(f, self.exc):
                self.write_file_data([self.file_path, f],
                                     self.info_folder, self.encoding)


def get_config(config, default_config, keys):
    # 获取配置
    values = []
    for key in keys:
        if key not in config:
            values.append(default_config[key])
        else:
            values.append(config[key])
    return values
