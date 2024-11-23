import os
import sys
import managerlib as ml

global_config_path = os.path.join(
    os.path.dirname(__file__), "./global")

if __name__ == '__main__':
    manager = ml.Manager(global_config_path)
    manager.input_command(sys.argv[1:])
