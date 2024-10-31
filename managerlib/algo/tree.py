# 树节点
class TreeNode:
    def __init__(self, data=None, next=None, output_end=False):
        self.data = data
        self.next = next if next is not None else []
        self.output_end = output_end

    def __str__(self):
        return f"TreeNodedata={self.data}, next={self.next})"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        for i in self.next:
            if i.data == item:
                return i
        raise KeyError(f"No child named {item}")

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

    def walk_nodes(self):
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


# 字典转树
def dict2tree(data, title=None, exc=None):
    if exc is None:
        # 排除项
        exc = []
    tree = TreeNode(title if title is not None else ".")
    for i in data:
        di = data[i]
        tree.add_child(i)
        if type(di) == dict:
            for j in di:
                if type(di[j]) == dict:
                    # 为字典时
                    tree[i].next.append(dict2tree(di[j], j))
                else:
                    # 为普通值时
                    tree[i].next.append(di[j])
        else:
            if di not in exc:
                tree[i].next.append(di)
    return tree


def tree2dict(tree, null_value=None):
    if null_value is None:
        # 填充值
        null_value = 0
    if not tree.next:
        return {tree.data: null_value}
    dic = {tree.data: {}}
    for i in tree.next:
        if type(i) == TreeNode:
            dic[tree.data][i.data] = tree2dict(i, null_value)
        else:
            dic[tree.data][i] = i
    return dic
