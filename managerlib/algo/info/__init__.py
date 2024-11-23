from . import tag
from . import link


class InfoParser:
    def __init__(self, tags, link_rules):
        self.tags_parser = tag.TagParser(tags)
        self.link_parser = link.LinkParser(link_rules)
        self.files = []

    def parse(self, file):
        self.files.append(file)
        return self.tags_parser.parse(file), []
