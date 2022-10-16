import pyautogui

from chronicles.chronicle_settings import Panel


def fill_main_window_panel(main_window_info):
    return Panel(panel_info=main_window_info)


def fill_panel_start_coords(main_window_panel: Panel, panel: Panel):
    try:
        loc = pyautogui.locateOnScreen(
            panel.get_anchor_image_path(),
            confidence=0.9,  # TODO return to 0.9 after fix HEALTH anchor
            region=main_window_panel.get_region()
        )
        panel.set_start_point(
            loc[0] + int(main_window_panel.get_x()),
            loc[1] + int(main_window_panel.get_y())
        )
        return panel
    except pyautogui.ImageNotFoundException:
        print("panel not found")
