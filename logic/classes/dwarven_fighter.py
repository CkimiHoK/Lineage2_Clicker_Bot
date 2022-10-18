from chronicles.chronicle_settings import ChronicleSettings
from logic.abstract_bot import AbstractBot

BUTTON_SIT = "0"
BUTTON_DROP = "3"
BUTTON_ATTACK = "1"
BUTTON_NEAREST_TARGET = "6"
BUTTON_HEAL_POTION = "8"
BUTTON_SPOIL = "2"
BUTTON_SWEEP = "4"


class DwarvenFighterBot(AbstractBot):

    def __init__(self, chronicle_settings: ChronicleSettings):
        super().__init__(chronicle_settings)
        self.__spoil_used = False

    def actions_before_main(self):
        if self.get_self_hp() < 40:
            print("INFO: We need to relax")
            if self.sit_until_heal(BUTTON_SIT):
                return True
            else:
                self.attack_target(BUTTON_ATTACK)
        return False

    def main_actions(self):
        return self.set_target_and_attack(BUTTON_ATTACK, BUTTON_NEAREST_TARGET)

    def actions_after_main(self):
        self.get_drop(BUTTON_DROP)

    def fail_actions(self, fail_count: int):
        if fail_count >= 5:
            self.move_random_location()  # COMMENT THIS STRING IF NOT NEED MOVE
            return True
        elif 1 < fail_count < 5:
            self.rotate_right()
            return False
        else:
            return False

    def actions_while_attack(self, target_hp: int, self_hp: int):
        if self_hp <= 20:
            self.use_skill(BUTTON_HEAL_POTION)
        if not self.__spoil_used and target_hp < 80:
            self.use_skill(BUTTON_SPOIL)
            self.__spoil_used = True

    def actions_on_target_death(self):
        self.use_skill(BUTTON_SWEEP)
        self.__spoil_used = False

