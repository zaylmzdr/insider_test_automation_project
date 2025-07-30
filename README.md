# Insider QA Jobs Test Automation Project

## Overview
This project automates the validation of the Insider website’s homepage, navigation, and Quality Assurance (QA) job listings.  
It verifies that job listings filtered by location and department display correctly and that the “View Role” button redirects users to the appropriate application form.

---

## Test Scope

1. Verify Insider homepage loads successfully at [https://useinsider.com/](https://useinsider.com/).  
2. Navigate from homepage to Careers page via the “Company” menu.  
3. Verify visibility of key sections on the Careers page: Locations, Teams, Life at Insider.  
4. Navigate to the Quality Assurance careers page and:  
   - Click “See all QA jobs”.  
   - Filter jobs by Location: Istanbul, Turkiye and Department: Quality Assurance.  
   - Verify filtered job listings appear.  
5. For each job listing:  
   - Confirm the Position title contains “Quality Assurance”.  
   - Confirm the Department is “Quality Assurance”.  
   - Confirm the Location is “Istanbul, Turkiye”.  
6. Click “View Role” on a valid job and verify redirection to the Lever application form (URL contains “lever.co”).

---

## Technologies & Tools

- **Programming Language:** Python 3.12  
- **Automation Tool:** Selenium WebDriver  
- **Test Framework:** unittest (Python standard library)  
- **Design Pattern:** Page Object Model (POM)  
- **Browser:** Google Chrome (with matching ChromeDriver)

---

## Project Structure

- **/pages/**           Page Object Model (POM) classes (BasePage, HomePage, CareerPage, JobsPage)  
- **/tests/**           Test scripts and test cases  
- **/screenshots/**     Automatically saved screenshots of test failures  
- **README.md**         Project documentation file
