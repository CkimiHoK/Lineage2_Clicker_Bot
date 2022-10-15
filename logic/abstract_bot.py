import pyautogui
import random

from abc import ABC, abstractmethod
from chronicles.chronicle_settings import ChronicleSettings
from support_functions import main_window
from logic.services import opencv_service
from logic.services import panel_info_filler

pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True

HEALTH_PANEL_SCREENSHOT_NAME = "screenshots/health_panel.png"
TARGET_PANEL_SCREENSHOT_NAME = "screenshots/target_panel.png"
GAME_WINDOW_SCREENSHOT_NAME = "screenshots/game_window.png"


class AbstractBot(ABC):
    def __init__(self, chronicle_settings: ChronicleSettings):
        self.__main_window_panel = panel_info_filler.fill_main_window_panel(
            main_window.get_window_info()
        )

        self.__health_panel = panel_info_filler.fill_panel_start_coords(
            self.__main_window_panel,
            chronicle_settings.get_health_panel()
        )

        self.__target_panel = panel_info_filler.fill_panel_start_coords(
            self.__main_window_panel,
            chronicle_settings.get_target_panel()
        )

    def go(self):
        print("run loop...")

        fail_count = 0
        while True:
            if self.actions_before_main():
                continue

            if self.main_actions():
                self.actions_after_main()
                fail_count = 0
            else:
                fail_count += 1

            if self.fail_actions(fail_count):
                fail_count = 0

        print("bot stopped")

    def attack_target(self, button_attack_value: str):
        mob_x, mob_y = self.get_target()
        if mob_x is not None and mob_y is not None:
            self.left_click_no_move(mob_x, mob_y)

            if self.get_target_hp() >= 98:
                pyautogui.press(button_attack_value)
                while True:
                    pyautogui.sleep(1)
                    if self.get_target_hp() <= 0:
                        break
                return True
            else:
                print("ERROR: target is not MOB")
                return False
        else:
            print("ERROR: can't found target")
            return False

    def get_target(self):
        pyautogui.screenshot(
            GAME_WINDOW_SCREENSHOT_NAME,
            region=self.__main_window_panel.get_region()
        )
        return opencv_service.find_target(GAME_WINDOW_SCREENSHOT_NAME)

    def get_self_hp(self):
        pyautogui.screenshot(
            HEALTH_PANEL_SCREENSHOT_NAME,
            region=self.__health_panel.get_region()
        )
        return opencv_service.calc_self_hp(HEALTH_PANEL_SCREENSHOT_NAME)

    def get_target_hp(self):
        pyautogui.screenshot(
            TARGET_PANEL_SCREENSHOT_NAME,
            region=self.__target_panel.get_region()
        )
        return opencv_service.calc_target_hp(TARGET_PANEL_SCREENSHOT_NAME)

    def sit_until_heal(self, button_sit_value: str):
        pyautogui.press(button_sit_value)
        while True:
            pyautogui.sleep(1)
            if self.get_self_hp() > 95:
                break
        pyautogui.press(button_sit_value)
        pyautogui.sleep(2)

    def left_click(self, x_pos, y_pos):
        pyautogui.moveTo(x=x_pos, y=y_pos, duration=0.2)
        pyautogui.mouseDown()
        pyautogui.mouseUp()

    def left_click_no_move(self, x_pos, y_pos):
        pyautogui.keyDown("shift")
        self.left_click(x_pos, y_pos)
        pyautogui.keyUp("shift")

    def get_drop(self, button_drop_value: str, try_count=3):
        for _ in range(try_count):
            pyautogui.sleep(0.2)
            pyautogui.press(button_drop_value)

    def move_random_location(self):
        random_x_loc = random.randint(350, 1400)
        random_y_loc = random.randint(100, 700)
        self.left_click(random_x_loc, random_y_loc)

    def rotate_right(self):
        pyautogui.keyDown("d")
        pyautogui.sleep(0.6)
        pyautogui.keyUp("d")

    def use_skill(self, button_skill_value: str):
        pyautogui.press(button_skill_value)

    @abstractmethod
    def actions_before_main(self):
        pass

    @abstractmethod
    def main_actions(self):
        pass

    @abstractmethod
    def actions_after_main(self):
        pass

    @abstractmethod
    def fail_actions(self, fail_count: int):
        pass
