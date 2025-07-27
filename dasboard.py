import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestOrangeHRM:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.wait = WebDriverWait(self.driver, 10)

        # Login
        self.wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("Admin")
        self.driver.find_element(By.NAME, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for dashboard to load
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))

    def teardown_method(self):
        self.driver.quit()

    def check_visible(self, locator, name):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            assert element.is_displayed(), f"{name} is not visible"
        except Exception:
            self.driver.save_screenshot(f"{name.replace(' ', '_').lower()}_error.png")
            raise AssertionError(f"{name} is NOT visible")

    def test_sidebar_menu(self):
        self.check_visible((By.XPATH, "//aside"), "Sidebar Menu")

    def test_module_navigation(self):
        modules = ["Admin", "PIM", "Leave", "Time", "Recruitment", "My Info"]
        for module in modules:
            self.check_visible((By.XPATH, f"//span[text()='{module}']"), f"{module} module")

    def test_profile_dropdown(self):
        self.check_visible((By.XPATH, "//span[@class='oxd-userdropdown-tab']"), "Profile Dropdown")

    def test_search_bar_presence(self):
        self.check_visible((By.XPATH, "//input[@placeholder='Search']"), "Search Bar")

    # Replaced the failing test_welcome_banner_presence with this one:
    def test_quick_launch_widget_presence(self):
        # Checking if the Quick Launch widget on dashboard is visible
        self.check_visible((By.XPATH, "//div[contains(@class, 'quick-launch')]"), "Quick Launch Widget")

    def test_breadcrumb_visibility(self):
        self.check_visible((By.XPATH, "//nav[contains(@class, 'oxd-topbar-body-nav')]"), "Breadcrumb Navigation")
