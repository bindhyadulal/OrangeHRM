from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import time


class ChangePasswordPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open_change_password(self):
        self.wait.until(ec.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'oxd-userdropdown-tab')]"))).click()
        self.wait.until(ec.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Change Password']"))).click()
        self.wait.until(ec.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Update Password']")))
        print("Change Password page opened")

    def input_password_fields(self, current_pwd, new_pwd, confirm_pwd):
        def input_for_label(label_text):
            return self.wait.until(ec.presence_of_element_located((
                By.XPATH,
                f"//label[normalize-space()='{label_text}']/ancestor::div[contains(@class, 'oxd-input-group')]/div[2]/input"
            )))

        input_for_label("Current Password").clear()
        input_for_label("Current Password").send_keys(current_pwd)
        input_for_label("Password").clear()
        input_for_label("Password").send_keys(new_pwd)
        input_for_label("Confirm Password").clear()
        input_for_label("Confirm Password").send_keys(confirm_pwd)
        print("Password fields filled")

    def submit_change(self):
        self.wait.until(ec.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))).click()
        time.sleep(2)

    def get_toast_message(self):
        try:
            toast = self.driver.find_element(By.CLASS_NAME, "oxd-toast-content-text")
            return toast.text
        except:
            return None

    def change_password(self, current_pwd, new_pwd, confirm_pwd):
        self.open_change_password()
        self.input_password_fields(current_pwd, new_pwd, confirm_pwd)
        self.submit_change()
        message = self.get_toast_message()
        if message:
            print("Toast Message:", message)
        else:
            print("No toast message. Possibly failed silently.")
