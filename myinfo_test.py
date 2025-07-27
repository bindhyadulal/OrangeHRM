from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def test_my_info():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(config.URL)

    # Login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(config.USERNAME)
    driver.find_element(By.NAME, "password").send_keys(config.PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    try:
        # Wait for dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
        )

        # Click on "My Info" in sidebar
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/web/index.php/pim/viewMyDetails']"))
        ).click()

        # Confirm My Info page loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h6[text()='Personal Details']"))
        )

        print("My Info page loaded successfully.")
    except Exception as e:
        print(f"Failed to load My Info page: {e}")

    driver.quit()

if __name__ == "__main__":
    test_my_info()
