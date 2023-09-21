import cv2
import numpy as np
import pyautogui
import time
import random
from typing import List
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang="en")  
# # need to run only once to download and load model into memory
print("ocr initialization success")

BUTTON_BUY = cv2.imread('image/button_buy.jpg', cv2.IMREAD_GRAYSCALE)
REACH_BOTTOM = cv2.imread('image/reach_bottom.jpg', cv2.IMREAD_GRAYSCALE)
ERROR_MESSAGE_OK_BUTTON_INVALID_ORDER = cv2.imread('image/ERROR_MESSAGE_OK_BUTTON_INVALID_ORDER.jpg', cv2.IMREAD_GRAYSCALE)
ERROR_MESSAGE_OK_BUTTON_NO_MONEY = cv2.imread('image/ERROR_MESSAGE_OK_BUTTON_NO_MONEY.jpg', cv2.IMREAD_GRAYSCALE)

FRACTION_WARFARE_CLOSE_BUTTON = (1143, 285)
ACTIVITIES_CLOSE_BUTTON = (1143, 285)
TWITCH_DROPS_CLOSE_BUTTON = (1266, 399)

MARKET_REGION = (338, 315, 927, 770)
BOTTOM_CHECK_REIGION = (920, 471, 350, 605)
BUY_ORDER_PRICE_REGION = (716, 723, 91, 57)
PRICE_REGION = (920, 471, 160, 605)

ACCOUNT_LIST = []
with open('account.txt', 'r') as file:
    lines = file.readlines()
for line in lines[:5]:
    ACCOUNT_LIST.append(line.strip())


PRICE_TABLE = { 'FLAX': 50, 
                'HEMP': 48, 
                'UN HEMP': 175,
                'RA HEMP': 980,
                'EXPONE HEMP': 6800,
                'SKY': 260,
                'UN SKY': 580,
                'RA SKY': 1400,
                'EX SKY': 8000,
                'AM': 745,
                'UN AM': 1170,
                'RA AM': 5800,
                'EX AM': 0,
                'SUN': 1400,
                'UN SUN': 4400,
                'GHOST H': 0
                }

BUY_ORDER_TABLE = { 'FLAX':         [50,    [9999, 6666]], # max_price, large_amount, small_amount 
                    'HEMP':         [48,    [9999, 6666]], 
                    'UN HEMP':      [175,   [7777, 5000]],
                    'RA HEMP':      [980,   [1333, 666]],
                    'EXPONE HEMP':  [6800,  [300, 150]],
                    'SKY':          [260,   [9999, 4444]],
                    'UN SKY':       [580,   [3333, 1666]],
                    'RA SKY':       [1400,  [1111, 666]],
                    'EX SKY':       [8000,  [300, 150]],
                    'AM':           [745,   [4444, 2666]],
                    'UN AM':        [1170,  [1666, 600]],
                    'RA AM':        [5800,  [300, 150]],
                    'EX AM':        [0,     [150, 50]],
                    'SUN':          [1400,  [1666, 888]],
                    'UN SUN':       [4400,  [600, 300]],
                    'GHOST H':      [0,     [450, 200]]
                }


