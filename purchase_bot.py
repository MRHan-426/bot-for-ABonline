import cv2
import numpy as np
import pyautogui
import time
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

ocr = PaddleOCR(use_angle_cls=True, lang="en")  # need to run only once to download and load model into memory
print("ocr initialization success")

BUTTON_BUY = cv2.imread('image/button_buy.jpg', cv2.IMREAD_GRAYSCALE)
ERROR_MESSAGE_OK_BUTTON_INVALID_ORDER = cv2.imread('image/ERROR_MESSAGE_OK_BUTTON_INVALID_ORDER.jpg', cv2.IMREAD_GRAYSCALE)
ERROR_MESSAGE_OK_BUTTON_NO_MONEY = cv2.imread('image/ERROR_MESSAGE_OK_BUTTON_NO_MONEY.jpg', cv2.IMREAD_GRAYSCALE)


MARKET_REGION = (338, 315, 900, 700)
PRICE_REGION = (920, 473, 120, 531)
BUY_COMFIRMATION_POS = (1008, 860) # 954~1050  850~880 
MINUS_SIGN_POS = (651, 708) # range 5

PRICE_TABLE = np.array([[3],
                        [4.0, 4.1, 4.2, 4.3],
                        [5.0, 5.1, 5.2, 5.3],
                        [6.0, 6.1, 6.2, 6.3],
                        [7.0, 7.1, 8.0]])

ACCOUNT_LIST = ['mail1', 'mail2', 'mail3', 'mail4', 'mail5']

