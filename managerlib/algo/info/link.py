import os


class LinkManager:
    def __init__(self):
        pass

    def _isid(self, file) -> list | bool:
        # 判断文件名末尾是否证明与其它文件相关
        if file == "":
            return [0]
        if str.isdigit(id := file.split(".")[0]):
            return [id]
        return False

    def check_link(self, file1, file2) -> list[list] | bool:
        # 检查两个文件从文件名是否有关联
        file1 = os.path.basename(file1).split(".")[0]
        file2 = os.path.basename(file2).split(".")[0]
        n = 0
        while True:
            # 找出文件名相同部分
            if file1[n] == file2[n]:
                n += 1
            else:
                break
        # 文件名末尾都为数字时
        if (f1_n := self._isid(file1[n:])) and (f2_n := self._isid(file2[n:])):
            return sorted_ids(f1_n, f2_n)
        return False


def sorted_id_2(id1, id2) -> list[list]:
    # 排序2个id
    # 从长度判断
    if (id1_l := len(id1)) > (id2_l := len(id2)):
        return [id2, id1]
    elif id1_l < id2_l:
        return [id1, id2]
    else:
        e = max(id1_l, id2_l)
        n = 0
        while True:
            if id1[n] > id2[n]:
                return [id2, id1]
            elif id1[n] < id2[n]:
                return [id1, id2]
            n += 1
            if n == e:
                return [id1, id2]


def sorted_ids(ids) -> list:
    # 排序多个id
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            ids[i], ids[j] = sorted_id_2(ids[i], ids[j])
    return ids
