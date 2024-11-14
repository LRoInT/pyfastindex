from . import tree
from . import info
# 树结构打印工具


def tree_printer(t, level=0):
    # 打印树
    if type(t) == tree.TreeNode:
        for i in ["TreeNode:{", f" data = {t.data}", " next={"]:
            print(" "*level*2+i)

        for i in t.next:
            tree_printer(i, level+1)

        print(" "*level*2+" }")
    # 打印常规数据
    else:
        print(" "*level*2+str(t))
        return
    print(" "*level*2+"}")


def merge_item_str(lis1, lis2) -> list:
    # 合并两个列表
    output = list(set(lis1+lis2))
    if "" in output:
        output.remove("")
    return output