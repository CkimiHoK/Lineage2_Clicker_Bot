from chronicles.chronicle_settings import ChronicleSettings
from logic.classes.dwarven_fighter import DwarvenFighterBot


def create_bot(class_name: str, chronicle_settings: ChronicleSettings):
    bot = None

    if class_name.lower() == "dwarven_fighter":
        bot = DwarvenFighterBot(chronicle_settings)

    return bot
