import os
import json
from . import algo
from . import file


# 数据管理器


class Manager:

    def __init__(self, file_path, folder_path):
        self.file_path = file_path
        self.folder_path = os.path.join(self.file_path, folder_path)
        self.load_data()
        self.tag_manager = algo.tag.TagManager(self.tags)

    def load_data(self):
        data = json.load(open(os.path.join(self.folder_path,
                                           "config.json"), "r", encoding="utf-8"))
        self.exc = data["except"] if "except" in data else []  # 排除对象
        self.data_folder = data["data"] if os.path.isabs(  # 数据文件夹
            data["data"]) else os.path.join(self.folder_path, data["data"])
        # 编码
        self.encoding = data["encoding"] if "encoding" in data else "utf-8"
        self.tags = json.load(open(data["tags"] if os.path.isabs(  # 标签
            data["tags"]) else os.path.join(self.folder_path, data["tags"]), encoding="utf-8")) if "tags" in data else {}

    def _creat_text(self, write_list):
        # 创建写入文本
        output = f":{write_list[0]}\n:{write_list[1]}\n:{write_list[2]}\n:"
        for i in write_list[3]:
            output += f'"{i}",'
        output += "\n:"
        for i in write_list[4]:
            output += f'"{i}",'
        return output

    def write_file_data(self, file_path, data_foloder_path, encoding="utf-8"):
        """
        :file_size
        :file_hash
        :file_name
        :file_tag
        :file_path
        """
        file_site = file.set_file_site(os.path.join(*file_path))
        file_tag = self.tag_manager.name2tag(file_path[1])
        # 创建文件夹
        os.makedirs(p := os.path.join(
            data_foloder_path, file_site[0]), exist_ok=True)
        # 查找相同文件
        old_data = ["" for _ in range(3)]
        i = "0"
        for i in os.listdir(p):
            fw = open(os.path.join(p, i), 'r+',
                      encoding=encoding).read()[1:].replace("\n", "").split(":")
            if fw[:2] == file_site[1:3]:
                old_data = fw[2:5]

        # 检查数据
        old_data[2] = sorted(algo.merge_item_str([i[1:-1] for i in old_data[2].split(",")], [file_path[1]]))
        old_data[2].remove("")
        
        for f in old_data[2]:
            if not file.check_file(fp := os.path.join(self.file_path, f), file_site[1:],self.exc):
                old_data[2].remove(f)
                if not file.file_except(f, self.exc):
                    self.write_file_data([self.file_path, f],
                                         self.data_folder, self.encoding)
                
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
        # 写入数据文件夹
        for f in file.list_files(self.file_path):
            if not file.file_except(f, self.exc):
                self.write_file_data([self.file_path, f],
                                     self.data_folder, self.encoding)
