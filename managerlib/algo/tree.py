# 树节点
from typing import Iterable


class TreeNode:
    def __init__(self, data=None, next=None, output_end=False):
        self.data = data
        self.next = next if next is not None else []
        self.output_end = output_end

    def __str__(self):
        return f"TreeNode(data='{self.data}', next={self.next})"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        item = item if isinstance(item, Iterable) and not isinstance(
            item, str) else (item,)
        for i in self.next:
            if type(i) == TreeNode:
                if i.data == item[0]:
                    if len(item) == 1:
                        return i
                    return i[item]
            else:
                if i == item[0]:
                    return i

    def __iter__(self):
        # 迭代器函数
        if self.output_end:
            if not self.next:
                # 不含有子节点时
                yield [self.data]
            for n in self.next:
                if type(n) == TreeNode:
                    #  含有子节点时
                    if not n.next:
                        # 为树末端时
                        yield [self.data, n.data]
                    else:
                        for i in n.walk_end_nodes():
                            yield [self.data] + i
                else:
                    yield [self.data, n]
        else:
            if not self.next:
                # 不含有子节点时
                yield [self.data]
            for n in self.next:
                if type(n) == TreeNode:
                    #  含有子节点时
                    yield [self.data, n.data]
                    if n.next:
                        for i in n.walk_end_nodes():
                            yield [self.data] + i
                else:
                    yield [self.data, n]

    def __setitem__(self, key, value):
        self.next.__setitem__(key, value)

    def add_child(self, data=None, next=None):
        self.next.append(TreeNode(data, next))

    def pop(self, item):
        for i in range(len(self.next)):
            if self.next[i].data == item:
                return self.next.pop(i)

    def walk_nodes(self) -> list:
        # 遍历树节点
        if not self.next:
            return [self.data]
        output = []
        for n in self.next:
            if type(n) == TreeNode:
                output.append([self.data, n.data])
                if n.next:
                    for i in n.walk_end_nodes():
                        output.append([self.data] + i)
            else:
                output.append([self.data, n])
        return output

    def walk_end_nodes(self):
        # 遍历树末端节点
        if not self.next:
            # 遍历到末端节点时
            return [self.data]
        output = []
        for n in self.next:
            if type(n) == TreeNode:
                if not n.next:
                    output.append([self.data, n.data])
                else:
                    for i in n.walk_end_nodes():
                        output.append([self.data] + i)
            else:
                output.append([self.data, n])
        return output

    def search(self, data) -> list:
        # 搜索子节点
        for i in self:
            if i[-1] == data:
                return i[1:]


def dict2tree(data, title=None, exc=None) -> TreeNode:
    # 字典转树
    if exc is None:
        exc = []
    tree = TreeNode(title if title is not None else ".")
    for i in data:
        di = data[i]
        tree.add_child(i)
        if type(di) == dict:
            # 为字典时
            for j in dict2tree(di, exc=exc).next:
                tree[i].next.append(j)
        else:
            if di not in exc:
                if isinstance(di, Iterable) and not isinstance(di, str):
                    # 判断是否可迭代
                    tree[i].next.extend(di)
                else:
                    tree[i].next.append(di)
    return tree


def tree2dict(tree, null_value=None) -> dict:
    # 树转字典
    if len(tree.next) == 0:
        return {}
    output = {}
    for i in tree.next:
        if type(i) == TreeNode:
            if len(i.next) == 0:
                output[i.data] = null_value
            else:
                output[i.data] = tree2dict(i)
        else:
            output[i] = null_value
    return output
