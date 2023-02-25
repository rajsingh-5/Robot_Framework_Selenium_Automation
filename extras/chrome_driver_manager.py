from robot.api.deco import keyword
from webdriver_manager.chrome import ChromeDriverManager


@keyword
def get_chrome_driver():
    driver_path = ChromeDriverManager().install()
    print(driver_path)
    return driver_path


get_chrome_driver()


