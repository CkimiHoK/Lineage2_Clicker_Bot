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

    def set_target_and_attack(self, button_attack_value: str, button_nearest_value: str):
        if self.get_nearest_target(button_nearest_value):
            return self.attack_target(button_attack_value)
        else:
            mob_x, mob_y = self.get_target_on_screen()
            if mob_x is not None and mob_y is not None:
                self.left_click_no_move(mob_x, mob_y)
                return self.attack_target(button_attack_value)
            else:
                return False

    def attack_target(self, button_attack_value: str):
        if self.get_target_hp() >= 98:
            pyautogui.press(button_attack_value)
            tick = 0
            while True:
                pyautogui.sleep(0.5)
                tick += 1
                target_hp = self.get_target_hp()
                avatar_hp = self.get_self_hp()
                if target_hp <= 0:
                    self.actions_on_target_death()
                    break
                elif target_hp >= 98 and tick >= 20:
                    print("WARN: We are STUCK")
                    pyautogui.press("esc")
                    self.move_random_location()
                    break
                else:
                    self.actions_while_attack(target_hp, avatar_hp)
            return True
        else:
            print("target is not MOB")
            return True

    def get_nearest_target(self, button_nearest_value: str):
        pyautogui.press(button_nearest_value)
        pyautogui.sleep(0.3)
        return self.get_target_hp() >= 98

    def get_target_on_screen(self):
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
        metric_heal = 0
        while True:
            pyautogui.sleep(1)
            current_heal = self.get_self_hp()
            if current_heal < metric_heal:
                print("WARN: We are UNDER ATTACK !!!")
                return False
            else:
                metric_heal = current_heal
            if self.get_self_hp() > 95:
                break
        pyautogui.press(button_sit_value)
        pyautogui.sleep(2)
        return True

    def left_click(self, x_pos, y_pos):
        pyautogui.moveTo(x=x_pos, y=y_pos, duration=0.2)
        pyautogui.mouseDown()
        pyautogui.mouseUp()

    def left_click_no_move(self, x_pos, y_pos):
        pyautogui.keyDown("shift")
        self.left_click(x_pos, y_pos)
        pyautogui.keyUp("shift")

    def get_drop(self, button_drop_value: str, try_count=4):
        for _ in range(try_count):
            pyautogui.sleep(0.5)
            pyautogui.press(button_drop_value)

    def move_random_location(self):
        random_x_loc = random.randint(350, 1400)
        random_y_loc = random.randint(100, 700)
        self.left_click(random_x_loc, random_y_loc)
        pyautogui.sleep(0.5)

    def rotate_right(self):
        pyautogui.keyDown("d")
        pyautogui.sleep(0.8)
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

    @abstractmethod
    def actions_while_attack(self, target_hp: int, self_hp: int):
        pass

    @abstractmethod
    def actions_on_target_death(self):
        pass
