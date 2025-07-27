from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def test_logout():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(config.URL)

    # Login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(config.USERNAME)
    driver.find_element(By.NAME, "password").send_keys(config.PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    try:
        # Wait for Dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
        )

        # Click profile icon
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='oxd-userdropdown-tab']"))
        ).click()

        # Click logout button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']"))
        ).click()

        # Wait for login page to reappear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        print("Logout successful. Returned to login page.")
    except Exception as e:
        print(f"Logout failed: {e}")

    driver.quit()

if __name__ == "__main__":
    test_logout()
