from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class OrangeHRMPIMTest:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        self.base_url = "https://opensource-demo.orangehrmlive.com/web/index.php"

    def login(self, username="Admin", password="admin123"):
        self.driver.get(f"{self.base_url}/auth/login")
        self.driver.maximize_window()

        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        dashboard_header = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))
        assert dashboard_header.is_displayed(), "Dashboard header not displayed"
        print("✅ Login successful")

    def navigate_to_pim_menu(self):
        pim_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']")))
        pim_menu.click()

        # Wait for PIM page header to ensure page loaded
        pim_header = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Employee Information']")))
        assert pim_header.is_displayed(), "PIM Employee Information header not displayed"
        print("✅ Navigated to PIM main page")

    def check_pim_menu_options(self):
        # Define menu options to check
        pim_options = {
            "Employee List": (By.XPATH, "//a[contains(@href, 'pim/viewEmployeeList')]//span[text()='Employee List']"),
            "Add Employee": (By.XPATH, "//a[contains(@href, 'pim/addEmployee')]//span[text()='Add Employee']"),
            "Reports": (By.XPATH, "//a[contains(@href, 'pim/viewReports')]//span[text()='Reports']"),
            "Configuration": (By.XPATH, "//a[contains(@href, 'pim/viewSettings')]//span[text()='Configuration']")
        }

        for name, locator in pim_options.items():
            element = self.wait.until(EC.presence_of_element_located(locator))
            assert element.is_displayed(), f"{name} menu option not displayed"
            assert element.is_enabled(), f"{name} menu option not enabled"
            print(f"✅ {name} menu option is visible and enabled")

    def navigate_to_employee_list(self):
        # Click on Employee List menu option
        employee_list = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'pim/viewEmployeeList')]//span[text()='Employee List']")))
        employee_list.click()

        # Wait for Employee List header
        emp_list_header = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Employee Information']")))
        assert emp_list_header.is_displayed(), "Employee Information header not visible"
        print("✅ Navigated to Employee List page")

    def test_employee_list_elements(self):
        fields = {
            "Employee Name": (By.XPATH, "//label[text()='Employee Name']/following::input[1]"),
            "Employee Id": (By.XPATH, "//label[text()='Employee Id']/following::input[1]"),
            "Employment Status": (By.XPATH, "//label[text()='Employment Status']/following::div[contains(@class,'oxd-select-text')]"),
            "Include": (By.XPATH, "//label[text()='Include']/following::div[contains(@class,'oxd-select-text')]"),
            "Supervisor Name": (By.XPATH, "//label[text()='Supervisor Name']/following::input[1]"),
            "Job Title": (By.XPATH, "//label[text()='Job Title']/following::div[contains(@class,'oxd-select-text')]"),
            "Sub Unit": (By.XPATH, "//label[text()='Sub Unit']/following::div[contains(@class,'oxd-select-text')]"),
        }

        for name, locator in fields.items():
            element = self.wait.until(EC.presence_of_element_located(locator))
            assert element.is_displayed(), f"{name} field not displayed"
            print(f"✅ {name} field is visible")

        self.check_clickable((By.XPATH, "//button[@type='submit']"), "Search button")
        self.check_clickable((By.XPATH, "//button[contains(text(),'Reset')]"), "Reset button")

        headers = ["Id", "First (& Middle) Name", "Last Name", "Job Title", "Employment Status", "Sub Unit"]
        for header_text in headers:
            header = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@role='columnheader']//span[text()='{header_text}']")))
            assert header.is_displayed(), f"Table header '{header_text}' not visible"
            print(f"✅ Table header '{header_text}' is visible")

    def check_clickable(self, by_locator, name):
        try:
            self.wait.until(EC.element_to_be_clickable(by_locator))
            print(f"✅ {name} is clickable")
        except TimeoutException:
            raise AssertionError(f"{name} is NOT clickable")

    def test_search_functionality(self):
        emp_name_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Employee Name']/following::input[1]")))
        emp_name_input.clear()
        emp_name_input.send_keys("Linda")

        search_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        search_button.click()

        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='oxd-table-body']//div[contains(@class, 'oxd-table-card')]")))
            print("✅ Search results loaded")
        except TimeoutException:
            print("⚠️ No search results found or table did not load")

    def logout(self):
        try:
            user_dropdown = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab")))
            user_dropdown.click()

            logout_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']")))
            logout_button.click()

            self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            print("✅ Logged out successfully")
        except (TimeoutException, WebDriverException):
            print("⚠️ Unable to logout cleanly")

    def run_all_tests(self):
        try:
            self.login()
            self.navigate_to_pim_menu()
            self.check_pim_menu_options()
            self.navigate_to_employee_list()
            self.test_employee_list_elements()
            self.test_search_functionality()
        except AssertionError as e:
            print(f"❌ Test failed: {e}")
        finally:
            self.logout()
            try:
                self.driver.quit()
            except WebDriverException:
                pass


if __name__ == "__main__":
    test = OrangeHRMPIMTest()
    test.run_all_tests()
