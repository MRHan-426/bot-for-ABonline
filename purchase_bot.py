import cv2
import numpy as np
import pyautogui
import time
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

ocr = PaddleOCR(use_angle_cls=True, lang="en")  # need to run only once to download and load model into memory
print("ocr initialization success")

BUTTON_BUY = cv2.imread('image/button_buy.jpg', cv2.IMREAD_GRAYSCALE)

MARKET_REGION = (338, 315, 900, 700)
PRICE_REGION = (920, 473, 120, 531)
BUY_COMFIRMATION_POS = (1008, 860) # 954~1050  850~880 
MINUS_SIGN_POS = (651, 708) # range 5

PRICE_TABLE = np.array([[3],
                        [4.0, 4.1, 4.2],
                        [5.0, 5.1, 5.2],
                        [6.0, 6.1, 6.2],
                        [7.0, 7.1]])
OPTIONAL_PRICE_TABLE = np.array([4.3, 5.3, 6.3, 8.0, 8.1])

class purchaseBot():
    def __init__(self, parent=None):
        """!
        @brief      Constructs a new instance.

        """
        self.screen = np.array(pyautogui.screenshot(region = MARKET_REGION))
        self.price_region = np.array(pyautogui.screenshot(region = PRICE_REGION))
        self.gray_screen = cv2.cvtColor(self.screen, cv2.COLOR_BGR2GRAY)

    def find_buy_button(self):
        """!
        @brief      Use opencv template match to locate "BUY" button.

        """
        h, w = BUTTON_BUY.shape
        result = cv2.matchTemplate(self.gray_screen, BUTTON_BUY, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.8)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(self.screen, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        cv2.imwrite("image/screen2.jpg", self.screen)


    def update_screenshot(self):
        """!
        @brief      Update screenshot.

        """
        self.screen = np.array(pyautogui.screenshot(region = MARKET_REGION))
        self.price_region = np.array(pyautogui.screenshot(region = PRICE_REGION))
        self.gray_screen = cv2.cvtColor(self.screen, cv2.COLOR_BGR2GRAY)    
        

    def read_price_from_screen(self):
        """!
        @brief      Use paddle ocr to get the prices.

        """
        result = ocr.ocr(self.screen, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            if res != None:
                for line in res:
                    print(line)

        result = result[0]
        if result != None:
            boxes = [line[0] for line in result]
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
            im_show = draw_ocr(self.screen, boxes, txts, scores, font_path='./fonts/simfang.ttf')
            im_show = Image.fromarray(im_show)
            return np.array(im_show)
        else:
            return np.array(self.screen)
        # cv2.destroyAllWindows()
        # im_show.save('image/result.jpg')
        # cv2.imwrite("image/screen2.jpg", self.price_region)


    def mouse_move(self, pos1, pos2, duration=0.5, num_points = 10):
        """!
        @brief      Mouse move from position1 to position2
                    Simulate human mouse movement
        
        @param      duration: moving time
        @param      num_points: interval points between the two points
        """

        x1, y1 = pos1
        x2, y2 = pos2
        sleep_duration = duration / num_points

        for _ in range(num_points):
            x_offset = random.randint(-5, 5)
            y_offset = random.randint(-5, 5)
            x1 += (x2 - x1) / num_points + x_offset
            y1 += (y2 - y1) / num_points + y_offset
            pyautogui.moveTo(x1, y1, duration = sleep_duration, tween = pyautogui.easeInOutQuad)
            
        pyautogui.moveTo(x2, y2)

    def mouse_click(self):
        """!
        @brief      Mouse click once

        """
        pyautogui.click()

    def store_money_in_guild_account(self):
        pass

    def take_out_money_from_guild_account(self):
        pass

    def log_out(self):
        pass

    def log_in(self, account):
        pass

    def open_market(self):
        pass

    def swipe_down(self):
        pass

    def turn_page(self):
        pass

    def search_for_item(self, name):
        pass

    def reset_filter_settings(self):
        pass

    def create_buy_order(self):
        pass

    def current_order_invalid(self):
        pass

    def money_not_enough(self):
        pass
    
    def calculate_max_price(self):
        pass


if __name__ == '__main__':

    pBot = purchaseBot()
    while(True):
        # pBot.find_buy_button()
        pBot.update_screenshot()
        img = pBot.read_price_from_screen()
        cv2.imshow("Price_OCR", img)
        cv2.waitKey(1000)
    cv2.destroyAllWindows()



