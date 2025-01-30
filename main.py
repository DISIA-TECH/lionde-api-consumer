from src.python.init_configurations import ConfigLoader
from src.python.system import downloader

if __name__ == "__main__":
    config = ConfigLoader()
    downloader(config)
