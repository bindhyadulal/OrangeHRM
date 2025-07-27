from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import config


def login():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(config.URL)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(config.USERNAME)
        driver.find_element(By.NAME, "password").send_keys(config.PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for dashboard element
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))
        print(" Login successful!")

    except TimeoutException:
        print("Login failed: Dashboard did not load.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return driver


if __name__ == "__main__":
    login()
