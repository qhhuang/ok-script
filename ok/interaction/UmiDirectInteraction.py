import ctypes
import time
import math
import random
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

    def send_key(self, key, down_time=0.01):
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
        self.move_to(x,y)

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

    def click(self, x=-1, y=-1, move_back=False, name=None):
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
            self.move_to(x,y)

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
            self.move_to(x,y)
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
            self.move_to(x,y)
        pydirectinput.mouseDown()

    def mouse_up(self, key=None):
        if not self.capture.clickable():
            logger.info(f"window in background, not clickable")
            return
        pydirectinput.mouseUp()

    def should_capture(self):
        return self.capture.clickable()

    def calculate_distance(self,  x=-1, y=-1):
        current_x, current_y = pydirectinput.position()
        if x != -1 and y != -1:
            return math.sqrt((current_x - x) ** 2 + (current_y - y) ** 2)
        else:
            return 0

    def move_to(self, x, y):
        if self.calculate_distance(x, y) > 600:
            print('UmiDirectInteraction 注入')
            current_x, current_y = pydirectinput.position()
            integers = [0, 100]
            random_numbers_x = sorted(random.sample(range(1,100), 10) + integers)
            random_numbers_y = sorted(random.sample(range(1,100), 10) + integers)

            # random_numbers_x = sorted(random.sample(range(50), 10))
            # random_numbers_y = sorted(random.sample(range(50), 10))
            # random_numbers_x = sorted(set([random.randint(0, 50) for _ in range(20)]))
            # random_numbers_y = sorted(set([random.randint(0, 50) for _ in range(20)]))
            # print('[random_numbers_x]',random_numbers_x)
            # print(random_numbers_y)
            for i in range(12):

                rand_current_x = random_numbers_x[i] / 100 * (x - current_x)  + current_x
                rand_current_y = random_numbers_y[i] / 100 * (y - current_y)  + current_y
                pydirectinput.moveTo(int(rand_current_x), int(rand_current_y))
        else:
            pydirectinput.moveTo(x, y)



def is_admin():
    try:
        # Only Windows users with admin privileges can read the C drive directly
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
