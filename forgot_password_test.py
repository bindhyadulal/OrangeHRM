from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def forgot_password():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(config.URL)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, 'orangehrm-login-forgot-header')]"))
        ).click()
        print("Forgot Password page opened successfully.")
    except Exception as e:
        print(f"Failed to open Forgot Password page: {e}")
        driver.quit()
        return

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(config.USERNAME)

        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for either confirmation or redirection
        WebDriverWait(driver, 10).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'Reset Password link sent successfully')]")),
                EC.presence_of_element_located((By.XPATH, "//p[contains(@class,'oxd-text--p')]"))  # fallback
            )
        )
        print("Password reset instructions sent successfully.")

    except Exception as e:
        print(f"Failed to send password reset instructions: {e}")

    driver.quit()

if __name__ == "__main__":
    forgot_password()


