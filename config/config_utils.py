from config import config
import yaml


def load():
  rawConfig = yaml.safe_load(open("config.yaml", "r").read())
  config.theme = rawConfig["theme"]
  config.width = rawConfig["width"]
  config.height = rawConfig["height"]
  config.providers = rawConfig["providers"]