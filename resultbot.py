# This script automates the process of checking results on a specific website using Selenium.
# It iterates through a range of roll numbers and dates of birth, submitting them to the website

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

# Settings
START_ROLL = 1234567
END_ROLL = 7654321
START_DOB = datetime.strptime("01-01-2001", "%d-%m-%Y")
END_DOB = datetime.strptime("01-02-2001", "%d-%m-%Y")

# Helper function to type text slowly
def send_keys_slowly(element, text, delay=0.01):
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

# Setup WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

for roll_num in range(START_ROLL, END_ROLL + 1):
    print(f"Trying roll number: {roll_num}")
    current_dob = START_DOB
    while current_dob <= END_DOB:
        dob_str = current_dob.strftime("%d%m%Y")  # Format: DDMMYYYY
        print(f"Trying DOB: {dob_str}")

        try:
            driver.get("https://results.digilocker.gov.in/cbse202510thzaqplmkixcseoivft.html")
            time.sleep(1)

            roll_input = driver.find_element(By.ID, "rroll")
            dob_input = driver.find_element(By.ID, "dob_input")

            send_keys_slowly(roll_input, str(roll_num))
            send_keys_slowly(dob_input, dob_str)

            submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            submit_button.click()

            time.sleep(2)

            page_source = driver.page_source
            if "The provided date of birth does not match our records." in page_source:
                print(f"→ No match for {roll_num} with DOB {dob_str}")
                current_dob += timedelta(days=1)
                continue
            else:
                print(f"✅ Result FOUND for roll number {roll_num} and DOB {dob_str}!")
                try:
                    result_container = driver.find_element(By.CSS_SELECTOR, ".result-container, .result-details, #result")
                    print("Result Details:\n", result_container.text)
                except:
                    body = driver.find_element(By.TAG_NAME, "body")
                    print("Result Details (fallback):\n", body.text[:1000])

                print("\nBrowser will remain open for manual inspection.")
                input("Press ENTER to close the browser and exit...")
                driver.quit()
                exit()

        except Exception as e:
            print(f"[ERR] Roll {roll_num}, DOB {dob_str}: {e}. Trying next DOB...")
            current_dob += timedelta(days=1)
            continue

print("Finished checking all roll numbers and DOBs.")
driver.quit()
