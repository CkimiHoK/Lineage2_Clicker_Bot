from support_functions import command_line_parser
from chronicles import chronicle_settings_factory
from logic import bot_factory


def start():
    command_line_config = command_line_parser.parse_command_line_params()
    chronicle_settings = chronicle_settings_factory.create_settings(command_line_config["v"])
    bot = bot_factory.create_bot(command_line_config["c"], chronicle_settings)
    # bot.go()


if __name__ == '__main__':
    start()
