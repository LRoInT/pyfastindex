class ArgvParser:
    def __init__(self, rules):
        self.rules = rules

    def _parse(self, argv, v_k):
        # 解析命令行参数
        if argv[0][0] != "-": # 第一项不为参数时
            return argv[0], argv[1:]
        output = {}
        while len(argv) > 0:
            if argv[0].startswith("--") and len(argv[0]) > 3:  # 长参数
                if (v := argv[0][2:]) not in v_k:
                    # 出现不该存在的参数时
                    raise Exception("Unknown option: " + argv[0])
            elif argv[0].startswith("-"):  # 短参数
                if (v := argv[0][1:]) not in v_k:
                    raise Exception("Unknown option: " + argv[0])
            k = v_k[v]  # 获取键
            if self.rules[k]["i"]:
                # 当参数需要值时
                if argv[1][0] != "-":
                    # 当下一项是参数值时
                    output[k] = argv[1]
                    argv = argv[2:]
                else:
                    # 下一项是当前参数的参数时
                    output[k], argv = self._parse(argv[1:], v_k)
            else:
                # 当参数不需要值时
                output[k] = True
                argv = argv[1:]
            # 清除重复
            if "s" in self.rules[k]:
                v_k.pop(self.rules[v_k[k]]["s"])
            if "l" in self.rules[k]:
                v_k.pop(self.rules[k]["l"])
        return output, argv

    def parse(self, argv):
        # 解析命令行参数
        v_k = {}  # 从值获取键
        for r in self.rules:
            if "s" in self.rules[r]:  # 短参数
                v_k[self.rules[r]["s"]] = r
            if "l" in self.rules[r]:  # 长参数
                v_k[self.rules[r]["l"]] = r
        output = {}  # 解析结果
        if argv[0][0] != "-":
            output["default"] = argv[0]  # 默认值
            argv = argv[1:]
        output.update(self._parse(argv, v_k)[0])
        return output
