class ArgvParser:
    def __init__(self, rules):
        self.rules = rules

    def _creat_v_k(self, dic):
        # 创建键值对
        v_k = {}  # 从值获取键
        for r in dic:
            if "s" in dic[r]:  # 短参数
                v_k[dic[r]["s"]] = r
            if "l" in dic[r]:  # 长参数
                v_k[dic[r]["l"]] = r
        return v_k

    def _get_argv(self, argv_str):
        if argv_str.startswith("-") and len(argv_str) >= 2:  # 短参数
            argv_str = argv_str[1:]
            if argv_str.startswith("-") and len(argv_str) >= 2:  # 长参数
                v = argv_str[1:]
            else:
                v = argv_str
            return v
        else:
            return False

    def _parse(self, argv, rules, sub=False):
        v_k = self._creat_v_k(rules)
        # 解析命令行参数
        output = {"nokey": []}
        while len(argv):
            """
            if argv[0].startswith("--") and len(argv[0]) > 3:  # 长参数
                if (v := argv[0][2:]) not in v_k:
                    # 出现不该存在的参数时
                    raise Exception("Unknown option: " + argv[0])
            elif argv[0].startswith("-") and len(argv[0]) > 2:  # 短参数
                if (v := argv[0][1:]) not in v_k:
                    raise Exception("Unknown option: " + argv[0])"""
            v = None
            while True:
                # 清除无参数项并获取第1个参数
                """if argv[0].startswith("--") and len(argv[0]) > 3:  # 长参数
                    if v := argv[0][2:] not in v_k:
                        # 出现不该存在的参数时
                        return output, argv
                    break
                elif argv[0].startswith("-") and len(argv[0]) > 2:  # 短参数
                    if v := argv[0][1:] not in v_k:
                        return output, argv
                    break"""
                if v := self._get_argv(argv[0]):
                    if not v  in v_k:
                        if sub:
                            return output, argv, True
                        # 出现不该存在的参数时
                        raise ValueError("Unknown option: " + argv[0])
                    break
                else:
                    output["nokey"].append(argv[0])
                    argv = argv[1:]
                if not len(argv):
                    return output, [], True if sub else False
            k = v_k[v]  # 获取键
            if rules[k]["i"]:
                # 当参数需要输入时
                while True:
                    output[k], argv, exit = self._parse(  # 获取参数输入
                        argv[1:], rules[k].get("sub", {}), sub=True)
                    if exit:
                        break
            else:
                # 当参数不需要值时
                output[k] = True
                argv = argv[1:]
            """# 清除重复
            if "s" in rules[k]:
                v_k.pop(rules[v_k[k]]["s"])
            if "l" in rules[k]:
                v_k.pop(rules[k]["l"])"""
        return output, argv, True if sub else False

    def parse(self, argv):
        # 解析命令行参数
        output = {}  # 解析结果
        parse_argv, argv, exit = self._parse(argv, self.rules)
        if exit:
            raise ValueError("Unknown option: " + argv[0])
        output.update(parse_argv)
        return output
