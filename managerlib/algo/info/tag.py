from fnmatch import fnmatch
from copy import copy
from .. import tree


class TagManager:
    def __init__(self, tag):
        tag = self.sort_tag(tag)
        self.tags = tree.dict2tree(  # 标签
            tag["tags"] if "tags" in tag else {}, title='tags', exc=[0])
        self.same = tree.dict2tree(  # 同义标签
            tag["same"] if "same" in tag else {}, title='same', exc=[0])
        self.trait = tag["trait"] if "trait" in tag else {}  # 标签特征
        self.type = tag["type"]  # 类型标签
        self.creat_mathers()  # 生成匹配器

    def sort_tag(self, tag) -> dict:
        output = {}
        for i in tag:
            output[i] = format_tags(tag[i])
        return output

    def get_tag_dict(self) -> dict:
        # 返回标签字典
        return {"same": tree.tree2dict(self.same,  null_value=0),
                "tags": tree.tree2dict(self.tags,  null_value=0),
                "trait": self.trait, "type": self.type}

    def _creat_ckecker(self, rule) -> callable:
        # 编译检查器
        if rule.startswith(file_match):
            def check(x): return fnmatch("./"+x, "**/"+rule[3:])
        else:
            def check(x): return False
        return check

    def _compile_mather(self, rules) -> list[callable]:
        # 编译匹配器
        com_rules = [lambda f:self._creat_ckecker(
            rule)(f) for rule in rules]  # 规则列表

        def mather(file):
            for rule in com_rules:
                if rule(file):
                    return True
            return False
        return mather

    def creat_mathers(self):
        # 生成匹配器
        self.type_matcher = {}
        for t in self.type:
            if t in self.trait:
                self.type_matcher[t] = self._compile_mather(self.trait[t])
                del self.trait[t]
        self.trait_matcher = {}
        for t in self.trait:
            self.trait_matcher[t] = self._compile_mather(self.trait[t])

    def match(self, file) -> list[str]:
        # 匹配文件
        output = []
        for t in self.type_matcher:
            if self.type_matcher[t](file):
                output.append(t)
        trait_matcher = copy(self.trait_matcher)
        for t in trait_matcher:
            # 匹配标签
            if trait_matcher[t](file):
                output.append(t)
                t_site = self.tags.search(t)
                for i in t_site:
                    # 添加上级标签
                    output.append(i)
                    if i in trait_matcher:
                        # 删除重复标签匹配器
                        del trait_matcher[i]
        return output


def format_tags(tags) -> list[str]:
    # 格式化标签
    if t := type(tags) == list:
        return sorted(tags)
    elif t == dict:
        output = {}
        for i in tags:
            output[i.replace(" ", "_").lower()] = format_tags(tags[i])
        return output
    return tags


file_match = "fn:"
