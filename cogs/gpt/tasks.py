# currently not in use, but it will be used in the future

# import datetime
# import os

# from discord.ext import tasks

from cogs import CogsExtension

from .utils import ChatGPTUtils


class ChatGPTTasks(CogsExtension):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.utils = ChatGPTUtils()
