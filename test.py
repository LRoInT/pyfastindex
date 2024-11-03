import managerlib as ml
import os
global_config_path = os.path.join(
    os.path.dirname(__file__), "./global_config.json")

if __name__ == '__main__':
    manager = ml.Manager(r"E:\\something\\something_nice",global_config_path)
    print(1,manager.tag_manager.tag_matcher.type_matcher,3)
    print(2,manager.tag_manager.tag_matcher.type_matcher["image"](r"E:\something\something_nice\img\表情包\img_1925331148_1715694625014.jpeg"))