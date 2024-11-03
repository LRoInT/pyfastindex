from fnmatch import fnmatch
import copy
from . import tree
from .. import algo


class TagManager:
    def __init__(self, tag):
        tag = self.sort_tag(tag)
        self.tags = tree.dict2tree(  # 标签
            tag["tags"] if "tags" in tag else {}, title='tags', exc=[0])
        self.same = tree.dict2tree(  # 同义标签
            tag["same"] if "same" in tag else {}, title='same', exc=[0])
        self.trait = tag["trait"] if "trait" in tag else {}  # 标签特征
        self.type = tag["type"]  # 类型标签
        self.tag_matcher = TagMatcher(  # 标签匹配器
            tag["tags"], tag["trait"], tag["type"])

    def sort_tag(self, tag):
        output = {}
        for i in tag:
            output[i] = algo.format_tags(tag[i])
        return output

    def get_tag_dict(self):
        # 返回标签字典
        return {"same": tree.tree2dict(self.same,  null_value=0),
                "tags": tree.tree2dict(self.tags,  null_value=0),
                "trait": self.trait, "type": self.type}


def format_tags(tags):
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


class TagMatcher:
    # 标签匹配器
    def __init__(self, tags, trait, type):
        self.trait = copy.copy(trait)
        self.type = copy.copy(type)
        self.matchers = self.creat_mathers()

    def _creat_ckecker(self, rule):
        # 编译检查器
        if rule.startswith(file_match):
            def check(x): return fnmatch("./"+x, "**/"+rule[3:])
        else:
            def check(x): return False
        return check

    def _compile_rule(self, rule):
        # 编译规则
        def output(file):
            if self._creat_ckecker(rule)(file):
                return True
        return output

    def _compile_mather(self, rules):
        # 编译匹配器
        com_rules = [self._compile_rule(rule) for rule in rules]

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

    def match(self, file):
        # 匹配文件
        output = []
        for t in self.type_matcher:
            if self.type_matcher[t](file):
                output.append(t)
        """while trait != 0:
            for t in trait:
                if not self.matchers["trait"][t](file):
                    output.append(t)
                    trait = trait[t]"""
        for t in self.trait_matcher:
            if self.trait_matcher[t](file):
                output.append(t)
        return output
