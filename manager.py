import sys
import managerlib as ml


if __name__ == '__main__':
    manager = ml.Manager(sys.argv[1],".data")
    manager.write_data()