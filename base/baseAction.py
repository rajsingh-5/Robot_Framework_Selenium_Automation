import datetime
import inspect
import io
import os
import time
import pyautogui
from PIL import Image
from PIL import ImageDraw
from robot.api.deco import keyword
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from robot.api import logger
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec


class baseAction:

    def __init__(self):
        self.driver = None

    @staticmethod
    def alert_page_screenshot(action_name):
        try:
            currentTime = baseAction.current_time()
            time.sleep(2)
            path = os.path.join(os.getcwd(), 'logs', f'image_{action_name}_{currentTime}.jpeg')
            img = pyautogui.screenshot()
            img.save(path, format="JPEG", quality=75)
            logger.info(f"<br><img src='{path}' width=800px><br>", html=True)
        except Exception as e:
            logger.info('in alert_page_screenshot', html=True)
            raise e

    @keyword
    def open_browser(self, browser_name):
        baseAction.createLogdir()
        if browser_name.lower() == 'chrome':
            chrome_option = Options()
            chrome_option.add_argument("--start-maximized")
            chrome_option.add_argument("disable-popup-blocking")
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_option)
        elif browser_name == 'firefox':
            self.driver = webdriver.Firefox(GeckoDriverManager().install())

    @keyword
    def close_browser(self):
        try:
            self.driver.quit()
        except Exception as e:
            logger.info('Close Browser Failed', html=True)
            raise e

    @keyword
    def close_window(self):
        try:
            self.driver.close()
        except Exception as e:
            logger.info('Close Window Failed', html=True)
            raise e

    @keyword
    def go_to_url(self, url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(30)
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
        except Exception as e:
            logger.info('in go_to_url', html=True)
            raise e

    @keyword
    def click(self, locator, hover=False):
        try:
            element_wait = baseAction.get_locators_for_wait(locator)
            WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((element_wait)))
            element = baseAction.get_locators(self, locator)
            location = element.location
            size = element.size
            if hover:
                action = ActionChains(self.driver)
                baseAction.attach_screenshot_draw(self, inspect.stack()[0][3], location, size)
                action.move_to_element(element).click().perform()
            else:
                baseAction.attach_screenshot_draw(self, inspect.stack()[0][3], location, size)
                element.click()
        except Exception as e:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            logger.info('Click Failed', html=True)
            raise e

    @keyword
    def scroll_to_element(self, locator):
        try:
            element = baseAction.get_locators(self, locator)
            location = element.location
            size = element.size
            ActionChains(self.driver).scroll_to_element(element).perform()
            baseAction.attach_screenshot_draw(self, inspect.stack()[0][3], location, size)
        except Exception as e:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            logger.info('in click', html=True)
            raise e

    @keyword
    def scroll_down(self, value):
        try:
            if not value.isnumeric():
                if value.lower() == "full":
                    self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            else:
                self.driver.execute_script(f"window.scrollTo(0,{int(value)})")
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
        except Exception as e:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            logger.info('in scroll_to_element', html=True)
            raise e

    @keyword
    def scroll_up(self, value):
        try:
            if not value.isnumeric():
                if value.lower() == "full":
                    self.driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
            else:
                self.driver.execute_script(f"window.scrollTo({int(value)}, 0)")
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
        except Exception as e:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            logger.info('in scroll_to_element', html=True)
            raise e

    @keyword
    def verify(self, locator, actual_text):
        element = baseAction.get_locators(self, locator)
        try:
            element_wait = baseAction.get_locators_for_wait(locator)
            WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((element_wait)))
            location = element.location
            size = element.size
            assert element.text == actual_text
            baseAction.attach_screenshot_draw(self, inspect.stack()[0][3], location, size)
            logger.info(f'Assertion error expected text "{element.text}" is equal to actual text "{actual_text}"',
                        html=True)
        except Exception as e:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            logger.info('Verification Failed', html=True)
            logger.error(f'Assertion error expected text "{element.text}" is not equal to actual text "{actual_text}"',
                         html=True)
            raise e

    # @keyword
    # def wait_for_element(self, locator):
    #     try:
    #         element = baseAction.get_locators_for_wait(self, locator)
    #         WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((element)))
    #         baseAction.attach_screenshot(self, inspect.stack()[0][3])
    #     except Exception as e:
    #         baseAction.attach_screenshot(self, inspect.stack()[0][3])
    #         logger.info('in wait_for_element', html=True)
    #         raise e

    @keyword
    def send_Keys(self, locator, value):
        try:
            element_wait = baseAction.get_locators_for_wait(locator)
            WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((element_wait)))
            element = baseAction.get_locators(self, locator)
            element.clear()
            location = element.location
            size = element.size
            baseAction.attach_screenshot_draw(self, inspect.stack()[0][3], location, size)
            element.send_keys(value)
        except Exception as e:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            logger.info('Send Keys Failed', html=True)
            raise e

    @keyword
    def press_key(self, locator, key):
        try:
            # baseAction.attach_screenshot(self, 'press_keys')
            element = baseAction.get_locators(self, locator)
            location = element.location
            size = element.size
            baseAction.attach_screenshot_draw(self, inspect.stack()[0][3], location, size)
            if key.lower() == 'enter':
                element.send_keys(Keys.ENTER)
            elif key.lower() == 'tab':
                element.send_keys(Keys.TAB)
        except Exception as e:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            logger.info('Press Key Failed', html=True)
            raise e

    @keyword
    def click_With_Coordinates(self, x, y):
        try:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            actionChains = ActionChains(self.driver)
            actionChains.move_by_offset(x, y).click().perform()
        except Exception as e:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            logger.info('Click_With_Coordinates Failed', html=True)
            raise e

    @keyword
    def switch_window(self, position):
        try:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            self.driver.switch_to.window(self.driver.window_handles[position])
        except Exception as e:
            baseAction.attach_screenshot(self, inspect.stack()[0][3])
            logger.info('Switch Window Failed', html=True)
            raise e

    @keyword
    def handle_alert(self, action, value=None):
        try:
            WebDriverWait(self.driver, 20).until(ec.alert_is_present())
            element = self.driver.switch_to.alert
            if action.lower() == 'accept':
                baseAction.alert_page_screenshot('handle_alert')
                element.accept()
            elif action.lower() == 'dismiss':
                element.dismiss()
                baseAction.alert_page_screenshot('handle_alert')
            elif action.lower() == 'sendkeys':
                element.send_keys(value)
                baseAction.alert_page_screenshot('handle_alert')
        except Exception as e:
            baseAction.alert_page_screenshot('handle_alert_failure')
            logger.info('Handle Alert Failed', html=True)
            raise e

    # @keyword
    # def sendKeys_for_frame(self, locator, value):
    #     print('192')
    #     counts = self.driver.find_elements(By.XPATH, '//frame' or '//iframe')
    #     counts = len(counts)
    #     print('194')
    #     for count in range(0, counts):
    #         self.driver.switch_to.frame(count)
    #         try:
    #             print('199')
    #             element = baseAction.get_locators(self, locator)
    #             element.clear()
    #             print('201')
    #             location = element.location
    #             size = element.size
    #             baseAction.attach_screenshot_draw(self, inspect.stack()[0][3], location, size)
    #             element.send_keys(value)
    #             print('205')
    #         except Exception as e:
    #             logger.info('first for loop')
    #             raise e
    #         counts1 = self.driver.find_elements(By.XPATH, '//frame || //iframe')
    #         counts1 = len(counts1)
    #         for count1 in range(0, counts1):
    #             self.driver.switch_to.frame(count1)
    #             try:
    #                 element = baseAction.get_locators(self, locator)
    #                 element.clear()
    #                 location = element.location
    #                 size = element.size
    #                 baseAction.attach_screenshot_draw(self, inspect.stack()[0][3], location, size)
    #                 element.send_keys(value)
    #             except Exception as e:
    #                 logger.info('first for loop')
    #                 raise e

    @keyword
    def handle_frame(self, index1=None, index2=None, index3=None):
        try:
            if index1.isnumeric():
                if index1 is not None:
                    self.driver.switch_to.frame(int(index1))
                    if index2 is not None:
                        self.driver.switch_to.frame(int(index2))
                        if index3 is not None:
                            self.driver.switch_to.frame(int(index3))
            else:
                if index1.lower() == 'parent':
                    self.driver.switch_to.parent_frame()
                elif index1.lower() == 'default':
                    self.driver.switch_to.default_content()
            baseAction.attach_screenshot(self, 'handle_frame')
        except Exception as e:
            baseAction.attach_screenshot(self, 'handle_frame_failure')
            logger.info('Handle Frame Failed', html=True)
            raise e

    def get_locators(self, locator):
        try:
            if '|' in locator:
                locatorBy, locatorStr = locator.split('|')
                if locatorBy.lower() == 'id':
                    return self.driver.find_element(By.ID, locatorStr)
                elif locatorBy.lower() == 'name':
                    return self.driver.find_element(By.NAME, locatorStr)
                elif locatorBy.lower() == 'class':
                    return self.driver.find_element(By.CLASS_NAME, locatorStr)
                elif locatorBy.lower() == 'css':
                    return self.driver.find_element(By.CSS_SELECTOR, locatorStr)
                elif locatorBy.lower() == 'link':
                    return self.driver.find_element(By.LINK_TEXT, locatorStr)
                elif locatorBy.lower() == 'partial':
                    return self.driver.find_element(By.PARTIAL_LINK_TEXT, locatorStr)
                elif locatorBy.lower() == 'xpath':
                    return self.driver.find_element(By.XPATH, locatorStr)
        except Exception as e:
            logger.info('in get_locators', html=True)
            raise e

    @staticmethod
    def get_locators_for_wait(locator):
        try:
            if '|' in locator:
                locatorBy, locatorStr = locator.split('|')
                if locatorBy.lower() == 'id':
                    element = By.ID, locatorStr
                    return element
                elif locatorBy.lower() == 'xpath':
                    element = By.XPATH, locatorStr
                    return element
                elif locatorBy.lower() == 'name':
                    element = By.NAME, locatorStr
                    return element
                elif locatorBy.lower() == 'class':
                    element = By.CLASS_NAME, locatorStr
                    return element
                elif locatorBy.lower() == 'css':
                    element = By.CSS_SELECTOR, locatorStr
                    return element
                elif locatorBy.lower() == 'link':
                    element = By.LINK_TEXT, locatorStr
                    return element
                elif locatorBy.lower() == 'partial':
                    element = By.PARTIAL_LINK_TEXT, locatorStr
                    return element
        except Exception as e:
            logger.info('in get_locators_for_wait', html=True)
            raise e

    def attach_screenshot(self, action_name):
        try:
            currentTime = baseAction.current_time()
            path = os.path.join(os.getcwd(), 'logs', f'image_{action_name}_{currentTime}.jpeg')
            screenshot = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            image = image.convert("RGB")
            image.save(path, format="JPEG", quality=30)
            logger.info(f"<br><img src='{path}' width=800px><br>", html=True)
        except Exception as e:
            logger.info('in attach_screenshot', html=True)
            raise e

    def attach_screenshot_draw(self, action_name, location, size):
        try:
            now = datetime.datetime.now()
            currentTime = now.strftime("%d_%m_%y_%H_%M_%S")
            path = os.path.join(os.getcwd(), 'logs', f'image_{action_name}_{currentTime}.jpeg')
            screenshot = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            draw = ImageDraw.Draw(image)
            draw.rectangle((left, top, right, bottom), outline="red")
            image = image.convert("RGB")
            image.save(path, format="JPEG", quality=30)
            logger.info(f"<br><img src='{path}' width=800px><br>", html=True)
        except Exception as e:
            logger.info('in attach_screenshot_draw', html=True)
            raise e

    @staticmethod
    def current_time():
        now = datetime.datetime.now()
        currentTime = now.strftime("%d_%m_%y_%H_%M_%S")
        return currentTime

    @staticmethod
    def createLogdir():
        try:
            path = os.path.join(os.getcwd(), 'logs')
            isExist = os.path.exists(path)
            if not isExist:
                os.mkdir(path)
        except Exception as e:
            print(e)