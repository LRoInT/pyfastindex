def format_tags(tags):
    # 格式化标签
    if t:=type(tags) == list:
        return sorted(tags)
    elif t == dict:
        output = {}
        for i in tags:
            output[i.replace(" ", "_").lower()] = format_tags(tags[i])
        return output
    return tags
