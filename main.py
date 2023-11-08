import time
import configparser
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize the configuration parser
config = configparser.ConfigParser()
config.read('config.ini')

# Read credentials from the INI file
ACCOUNT_EMAIL = config.get('LinkedIn', 'ACCOUNT_EMAIL')
ACCOUNT_PASSWORD = config.get('LinkedIn', 'ACCOUNT_PASSWORD')
MY_PHONE = config.get('LinkedIn', 'MY_PHONE')

def abort_application():
    # Click Close Button
    try:
        close_down_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        close_down_button.click()

        time.sleep(2)
        # Click Discard Button
        discard_button = driver.find_elements(by=By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[0]
        discard_button.click()
    except:
        pass


chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome()

# Navigate to the website
driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=3758770878&f_AL=true&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")
time.sleep(2)
sign_in_button = driver.find_element(By.XPATH, '/html/body/div[4]/a[1]')
sign_in_button.click()

time.sleep(5)
email = driver.find_element(By.XPATH, '//*[@id="username"]')
email.send_keys(ACCOUNT_EMAIL)
password = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[2]/input')
password.send_keys(ACCOUNT_PASSWORD)
password.send_keys(Keys.ENTER)

# Get Listings
time.sleep(5)
all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")

# Apply for Jobs
for listing in all_listings:
    print("Opening Listing")
    listing.click()
    time.sleep(3)
    try:
        # Click Apply Button
        apply_button = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-s-apply button")
        apply_button.click()

        # Check the Submit Button
        submit_button = driver.find_element(by=By.CSS_SELECTOR, value="footer div button")
        if submit_button.get_attribute("aria-label") == "Continue to next step":
            abort_application()
            print("Complex application, skipped.")
            continue
        else:
            # Click Submit Button
            print("Submitting job application")
            submit_button.click()

        time.sleep(2)
        # Click Close Button
        close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        close_button.click()

    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()