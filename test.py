import managerlib as ml
import os
global_config_path = os.path.join(
    os.path.dirname(__file__), "./global")

if __name__ == '__main__':
    manager = ml.Manager(r"./test",global_config_path)
    manager.write_info(r"E:\code\pyfastindex\test\files\a copy 3.txt")
    print(manager.get_info(r"E:\code\pyfastindex\test\files\a.txt"))