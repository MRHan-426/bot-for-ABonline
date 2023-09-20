import cv2
import numpy as np
import pyautogui
import time
import random
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

ocr = PaddleOCR(use_angle_cls=True, lang="en")  
# # need to run only once to download and load model into memory
# print("ocr initialization success")

BUTTON_BUY = cv2.imread('image/button_buy.jpg', cv2.IMREAD_GRAYSCALE)
REACH_BOTTOM = cv2.imread('image/reach_bottom.jpg', cv2.IMREAD_GRAYSCALE)
ERROR_MESSAGE_OK_BUTTON_INVALID_ORDER = cv2.imread('image/ERROR_MESSAGE_OK_BUTTON_INVALID_ORDER.jpg', cv2.IMREAD_GRAYSCALE)
ERROR_MESSAGE_OK_BUTTON_NO_MONEY = cv2.imread('image/ERROR_MESSAGE_OK_BUTTON_NO_MONEY.jpg', cv2.IMREAD_GRAYSCALE)


MARKET_REGION = (338, 315, 927, 770)
PRICE_REGION = (920, 471, 350, 605)
BUY_COMFIRMATION_POS = (1008, 860) # 954~1050  850~880 
MINUS_SIGN_POS = (651, 708) # range 5

PRICE_TABLE = np.array([[4.0, 4.1, 4.2, 4.3],
                        [5.0, 5.1, 5.2, 5.3],
                        [6.0, 6.1, 6.2, 6.3],
                        [3, 7.0, 7.1, 8.0]])

ACCOUNT_LIST = []
with open('account.txt', 'r') as file:
    lines = file.readlines()
