import argparse
import os
import uuid
from datetime import datetime
from pathlib import Path

import yaml
from setuptools.command.setopt import config_file


class Util:
    @staticmethod
    def get_projiect_directory():
        """获取文件路径"""
        root = Path(__file__).resolve().parent.parent.parent
        return f"{root}{os.sep}" # os.sep 可以使用系统的路径分隔符

    @staticmethod
    def get_config_file_path():
        default_config_file = "config.yaml"
        """获取配置文件路径"""
        if os.path.exists(Util.get_projiect_directory() + "data/." + default_config_file):
            config_file =  "data/." + default_config_file
        else:
            config_file = Util.get_projiect_directory() + default_config_file
        return  config_file

    @staticmethod
    def get_config():
        """加载配置文件"""
        parser = argparse.ArgumentParser(description="Server configuration")
        config_file = Util.get_config_file_path()
        parser.add_argument("--config", default=config_file, help="Path to the configuration file")
        args = parser.parse_args()
        print(f"Loading configuration from {config_file}")
        with open(config_file, "r",encoding="utf-8") as f:
            config = yaml.safe_load(f)
        #初始化目录
        Util.init_directory(config)
        return config

    @staticmethod
    def init_directory(config):
        results = set()
        def _traverse(data):
            if isinstance(data, dict):
                for key, value in data.items():
                    if "output_dir" in data:
                        results.add(data["output_dir"])
                    for value in data.values():
                        _traverse(value)
            elif isinstance(data, list):
                for item in data:
                    _traverse(item)

        _traverse(config)
        #同一创建目录
        for result in results:
            try:
                os.makedirs(Util.get_projiect_directory() + result,exist_ok=True)
            except PermissionError:
                print("权限不足")

    @staticmethod
    def get_random_file_path(dir:str,ex_name:str):
        file_name = f"{datetime.now().date()}_{uuid.uuid4().hex}.{ex_name}"
        file_path = os.path.join(dir,file_name)
        return file_path

if __name__ == "__main__":
    print(Util.get_projiect_directory())
    Util.get_config()