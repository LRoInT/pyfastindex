from . import tree
from . import tag
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


def merge_item_str(lis1, lis2):
    # 合并两个列表
    setall = list(set(lis1+lis2))
    """
    deled_list = [] # 删除的项
    deled_num = 0  # 删除的个数
    for i in range(len(setall)):
        for j in range(i+1, len(setall)):
            lenth = min(len(setall[i-deled_num]), len(setall[j - deled_num]))
            if lenth == 0:
                # 删除无用项
                deled_list.append(setall[i-deled_num])
                del setall[i-deled_num]
                deled_num += 1"""
    return setall
