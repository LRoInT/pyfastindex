import os
import sys
import managerlib as ml

global_config_path = os.path.join(
    os.path.dirname(__file__), "./global")

if __name__ == '__main__':
    manager = ml.Manager(sys.argv[1], global_config_path)
    manager.write_info(sys.argv[1])