DICTIONARY_FIBER = ['FLAX',
                    'HEMP',
                    'UN HEMP',
                    'RA HEMP',
                    'EXPONE HEMP',
                    'SKY',
                    'UN SKY',
                    'RA SKY',
                    'EX SKY',
                    'AM',
                    'UN AM',
                    'RA AM',
                    'EX AM',
                    'SUN',
                    'UN SUN',
                    'GHOST H']

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


    def mouse_move(self, target, duration=0.5, num_points = 10):
        """!
        @brief      Mouse move from position1 to position2
                    Simulate human mouse movement
        
        @param      duration: moving time
        @param      num_points: interval points between the two points
        """

        x1, y1 = pyautogui.position()
        x2, y2 = target
        sleep_duration = duration / num_points

        for _ in range(num_points):
            x_offset = random.randint(-5, 5)
            y_offset = random.randint(-5, 5)
            x1 += (x2 - x1) / num_points + x_offset
            y1 += (y2 - y1) / num_points + y_offset
            pyautogui.moveTo(x1, y1, duration = sleep_duration, tween = pyautogui.easeInOutQuad)
            
        pyautogui.moveTo(x2 + random.randint(-5, 5), y2 + random.randint(-5, 5))

    def mouse_click(self):
        """!
        @brief      Mouse click once

        """
        pyautogui.click()

    def store_money_in_guild_account(self):
        """!
        @brief      Store money into the guild account
                    Simulates a series of actions to store money into a guild account.
        """
        pyautogui.press('g')
        pyautogui.keyUp('g')  

        GUILD_ACCOUNT_BUTTON = (456, 561)
        self.mouse_move(GUILD_ACCOUNT_BUTTON)
        self.mouse_click()
        time.sleep(0.5)

        DEPOSIT_MONEY_BUTTON = (204, 476)
        self.mouse_move(DEPOSIT_MONEY_BUTTON)
        self.mouse_click()
        time.sleep(0.5)

        DRAG_MONEY_START = (789, 620)
        DRAG_MONEY_END = (1013, 621)
        self.mouse_move(DRAG_MONEY_START)
        pyautogui.mouseDown()
        self.mouse_move(DRAG_MONEY_END)
        pyautogui.mouseUp()

        CONFIRM_DEPOSIT_MONEY_BUTTON = (924, 684)
        self.mouse_move(CONFIRM_DEPOSIT_MONEY_BUTTON)
        self.mouse_click()
        time.sleep(0.5)


    def take_out_money_from_guild_account(self):
        """!
        @brief      Withdraw money from the guild account
                    Simulates a series of actions to take money out of a guild account.
        """
        pyautogui.press('g')
        pyautogui.keyUp('g')  

        GUILD_ACCOUNT_BUTTON = (456, 561)
        self.mouse_move(GUILD_ACCOUNT_BUTTON)
        self.mouse_click()
        time.sleep(0.5)

        WITHDRAW_MONEY_BUTTON = (204, 525)
        self.mouse_move(WITHDRAW_MONEY_BUTTON)
        self.mouse_click()
        time.sleep(0.5)

        DRAG_MONEY_START = (789, 620)
        DRAG_MONEY_END = (1013, 621)
        self.mouse_move(DRAG_MONEY_START)
        pyautogui.mouseDown()
        self.mouse_move(DRAG_MONEY_END)
        pyautogui.mouseUp()

        CONFIRM_WITHDRAW_MONEY_BUTTON = (924, 684)
        self.mouse_move(CONFIRM_WITHDRAW_MONEY_BUTTON)
        self.mouse_click()
        time.sleep(0.5)


    def log_out(self):
        """!
        @brief      Log out of the account
            Simulates actions to properly log out of an account.
        """
        pyautogui.press('esc')
        pyautogui.keyUp('esc')

        LOG_OUT_BUTTON = (1452, 198)
        self.mouse_move(LOG_OUT_BUTTON)
        self.mouse_click()
        time.sleep(10)


    def log_in(self, account: str):
        """!
        @brief      Log into the account
                    Simulates a series of actions to log into an account.
        
        @param      account: Account details or credentials for login.
        """
        LOG_IN_BUTTON = (765, 539)
        self.mouse_move(LOG_IN_BUTTON)
        self.mouse_click()
        time.sleep(0.5) 

        pyautogui.typewrite(account)
        time.sleep(1) 
        pyautogui.press('enter')
        pyautogui.keyUp('enter')
        time.sleep(1) 
        pyautogui.press('enter')
        pyautogui.keyUp('enter')
        time.sleep(2) 
        
        ENTER_WORLD_BUTTON = (1079, 1022)
        self.mouse_move(ENTER_WORLD_BUTTON)
        self.mouse_click()
        time.sleep(5) 


    def open_market(self):
        """!
        @brief      Open the in-game market
                    Simulates a click action to open the market.
        """
        MARKET_POSITION = (1227, 195)
        self.mouse_move(MARKET_POSITION)
        self.mouse_click()
        time.sleep(0.5) 


    def swipe_down(self):
        """!
        @brief      Swipe down in the interface
                    Simulates a swipe down action to scroll content.
        """
        x_offset = random.randint(-100, 20)
        x_offset_2 = random.randint(-100, 20)
        y_offset = random.randint(0, 200)

        SWIPE_START_POINT = (1023 + x_offset, 570 + y_offset)
        SWIPE_END_POINT = (1019 + x_offset_2, 470 + y_offset)
        self.mouse_move(SWIPE_START_POINT)
        pyautogui.mouseDown()
        self.mouse_move(SWIPE_END_POINT)
        pyautogui.mouseUp()


    def turn_page(self):
        """!
        @brief      Turn to the next page
                    Simulates a click action to turn the page in a book or interface.
        """
        TURN_PAGE_BUTTON = (837, 1028)
        self.mouse_move(TURN_PAGE_BUTTON)
        self.mouse_click()
        time.sleep(0.5) 
        

    def search_for_item(self, name:str):
        """!
        @brief      Search for an item by its name
                    Simulates typing and search actions to find an item.
        
        @param      name: Name of the item to search for.
        """
        SEARCH_BOX_POSITION = (446, 342)
        self.mouse_move(SEARCH_BOX_POSITION)
        self.mouse_click()
        time.sleep(0.3) 

        pyautogui.typewrite(name)
        time.sleep(0.5)
        pyautogui.press('enter')
        pyautogui.keyUp('enter')
        time.sleep(0.5)


    def reset_filter_settings(self):
        """!
        @brief      Reset all filter settings in the interface
                    Simulates a click action to reset all applied filters.
        """
        RESET_FILTER_BUTTON = (537, 345)
        self.mouse_move(RESET_FILTER_BUTTON)
        self.mouse_click()
        time.sleep(0.3) 


    def create_buy_order(self):
        pass
    
    def calculate_max_price(self):
        pass

    def regular_purchase(self):
        pass

    def purchase_and_create_buy_order(self):
        pass


    def current_order_invalid(self):
        pass

    def money_not_enough(self):
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



