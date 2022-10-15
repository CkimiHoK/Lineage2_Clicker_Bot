from logic.abstract_bot import AbstractBot

BUTTON_SIT = "0"
BUTTON_DROP = "3"
BUTTON_ATTACK = "1"


class DwarvenFighterBot(AbstractBot):
    def actions_before_main(self):
        if self.get_self_hp() < 60:
            print("we need to relax")
            self.sit_until_heal(BUTTON_SIT)
            return True
        return False

    def main_actions(self):
        return self.attack_target(BUTTON_ATTACK)

    def actions_after_main(self):
        self.get_drop(BUTTON_DROP)

    def fail_actions(self, fail_count: int):
        if fail_count >= 3:
            self.move_random_location()
            return True
        elif 1 < fail_count < 3:
            self.rotate_right()
            return False
        else:
            return False
