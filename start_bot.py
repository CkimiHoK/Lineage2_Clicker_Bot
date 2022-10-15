import time

from support_functions import command_line_parser
from chronicles import chronicle_settings_factory
from logic import bot_factory


def start():
    command_line_config = command_line_parser.parse_command_line_params()
    chronicle_settings = chronicle_settings_factory.create_settings(int(command_line_config["v"]))
    bot = bot_factory.create_bot(command_line_config["c"], chronicle_settings)
    bot.go()


if __name__ == '__main__':
    print("We start across 5 seconds !")
    seconds = 0
    while seconds < 5:
        print(5-seconds, " seconds remaining...")
        time.sleep(1)
        seconds += 1
    start()
