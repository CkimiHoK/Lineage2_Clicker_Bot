from chronicles.chronicle_settings import Panel

PATH = "chronicles/c1/anchor_images/"

HEALTH_PANEL_IMAGE_NAME = "health_panel_anchor.png"
HEALTH_PANEL_SIZE = {"width": 355, "height": 70}

SKILL_PANEL_IMAGE_NAME = "skill_panel_anchor.png"
SKILL_PANEL_SIZE = {"width": 415, "height": 50}

TARGET_PANEL_IMAGE_NAME = "target_panel_anchor.png"
TARGET_PANEL_SIZE = {"width": 150, "height": 35}


def create_panels():
    health_panel = Panel(PATH + HEALTH_PANEL_IMAGE_NAME, HEALTH_PANEL_SIZE)
    skill_panel = Panel(PATH + SKILL_PANEL_IMAGE_NAME, SKILL_PANEL_SIZE)
    target_panel = Panel(PATH + TARGET_PANEL_IMAGE_NAME, TARGET_PANEL_SIZE)

    return health_panel, skill_panel, target_panel
