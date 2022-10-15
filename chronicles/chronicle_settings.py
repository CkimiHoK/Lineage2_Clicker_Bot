class Panel:
    def __init__(self, anchor_image_path: str = "", panel_info=None):
        if panel_info is None:
            panel_info = dict()

        self.__anchor_image_path = anchor_image_path
        self.__panel_info = panel_info
        self.__x = panel_info.get("x")
        self.__y = panel_info.get("y")
        self.__width = panel_info.get("width")
        self.__height = panel_info.get("height")

    def set_start_point(self, x, y):
        self.__x = x
        self.__y = y

    def get_anchor_image_path(self):
        return self.__anchor_image_path

    def get_size(self):
        return self.__width, self.__height

    def get_start_point(self):
        return self.__x, self.__y

    def get_end_point(self):
        return self.__x + self.__width, self.__y + self.__height

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_region(self):
        return self.__x, self.__y, self.__width, self.__height


class ChronicleSettings:
    def __init__(self, health_panel: Panel, skill_panel: Panel, target_panel: Panel):
        self.__health_panel = health_panel
        self.__skill_panel = skill_panel
        self.__target_panel = target_panel

    def get_health_panel(self):
        return self.__health_panel

    def get_skill_panel(self):
        return self.__skill_panel

    def get_target_panel(self):
        return self.__target_panel
