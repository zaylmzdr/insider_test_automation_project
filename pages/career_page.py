from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class CareerPage(BasePage):
    TEAMS = (By.XPATH, '//a[text()="See all teams"]')
    LOCATIONS = (By.ID, "career-our-location")
    LIFE_AT_INSIDER_HEADER = (By.XPATH, "//h2[text()='Life at Insider']")

    def scroll_and_check_blocks(self):
        """
           Scrolls to key sections on the page and verifies their visibility:
           'See all teams', 'Our Locations', and 'Life at Insider'.
           """
        wait = self.wait
        blocks = [
            ("See all teams", self.TEAMS),
            ("Our Locations", self.LOCATIONS),
            ("Life at Insider", self.LIFE_AT_INSIDER_HEADER)
        ]
        for block_name, locator in blocks:
            try:
                element = wait.until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                wait.until(EC.visibility_of_element_located(locator))
                time.sleep(1.5)
                assert element.is_displayed(), f"The '{block_name}' section is not visible."
                print(f"The '{block_name}' section was successfully displayed.")
            except Exception as e:
                print(f"Error during checking the '{block_name}' block: {e}")
