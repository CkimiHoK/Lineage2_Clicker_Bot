from chronicles.c1 import c1_panels_factory
from chronicles.chronicle_settings import ChronicleSettings


def create_settings(chronicle_version: int):
    chronicle_settings = None

    if chronicle_version == 1:
        chronicle_settings = ChronicleSettings(*c1_panels_factory.create_panels())

    return chronicle_settings
