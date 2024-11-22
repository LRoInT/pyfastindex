import json
from managerlib import argv
argvtest=argv.ArgvParser(json.load(open(r"global\prog_argv.json","r",encoding="utf-8")))
print(argvtest.parse(["-w","111","-a","222","-d","333"]))