class purchaseBot():
    def __init__(self, parent=None):
        """!
        @brief      Constructs a new instance.

        """
        self.screen = np.array(pyautogui.screenshot(region = MARKET_REGION))
        self.price_region = np.array(pyautogui.screenshot(region = PRICE_REGION))
        self.buy_order_price_region = np.array(pyautogui.screenshot(region = BUY_ORDER_PRICE_REGION))

        self.bottom_check_window = np.array(pyautogui.screenshot(region = BOTTOM_CHECK_REIGION))
        self.bottom_check_window = cv2.cvtColor(self.bottom_check_window, cv2.COLOR_BGR2GRAY)


    def find_buy_button(self):
        """!
        @brief      Use opencv template match to locate "BUY" button.

        """
        h, w = BUTTON_BUY.shape
        result = cv2.matchTemplate(self.screen, BUTTON_BUY, cv2.TM_CCOEFF_NORMED)
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
        self.buy_order_price_region = np.array(pyautogui.screenshot(region = BUY_ORDER_PRICE_REGION))

        self.bottom_check_window = np.array(pyautogui.screenshot(region = BOTTOM_CHECK_REIGION))
        self.bottom_check_window = cv2.cvtColor(self.bottom_check_window, cv2.COLOR_BGR2GRAY)


    def read_price_from_screen(self, region: tuple):
        """!
        @brief      Use paddle ocr to get the prices.

        """
        result = ocr.ocr(region, cls=True)
        result = result[0]
        return result

        # if result != None:
        #     boxes = [line[0] for line in result]
        #     txts = [line[1][0] for line in result]
        #     scores = [line[1][1] for line in result]

        #     im_show = draw_ocr(region, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        #     im_show = Image.fromarray(im_show)
        #     return np.array(im_show)
        # else:
        #     return np.array(self.screen)


    def buy_an_item(self, max_price: int):
        """!
        @brief      Buy an item that is below the max price.
                    If buy successfully, return true.

        """
        result = self.read_price_from_screen(region = self.price_region)
        if result == None:
            print("Unpredictable ERROR Occurs, please report")
            return False, result
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        boxes = [line[0] for line in result]
        for i in range(len(txts)):
            if  scores[i] >= 0.98:
                price = int(txts[i].replace(',', ''))
                if  price <= max_price:
                    buy_button_position = (int(boxes[i][0][0] + PRICE_REGION[0] + 216), int(boxes[i][0][1] + PRICE_REGION[1] + 14))
                    # print(buy_button_position)
                    self.mouse_move(buy_button_position)
                    time.sleep(0.2)
                    self.mouse_click()
                    self.mouse_move((1011, 860), duration=0.15)
                    time.sleep(0.2)
                    self.mouse_click()
                    time.sleep(0.1)
                    return True, result
                else:
                    return False, result
            else:
                pass

        return False, result


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
        time.sleep(5) 
        
        ENTER_WORLD_BUTTON = (1079, 1022)
        self.mouse_move(ENTER_WORLD_BUTTON)
        self.mouse_click()
        time.sleep(8) 


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
        self.reset_filter_settings()
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


    def regular_purchase(self, account: str):
        self.mouse_move((794,23))
        self.mouse_click()
        time.sleep(1)

        self.log_in(account)
        time.sleep(0.2)

        self.take_out_money_from_guild_account()
        time.sleep(0.2)

        self.open_market()
        time.sleep(0.2)

        for item in PRICE_TABLE.keys():
            self.search_for_item(item)
            time.sleep(0.5)

            self.swipe_down() # we don't buy items that remain on top of the market
            time.sleep(0.2)

            fail_count = 0

            while True:
                self.update_screenshot()
                success, result = self.buy_an_item(max_price=PRICE_TABLE[item])
                
                if success:
                    self.update_screenshot()

                    result = cv2.matchTemplate(self.bottom_check_window, REACH_BOTTOM, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)

                    if max_val >= 0.85:
                        self.turn_page()
                    else:
                        pass
                else:
                    fail_count += 1
                    if fail_count == 2:
                        break
                    self.swipe_down()

            time.sleep(0.2)
        self.store_money_in_guild_account()
        time.sleep(0.3)
        pyautogui.press('esc')
        pyautogui.keyUp('esc')
        self.log_out()
        time.sleep(0.2)
        print("Regular Purchase routine Finish")


    def create_buy_order(self, amount: List[int], max_price: int):
        BUY_ORDER_BUTTON_POSITION = (650, 644)
        self.mouse_move(BUY_ORDER_BUTTON_POSITION)
        time.sleep(0.2)
        self.mouse_click()
        self.update_screenshot()
        time.sleep(0.2)
        result = self.read_price_from_screen(region = self.buy_order_price_region)
        if result == None:
            print("Unpredictable ERROR Occurs, please report RESULT == NONE")
            return False
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        boxes = [line[0] for line in result]
        if len(txts) > 1:
            print("Unpredictable ERROR Occurs, please report TXTS > 1")
            return False
        price = int(txts[0].replace(',', ''))

        # price range
        if  price >= max_price:
            self.mouse_move((1070, 387))
            time.sleep(0.2)
            self.mouse_click()
            time.sleep(0.2)
            return False

        elif  price < max_price * 0.925:
            SET_BUY_ORDER_AMOUNT = (665, 684)
            self.mouse_move(SET_BUY_ORDER_AMOUNT)
            time.sleep(0.2)
            pyautogui.mouseDown()
            time.sleep(0.3) 
            pyautogui.mouseUp()
            pyautogui.typewrite(str(amount[0]))
            time.sleep(0.5)

            SET_BUY_ORDER_PRICE = (720, 747)
            self.mouse_move(SET_BUY_ORDER_PRICE)
            time.sleep(0.2)
            pyautogui.mouseDown()
            time.sleep(0.3) 
            pyautogui.mouseUp()
            pyautogui.typewrite(str(int(max_price * 0.90) + 1))
            time.sleep(0.5)
            
        elif price < max_price * 0.975 and price >= max_price * 0.925:
            SET_BUY_ORDER_AMOUNT = (665, 684)
            self.mouse_move(SET_BUY_ORDER_AMOUNT)
            time.sleep(0.2)
            pyautogui.mouseDown()
            time.sleep(0.3) 
            pyautogui.mouseUp()
            pyautogui.typewrite(str(amount[0]))
            time.sleep(0.5)

            PRICE_ADD_BUTTON_POSITION = (983, 749)
            self.mouse_move(PRICE_ADD_BUTTON_POSITION)
            time.sleep(0.2)
            self.mouse_click()
            time.sleep(0.2)

        elif price < max_price and price >= max_price * 0.975:
            SET_BUY_ORDER_AMOUNT = (665, 684)
            self.mouse_move(SET_BUY_ORDER_AMOUNT)
            time.sleep(0.2)
            pyautogui.mouseDown()
            time.sleep(0.3) 
            pyautogui.mouseUp()
            pyautogui.typewrite(str(amount[1]))
            time.sleep(0.5)

            PRICE_ADD_BUTTON_POSITION = (983, 749)
            self.mouse_move(PRICE_ADD_BUTTON_POSITION)
            time.sleep(0.2)
            self.mouse_click()
            time.sleep(0.2)

        CREATE_BUY_ORDER_BUTTON_POSITION = (1011, 860)
        self.mouse_move(CREATE_BUY_ORDER_BUTTON_POSITION)
        time.sleep(0.2)
        self.mouse_click()
        time.sleep(0.2)

        YES_BUTTON_POSITION_1 = (629, 644)
        YES_BUTTON_POSITION_2 = (629, 654)
        YES_BUTTON_POSITION_3 = (629, 664)
        YES_BUTTON_POSITION_4 = (629, 674)

        self.mouse_move(YES_BUTTON_POSITION_1)
        time.sleep(0.2)
        self.mouse_click()
        time.sleep(0.2)

        self.mouse_move(YES_BUTTON_POSITION_2)
        time.sleep(0.2)
        self.mouse_click()
        time.sleep(0.2)

        self.mouse_move(YES_BUTTON_POSITION_3)
        time.sleep(0.2)
        self.mouse_click()
        time.sleep(0.2)

        self.mouse_move(YES_BUTTON_POSITION_4)
        time.sleep(0.2)
        self.mouse_click()
        time.sleep(0.2)

        return True


    def purchase_and_create_buy_order(self, account:str):
        self.mouse_move((794,23))
        self.mouse_click()
        time.sleep(1)

        self.log_in(account)
        time.sleep(0.2)

        self.take_out_money_from_guild_account()
        time.sleep(0.2)

        self.open_market()
        time.sleep(0.2)

        for item in BUY_ORDER_TABLE.keys():
            self.search_for_item(item)
            time.sleep(0.5)

            self.swipe_down() # we don't buy items that remain on top of the market
            time.sleep(0.2)

            while True:
                self.update_screenshot()
                success, result = self.buy_an_item(max_price= BUY_ORDER_TABLE[item][0])
                self.update_screenshot()
                
                if success:
                    result = cv2.matchTemplate(self.bottom_check_window, REACH_BOTTOM, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)

                    if max_val >= 0.85:
                        self.turn_page()
                    else:
                        pass
                else:
                    if result != None:
                        boxes = [line[0] for line in result]
                        buy_button_position = (int(boxes[0][0][0] + PRICE_REGION[0] + 216), int(boxes[0][0][1] + PRICE_REGION[1] + 14))
                        self.mouse_move(buy_button_position)
                        time.sleep(0.2)
                        self.mouse_click()
                        time.sleep(0.2)
                        buyorder_success = self.create_buy_order(BUY_ORDER_TABLE[item][1], BUY_ORDER_TABLE[item][0])
                        break
                    else:
                        break

            time.sleep(0.2)
        self.store_money_in_guild_account()
        time.sleep(0.3)
        pyautogui.press('esc')
        pyautogui.keyUp('esc')
        self.log_out()
        time.sleep(0.2)
        print("Regular Purchase routine Finish")


    def current_order_invalid(self):
        pass

    def money_not_enough(self):
        pass


if __name__ == '__main__':

    pBot = purchaseBot()
    '''
        Test
    '''

    pBot.mouse_move((794,23))
    pBot.mouse_click()
    time.sleep(1)
    for i in ACCOUNT_LIST:
        print(i)
        # pBot.regular_purchase(i)
        pBot.purchase_and_create_buy_order(i)

        time.sleep(3)


    # while(True):
    #     # pBot.find_buy_button()
    #     pBot.update_screenshot()
    #     img = pBot.read_price_from_screen(pBot.buy_order_price_region)
    #     cv2.imshow("Price_OCR", img)
    #     cv2.waitKey(500) #ms
    # cv2.destroyAllWindows()
