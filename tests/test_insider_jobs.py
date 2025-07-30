import os
from datetime import datetime
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pages.home_page import HomePage
from pages.career_page import CareerPage
from pages.jobs_page import JobsPage


class InsiderJobFilterTest(unittest.TestCase):
    """
        Test Scenario: Filter QA jobs on Insider career site and verify redirection to application form

        Test Steps:
        1. Navigate to Insider homepage
        2. Accept cookie banner if visible
        3. Navigate to the Career page and scroll to key sections
        4. Navigate directly to QA careers page
        5. Accept cookies again if needed
        6. Click on "See all QA jobs"
        7. Verify 'Quality Assurance' department is selected
        8. Open location dropdown and select 'Istanbul, Turkiye'
        9. Scroll page to ensure job cards are loaded
        10. Verify 'Istanbul' location is selected
        11. Check job cards content (position, department, location, etc.)
        12. Click on first valid 'View Role' button
        13. Verify redirection to Lever application page
        """

    def setUp(self):
        """Set up Chrome WebDriver with options before each test."""
        chrome_options = Options()
        chrome_options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.get("https://useinsider.com/")

        self.home_page = HomePage(self.driver)
        self.career_page = CareerPage(self.driver)
        self.jobs_page = JobsPage(self.driver)

    def test_insider_job_filter(self):
        """Full end-to-end test for filtering and verifying QA job listings on Insider careers."""
        self.assertIn("https://useinsider.com/", self.driver.current_url, "You are not on the Insider homepage")

        self.home_page.accept_cookie_if_visible()
        self.home_page.navigate_to_career_page_and_scroll()

        self.career_page.scroll_and_check_blocks()

        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        self.jobs_page.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        # Reuse cookie acceptance method from home_page
        self.jobs_page.accept_cookie_if_visible = self.home_page.accept_cookie_if_visible
        self.jobs_page.accept_cookie_if_visible()

        self.jobs_page.click_see_all_qa_jobs()
        self.jobs_page.accept_cookie_if_visible()

        self.jobs_page.check_department_selected()

        self.jobs_page.open_location_dropdown()
        self.jobs_page.select_istanbul_option()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        self.jobs_page.check_location_selected()
        self.jobs_page.check_job_cards_content()

        clicked = self.jobs_page.click_first_valid_view_role()
        self.assertTrue(clicked, "Failed to click the 'View Role' button.")

        self.jobs_page.wait.until(lambda d: 'lever.co' in d.current_url)
        self.assertIn("lever.co", self.driver.current_url, "Did not redirect to the Lever application form page.")
        print("Redirected to the Lever application form page successfully.")

        time.sleep(3)

    def tearDown(self):
        """Take screenshot only if test failed, then quit driver."""
        has_failure = False
        if hasattr(self, '_outcome'):
            errors = getattr(self._outcome, 'errors', None)
            if errors is None:
                result = getattr(self._outcome, 'result', None)
                if result:
                    errors = getattr(result, 'errors', None)
            if errors:
                for test, exc_info in errors:
                    if exc_info is not None:
                        has_failure = True
                        break

        if has_failure:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            test_method_name = self._testMethodName
            screenshot_path = os.path.join(screenshots_dir, f"{test_method_name}.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
