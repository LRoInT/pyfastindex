from fnmatch import fnmatch
import re

from . import tree
from . import sort


class TagManager:
    def __init__(self, tag):
        tag = self.sort_tag(tag)
        self.tags = tree.dict2tree(  # 标签
            tag["tags"] if "tags" in tag else {}, title='tags', exc=[0])
        self.same = tree.dict2tree(  # 同义标签
            tag["same"] if "same" in tag else {}, title='same', exc=[0])
        self.trait = tag["trait"] if "trait" in tag else {}  # 标签特征

    def sort_tag(self, tag):
        output = {}
        for i in tag:
            output[i] = sort.format_tags(tag[i])
        return output

    def name2tag(self, name):
        output = []
        append = output.append
        for t in self.trait:
            for n in self.trait[t]:
                if n.startswith("fn:"):
                    if fnmatch("./"+name, "**/"+n[3:]) or n in name:
                        append(t)
                        break
        return output
