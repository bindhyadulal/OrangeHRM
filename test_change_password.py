from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

from login_page import OrangeHRMLoginPage
from change_password import ChangePasswordPage

# Constants
default_password = "admin123"
username = "Admin"
url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

# Test Cases
test_cases = [
    {"name": "Valid_Password_Change", "current": default_password, "new": "Admin@1234", "confirm": "Admin@1234"},
    {"name": "Mismatch_Confirm", "current": "Admin@1234", "new": "Admin@1234", "confirm": "Admin@123"},
    {"name": "Too_Short", "current": "Admin@1234", "new": "Ab1@", "confirm": "Ab1@"},
    {"name": "Weak_Password", "current": "Admin@1234", "new": "password", "confirm": "password"},
    {"name": "Blank_Fields", "current": "Admin@1234", "new": "", "confirm": ""},
    {"name": "Same_As_Current", "current": "Admin@1234", "new": "Admin@1234", "confirm": "Admin@1234"},
    {"name": "Too_Long", "current": "Admin@1234", "new": "A" * 100 + "@123a", "confirm": "A" * 100 + "@123a"},
    {"name": "Only_Spaces", "current": "Admin@1234", "new": "    ", "confirm": "    "},
    {"name": "Special_Chars", "current": "Admin@1234", "new": "Ab@!#%&*()", "confirm": "Ab@!#%&*()"},
    {"name": "Reuse_Old_Password", "current": "Admin@1234", "new": default_password, "confirm": default_password},
]


def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)
    login_page = OrangeHRMLoginPage(driver)
    change_page = ChangePasswordPage(driver, wait)

    try:
        # Login once
        login_page.open_login_page()
        login_page.login(username, default_password)
        login_page.assert_dashboard_loaded()

        for case in test_cases:
            print(f"\n=== Running Test: {case['name']} ===")
            try:
                change_page.change_password(case["current"], case["new"], case["confirm"])
            except Exception as e:
                driver.save_screenshot(f"{case['name']}_error.png")
                print(f"Error during test {case['name']}: {e}")
            time.sleep(2)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
