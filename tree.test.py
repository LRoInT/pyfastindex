from managerlib.algo import tree
a = tree.TreeNode("a", next=[
    tree.TreeNode("a-1", next=[
        tree.TreeNode("a-1-1", next=[]),
        tree.TreeNode("a-1-2", next=[
            tree.TreeNode("a-1-2-1", next=[]),
            tree.TreeNode("a-1-2-2", next=[])
        ])
    ]),
    tree.TreeNode("a-2", next=[
        tree.TreeNode("a-2-1", next=[])
    ])
])
print(tree.tree2dict(a,"a"))
print(a["a-1"])
a.pop("a-1")
print(a)