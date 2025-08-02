import ctypes
import time
import math
import random

import numpy as np
import pydirectinput

from ok.capture.BaseCaptureMethod import BaseCaptureMethod
from ok.interaction.BaseInteraction import BaseInteraction
from ok.logging.Logger import get_logger

logger = get_logger(__name__)

pydirectinput.FAILSAFE = False


class UmiDirectInteraction(BaseInteraction):

    def __init__(self, capture: BaseCaptureMethod, hwnd_window):
        super().__init__(capture)
        if not is_admin():
            logger.error(f"You must be an admin to use Win32Interaction")

    def send_key(self, key, down_time=random.uniform(0.05, 0.15)):
        if not self.capture.clickable():
            logger.error(f"can't click on {key}, because capture is not clickable")
            return
        pydirectinput.keyDown(str(key))
        time.sleep(down_time)
        pydirectinput.keyUp(str(key))

    def send_key_down(self, key):
        if not self.capture.clickable():
            logger.error(f"can't click on {key}, because capture is not clickable")
            return
        pydirectinput.keyDown(str(key))

    def send_key_up(self, key):
        if not self.capture.clickable():
            logger.error(f"can't click on {key}, because capture is not clickable")
            return
        pydirectinput.keyUp(str(key))

    def move(self, x, y):
        if not self.capture.clickable():
            return
        x, y = self.capture.get_abs_cords(x, y)
        self.move_to(x, y)

    def swipe(self, x1, y1, x2, y2, duration):
        # Convert coordinates to integers
        x1, y1 = self.capture.get_abs_cords(x1, y1)
        x2, y2 = self.capture.get_abs_cords(x2, y2)

        # Move the mouse to the start point (x1, y1)
        pydirectinput.moveTo(x1, y1)
        time.sleep(0.1)  # Pause for a moment

        # Press the left mouse button down
        pydirectinput.mouseDown()

        # Calculate the relative movement (dx, dy)
        dx = x2 - x1
        dy = y2 - y1

        # Calculate the number of steps
        steps = int(duration / 100)  # 100 steps per second

        # Calculate the step size
        step_dx = dx / steps
        step_dy = dy / steps

        # Move the mouse to the end point (x2, y2) in small steps
        for i in range(steps):
            pydirectinput.moveTo(x1 + int(i * step_dx), y1 + int(i * step_dy))
            time.sleep(0.1)  # Sleep for 10ms

        # Release the left mouse button
        pydirectinput.mouseUp()

    def click(self, x=-1, y=-1, move_back=False, name=None, **kwargs):
        super().click(x, y, name=name)
        if not self.capture.clickable():
            logger.info(f"window in background, not clickable")
            return
        # Convert the x, y position to lParam
        # lParam = win32api.MAKELONG(x, y)
        current_x, current_y = -1, -1
        if move_back:
            current_x, current_y = pydirectinput.position()
        if x != -1 and y != -1:
            x, y = self.capture.get_abs_cords(x, y)
            logger.info(f"left_click {x, y}")
            self.move_to(x, y)

        pydirectinput.click()
        if current_x != -1 and current_y != -1:
            pydirectinput.moveTo(current_x, current_y)

    def right_click(self, x=-1, y=-1, move_back=False, name=None):
        super().right_click(x, y, name=name)
        if not self.capture.clickable():
            logger.info(f"window in background, not clickable")
            return
        # Convert the x, y position to lParam
        # lParam = win32api.MAKELONG(x, y)
        current_x, current_y = -1, -1
        if move_back:
            current_x, current_y = pydirectinput.position()
        if x != -1 and y != -1:
            x, y = self.capture.get_abs_cords(x, y)
            logger.info(f"left_click {x, y}")
            self.move_to(x, y)
        pydirectinput.rightClick()
        if current_x != -1 and current_y != -1:
            pydirectinput.moveTo(current_x, current_y)

    def mouse_down(self, x=-1, y=-1, name=None, key=None):
        if not self.capture.clickable():
            logger.info(f"window in background, not clickable")
            return
        if x != -1 and y != -1:
            x, y = self.capture.get_abs_cords(x, y)
            logger.info(f"left_click {x, y}")
            self.move_to(x, y)
        button = self.get_mouse_button(key)
        pydirectinput.mouseDown(button=button)

    @staticmethod
    def get_mouse_button(key):
        button = pydirectinput.LEFT if key == "left" else pydirectinput.RIGHT
        return button

    def mouse_up(self, key="left"):
        if not self.capture.clickable():
            logger.info(f"window in background, not clickable")
            return
        button = self.get_mouse_button(key)
        pydirectinput.mouseUp(button=button)

    def should_capture(self):
        return self.capture.clickable()

    @staticmethod
    def calculate_distance(x=-1, y=-1):
        current_x, current_y = pydirectinput.position()
        if x != -1 and y != -1:
            return math.sqrt((current_x - x) ** 2 + (current_y - y) ** 2)
        else:
            return 0

    # def move_to(self, x, y):
    #     print('UmiDirectInteraction calculate_distance', self.calculate_distance(x, y))
    #     if self.calculate_distance(x, y) > 100:
    #         print('UmiDirectInteraction 注入')
    #         current_x, current_y = pydirectinput.position()
    #         integers = [0, 100]
    #         random_numbers_x = sorted(random.sample(range(1, 100), 10) + integers)
    #         random_numbers_y = sorted(random.sample(range(1, 100), 10) + integers)
    #         for i in range(12):
    #             rand_current_x = random_numbers_x[i] / 100 * (x - current_x) + current_x
    #             rand_current_y = random_numbers_y[i] / 100 * (y - current_y) + current_y
    #             pydirectinput.moveTo(int(rand_current_x), int(rand_current_y))
    #     else:
    #         pydirectinput.moveTo(x, y)

    def move_to(self, x, y):
        """鼠标相对移动函数，根据x和y方向的偏移量移动鼠标"""


        current_x, current_y = pydirectinput.position()
        x = x - current_x
        y = y - current_y
        def bezier_curve(t, control_points):
            """贝塞尔曲线计算函数，用于生成平滑的移动路径"""
            n = len(control_points) - 1
            result = np.zeros_like(control_points[0], dtype=float)
            for i, point in enumerate(control_points):
                # 计算贝塞尔曲线的加权和
                result += (np.math.comb(n, i) * ((1 - t) ** (n - i)) * (t ** i) * point)
            return result

        try:
            x = int(x)
            y = int(y)

            # 确定移动的总步数（根据最大偏移量计算）
            max_offset = abs(x) if abs(x) > abs(y) else abs(y)

            # 贝塞尔曲线的控制点
            start_point = np.array([0, 0], dtype=float)
            end_point = np.array([x, y], dtype=float)

            # 随机生成中间控制点（使移动路径更自然）
            if x == 0:
                control_x1 = random.uniform(-50, 50)
                control_x2 = random.uniform(-50, 50)
            else:
                control_x1 = random.uniform(x // 100, x // 2)
                control_x2 = random.uniform(x // 100, x // 2)

            if y == 0:
                control_y1 = random.uniform(-50, 50)
                control_y2 = random.uniform(-50, 50)
            else:
                control_y1 = random.uniform(y // 100, y // 2)
                control_y2 = random.uniform(y // 100, y // 2)

            control_point1 = np.array([control_x1, control_y1], dtype=float)
            control_point2 = np.array([control_x2, control_y2], dtype=float)

            # 生成移动的步数（随机增加5-10步使路径更自然）
            # step_count = max_offset // 8 + random.randint(5, 10)
            # 首先有个鼠标移动速度 然后根据距离和速度算出移动时间 移动时间乘以平滑度 等于步数
            move_speed = 250
            smoothness = 4
            step_count = max(int(self.calculate_distance(x, y) / move_speed * smoothness), 10)  # 至少10步确保平滑
            # 生成0到1之间的均匀分布作为贝塞尔曲线的参数
            t_values = np.linspace(0, 1, step_count)
            # t_values = np.linspace(0, 1, total_steps)

            # 计算贝塞尔曲线上的所有点（移动路径）
            path_points = []
            for t in t_values:
                point = bezier_curve(t, [start_point, control_point1, control_point2, end_point])
                path_points.append(point)

            # 将路径点转换为整数数组
            path_points = np.array(path_points, dtype=int)
            # 提取x和y方向的路径
            x_path = [point[0] for point in path_points]
            y_path = [point[1] for point in path_points]

            # 逐步移动鼠标
            for i in range(step_count):
                pydirectinput.moveTo(int(x_path[i] + current_x), int(y_path[i] + current_y))

        except Exception as e:
            print('输入参数错误!', e)



def is_admin():
    try:
        # Only Windows users with admin privileges can read the C drive directly
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
