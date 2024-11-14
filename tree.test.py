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
for i in a:print(i)
print("-")
print(a.search("a-1-2-1"))