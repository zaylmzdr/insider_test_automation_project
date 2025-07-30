from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class HomePage(BasePage):
    COMPANY_MENU = (By.LINK_TEXT, 'Company')
    CAREERS_MENU = (By.LINK_TEXT, 'Careers')
    COOKIE_BUTTON = (By.ID, "wt-cli-accept-btn")

    def accept_cookie_if_visible(self, timeout=3):
        """If cookie banner appears, click to accept it; otherwise do nothing."""
        try:
            short_wait = self.wait
            cookie_button = short_wait.until(EC.element_to_be_clickable(self.COOKIE_BUTTON))
            cookie_button.click()
            print("Cookie banner closed.")
        except:
            print("Cookie banner not visible, it might already be closed.")

    def navigate_to_career_page_and_scroll(self):
        """Hover over 'Company' menu and click on 'Careers' to navigate there."""
        wait = self.wait
        company = self.driver.find_element(*self.COMPANY_MENU)
        ActionChains(self.driver).move_to_element(company).perform()
        time.sleep(1)
        self.driver.find_element(*self.CAREERS_MENU).click()
        time.sleep(2)