for line in lines[:5]:
    ACCOUNT_LIST.append(line.strip())

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
        result = ocr.ocr(self.price_region, cls=True)
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
            im_show = draw_ocr(self.price_region, boxes, txts, scores, font_path='./fonts/simfang.ttf')
            im_show = Image.fromarray(im_show)
            return np.array(im_show)
        else:
            return np.array(self.screen)
        # cv2.destroyAllWindows()
        # im_show.save('image/result.jpg')
        # cv2.imwrite("image/screen2.jpg", self.price_region)

    def buy_an_item(self):
        read_price_from_screen()

        return False
        pass



    def mouse_move(self, target, duration=0.3):
        """!
        @brief      Mouse move from position1 to position2
                    Simulate human mouse movement
        
        @param      duration: moving time
        @param      num_points: interval points between the two points
        """

        # x1, y1 = pyautogui.position()
        x2, y2 = target
        # sleep_duration = duration / num_points
        # for _ in range(num_points):
        #     x_offset = random.randint(-5, 5)
        #     y_offset = random.randint(-5, 5)
        #     x1 += (x2 - x1) / num_points + x_offset
        #     y1 += (y2 - y1) / num_points + y_offset
        #     pyautogui.moveTo(x1, y1, duration = sleep_duration, tween = pyautogui.easeInOutQuad)
            
        pyautogui.moveTo(x2 + random.randint(-5, 5), y2 + random.randint(-5, 5), duration = duration, tween = pyautogui.easeInOutQuad)


    def mouse_click(self, clicks = 1):
        """!
        @brief      Mouse click once

        """
        pyautogui.click(clicks=clicks)


    def drag_to(self, target, duration=0.3):
        """!
        @brief      Mouse move from position1 to position2
                    Simulate human mouse movement
        
        @param      duration: moving time
        @param      num_points: interval points between the two points
        """

        x2, y2 = target
        pyautogui.dragTo(x2 + random.randint(-5, 5), y2 + random.randint(-5, 5), duration = duration, tween = pyautogui.easeInOutQuad)


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
        time.sleep(0.3) 

        pyautogui.mouseDown()
        time.sleep(0.3) 

        pyautogui.mouseUp()
        time.sleep(0.3) 

        pyautogui.press('backspace')
        pyautogui.keyUp('backspace')       

        pyautogui.typewrite(account)
        time.sleep(1) 
        pyautogui.press('enter')
        pyautogui.keyUp('enter')
        time.sleep(1) 
        pyautogui.press('enter')
        pyautogui.keyUp('enter')
        time.sleep(3) 
        
        ENTER_WORLD_BUTTON = (1079, 1022)
        self.mouse_move(ENTER_WORLD_BUTTON)
        self.mouse_click()
        time.sleep(5) 


    def open_market(self):
        """!
        @brief      Open the in-game market
                    Simulates a click action to open the market.
        """
        MARKET_POSITION = (1062, 272)
        self.mouse_move(MARKET_POSITION)
        self.mouse_click()
        time.sleep(0.5) 


    def swipe_down(self):
        """!
        @brief      Swipe down in the interface
                    Simulates a swipe down action to scroll content.
        """
        x_offset = random.randint(-100, 20)
        y_offset = random.randint(0, 100)

        SWIPE_START_POINT = (1023 + x_offset, 870 + y_offset)
        SWIPE_END_POINT = (1023 + x_offset, 503 + y_offset)

        self.mouse_move(SWIPE_START_POINT)
        self.drag_to(SWIPE_END_POINT)
        time.sleep(0.5)
        # pyautogui.mouseDown()
        # self.mouse_move(SWIPE_END_POINT)
        # pyautogui.mouseUp()


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
        SEARCH_BOX_POSITION = (435, 344)
        self.mouse_move(SEARCH_BOX_POSITION)
        time.sleep(0.3) 

        pyautogui.mouseDown()
        time.sleep(0.3) 

        pyautogui.mouseUp()
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


    def regular_purchase(self, account: str):
        pBot.mouse_move((794,23))
        pBot.mouse_click()
        time.sleep(1)

        pBot.log_in(str)
        time.sleep(0.2)

        pBot.take_out_money_from_guild_account()
        time.sleep(0.2)

        open_market()
        time.sleep(0.2)

        for item in DICTIONARY_FIBER:
            pBot.search_for_item(item)
            time.sleep(0.2)

            pBot.swipe_down() # we don't buy items that remain on top of the market
            time.sleep(0.2)

            while(True):
                pBot.update_screenshot()
                success = buy_an_item()
                if success:
                    pBot.update_screenshot()

                result = cv2.matchTemplate(pBot.gray_screen, REACH_BOTTOM, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)

                if max_val >= 0.85:
                    pBot.turn_page()
                else:
                    pBot.swipe_down()

            time.sleep(0.2)




    def purchase_and_create_buy_order(self):
        pass


    def current_order_invalid(self):
        pass

    def money_not_enough(self):
        pass


if __name__ == '__main__':

    pBot = purchaseBot()
    '''
        Test
    '''
    # pBot.mouse_move((2115, 537))
    # pBot.drag_to((2115, 537))
    # pBot.reset_filter_settings()
    # pBot.search_for_item("UN HEMP")
    # pBot.reset_filter_settings()
    # pBot.turn_page()
    # for i in range(5):
    #     pBot.update_screenshot()
    #     result = cv2.matchTemplate(pBot.gray_screen, REACH_BOTTOM, cv2.TM_CCOEFF_NORMED)
    #     _, max_val, _, _ = cv2.minMaxLoc(result)
    #     if max_val >= 0.85:
    #         pBot.turn_page()
    #     else:
    #         pBot.swipe_down()

    # pyautogui.press('esc')
    # pyautogui.keyUp('esc')
    # pBot.log_out()
    pBot.mouse_move((794,23))
    pBot.mouse_click()
    time.sleep(1)
    # pBot.take_out_money_from_guild_account()
    # pBot.store_money_in_guild_account()
    
    while(True):
        # pBot.find_buy_button()
        pBot.update_screenshot()
        img = pBot.read_price_from_screen()
        cv2.imshow("Price_OCR", img)
        cv2.waitKey(500) #ms
    cv2.destroyAllWindows()



