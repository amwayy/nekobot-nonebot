import os

import nonebot

from nekobot import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'plugins'), 'nekobot.plugins')
    nonebot.run()