import cv2
import numpy as np


def calc_self_hp(image_path: str):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    mask = cv2.inRange(image, (0, 0, 150), (125, 90, 255))

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    (contours, hierarchy) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    percent = 0
    for cnt in contours:
        cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        cv2.convexHull(cnt)

        left = list(cnt[cnt[:, :, 0].argmin()][0])
        right = list(cnt[cnt[:, :, 0].argmax()][0])
        length = right[0] - left[0]

        percent = round(100 * length / 330)

    return percent


def calc_target_hp(image_path: str):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    mask = cv2.inRange(image, (0, 0, 150),  (125, 90, 255))

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    (contours, hierarchy) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    percent = 0
    for cnt in contours:
        cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        cv2.convexHull(cnt)

        left = list(cnt[cnt[:, :, 0].argmin()][0])
        right = list(cnt[cnt[:, :, 0].argmax()][0])
        length = right[0] - left[0]

        percent = round(100 * length / 131)

    return percent


def find_target(image_path: str):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    image[0:70, 0:355] = (0, 0, 0)  # HEALTH_BAR y_from:y_to x_from:x_to
    image[720:900, 0:355] = (0, 0, 0)  # CHAT y_from:y_to x_from:x_to
    image[350:600, 750:850] = (0, 0, 0)  # AVATAR y_from:y_to x_from:x_to
    image[865:900, 600:1000] = (0, 0, 0)  # SKILL_PANEL y_from:y_to x_from:x_to

    image = exclude_targeted(image)

    gray_game_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, only_white = cv2.threshold(gray_game_img, 252, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 7))
    closed = cv2.morphologyEx(only_white, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, kernel, iterations=1)
    closed = cv2.dilate(closed, kernel, iterations=1)

    (contours, hierarchy) = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    x_pos = None
    y_pos = None
    for cnt in contours:
        cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        cv2.convexHull(cnt)

        left = list(cnt[cnt[:, :, 0].argmin()][0])
        right = list(cnt[cnt[:, :, 0].argmax()][0])
        if right[0] - left[0] < 20:
            continue
        center = round((right[0] + left[0]) / 2)
        center = int(center)

        x_pos = center
        y_pos = right[1] + 20
        break

    return x_pos, y_pos


def exclude_targeted(image):
    # TODO REMOVE IMAGE name HARDCODE
    template = cv2.imread('chronicles/c1/anchor_images/target_anchor.png', 0)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, only_white = cv2.threshold(gray_image, 130, 255, cv2.THRESH_TOZERO)
    ret, tp1 = cv2.threshold(template, 130, 255, cv2.THRESH_TOZERO)

    res = cv2.matchTemplate(only_white, tp1, cv2.TM_CCORR_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        image[pt[1]+5:pt[1] + 15, pt[0] - 40:pt[0]+55] = (0, 0, 0)

    return image
