from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

def login(driver):
    driver.get(config.URL)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(config.USERNAME)
        driver.find_element(By.NAME, "password").send_keys(config.PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))
        print("Login successful.")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def visit_my_info(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='My Info']/parent::a"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h6[text()='Personal Details']"))
        )
        print("My Info page loaded successfully.")
    except Exception as e:
        print(f"Failed to load My Info page: {e}")

def visit_leave(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Leave']/parent::a"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h5[text()='Leave List']"))
        )
        print(".Leave page loaded successfully.")
    except Exception as e:
        print(f".Failed to load Leave page: {e}")

def visit_pim(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']/parent::a"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h5[text()='Employee Information']"))
        )
        print(".PIM page loaded successfully.")
    except Exception as e:
        print(f".Failed to load PIM page: {e}")

def visit_performance(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Performance']/parent::a"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h6[text()='Performance']"))
        )
        print(".Performance page loaded successfully.")
    except Exception as e:
        print(f".Failed to load Performance page: {e}")


def logout(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='oxd-userdropdown-tab']"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        print(".Logout successful. Returned to login page.")
    except Exception as e:
        print(f".Logout failed: {e}")

def run_full_test():
    driver = webdriver.Chrome()
    driver.maximize_window()

    if login(driver):
        visit_my_info(driver)
        visit_leave(driver)
        visit_pim(driver)
        visit_performance(driver)
        logout(driver)

    driver.quit()

if __name__ == "__main__":
    run_full_test()
