from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.color import Color
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from pages.base_page import BasePage
import time

class JobsPage(BasePage):
    SEE_ALL_JOBS = (By.LINK_TEXT, "See all QA jobs")
    LOCATION_DROPDOWN = (By.CSS_SELECTOR, "span#select2-filter-by-location-container")
    DEPARTMENT_DROPDOWN = (By.CSS_SELECTOR, "span#select2-filter-by-department-container")
    LOCATION_OPTIONS = (By.CSS_SELECTOR, "ul.select2-results__options li.select2-results__option")
    JOB_CARDS = (By.CLASS_NAME, "position-list-item")
    POSITION_TITLE = (By.CLASS_NAME, "position-title")
    POSITION_DEPARTMENT = (By.CLASS_NAME, "position-department")
    POSITION_LOCATION = (By.CLASS_NAME, "position-location")
    VIEW_ROLE_BUTTON = (By.XPATH, ".//a[contains(text(), 'View Role')]")

    def click_see_all_qa_jobs(self):
        """Scrolls to and clicks the 'See all QA jobs' button."""
        wait = self.wait
        see_all_jobs = wait.until(EC.element_to_be_clickable(self.SEE_ALL_JOBS))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", see_all_jobs)
        see_all_jobs.click()
        print("'See all QA jobs' button clicked.")

    def check_department_selected(self):
        """Waits until 'Quality Assurance' is shown as the selected department."""
        wait = self.wait
        wait.until(EC.text_to_be_present_in_element(self.DEPARTMENT_DROPDOWN, "Quality Assurance"))

    def open_location_dropdown(self):
        """Waits for and clicks to open the location dropdown menu."""
        wait = self.wait
        location_dropdown = wait.until(EC.element_to_be_clickable(self.LOCATION_DROPDOWN))
        location_dropdown.click()
        print("Location dropdown opened.")

    def select_istanbul_option(self):
        """Selects the 'Istanbul' option from the location dropdown."""
        wait = self.wait
        wait.until(lambda d: len(d.find_elements(*self.LOCATION_OPTIONS)) > 1)
        location_options = self.driver.find_elements(*self.LOCATION_OPTIONS)
        istanbul_option = next((opt for opt in location_options if "Istanbul" in opt.text), None)
        assert istanbul_option is not None, "Istanbul option not found in dropdown."
        istanbul_option.click()
        print("Istanbul, Turkiye selected.")
        time.sleep(3)

    def check_location_selected(self):
        """Verifies that 'Istanbul, Turkiye' is the currently selected location in the dropdown."""
        selected_location_text = self.driver.find_element(*self.LOCATION_DROPDOWN).text
        assert "Istanbul, Turkiye" in selected_location_text, "Selected location in dropdown is not Istanbul."
        print("Istanbul location is shown as selected in dropdown.")

    def check_jobs_loaded(self):
        """Waits for job listings to load and asserts at least one is present."""
        wait = self.wait
        job_cards = wait.until(EC.visibility_of_all_elements_located(self.JOB_CARDS))
        assert len(job_cards) > 0, "No job listings found."
        print(f"{len(job_cards)} job listings found.")
        return job_cards

    def check_job_cards_content(self):
        """
            Verifies that each visible job card contains 'Quality Assurance'
            in the position and department fields, and that the location is 'Istanbul, Turkiye'.
            Skips stale elements if they occur during iteration.
            """
        job_cards = self.check_jobs_loaded()
        wait = self.wait
        for i in range(len(job_cards)):
            try:
                job_cards = wait.until(EC.visibility_of_all_elements_located(self.JOB_CARDS))
                card = job_cards[i]
                self.driver.execute_script("arguments[0].scrollIntoView();", card)
                time.sleep(0.5)
                position = card.find_element(self.POSITION_TITLE[0], self.POSITION_TITLE[1]).text
                department = card.find_element(self.POSITION_DEPARTMENT[0], self.POSITION_DEPARTMENT[1]).text
                location = card.find_element(self.POSITION_LOCATION[0], self.POSITION_LOCATION[1]).text

                assert "Quality Assurance" in position, f"'Quality Assurance' not found in position: {position}"
                assert "Quality Assurance" in department, f"'Quality Assurance' not found in department: {department}"
                assert location == "Istanbul, Turkiye", f"Location is not 'Istanbul, Turkiye': {location}"
            except StaleElementReferenceException:
                print(f"Job listing {i} became stale, skipping.")
                continue

    def click_first_valid_view_role(self):
        """
           Iterates through job cards, hovers over each to check if the title color changes (indicating it is active),
           then clicks the 'View Role' button on the first active job card and switches to the new window.
           Returns True if a job role is successfully opened, otherwise False.
           """
        wait = self.wait
        job_cards = self.check_jobs_loaded()
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        for i in range(len(job_cards)):
            try:
                job_cards = wait.until(EC.visibility_of_all_elements_located(self.JOB_CARDS))
                job = job_cards[i]
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job)
                time.sleep(1)
                ActionChains(self.driver).move_to_element(job).perform()
                time.sleep(1)

                title_element = job.find_element(self.POSITION_TITLE[0], self.POSITION_TITLE[1])
                title_color_hex = Color.from_string(title_element.value_of_css_property("color")).hex
                print(f"Title color after hover: {title_color_hex}")

                if title_color_hex.lower() != "#000000":
                    print("Hover successful, title color is not black.")
                    view_button = wait.until(EC.element_to_be_clickable(job.find_element(*self.VIEW_ROLE_BUTTON)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_button)
                    time.sleep(0.5)
                    view_button.click()
                    print("'View Role' button clicked.")
                    wait.until(lambda d: len(d.window_handles) > 1)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    return True
                else:
                    print("Title color still black after hover, skipping.")
            except Exception as e:
                print(f"Failed to process job listing: {e}")
        return False
