# 首先通过pip安装selenium；Selenium抽象了WebDriver
# 然后下载chromedriver，它是WebDriver的一个Chrome实现
# 现在我们可以通过WebDriver来操作页面元素了
import sys

from commons import log
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FreightSmart(object):
    def __init__(self, start_port, target_port, cookies):
        self._start_port = start_port
        self._target_port = target_port
        self.driver = webdriver.Chrome(executable_path="bin/chromedriver")
        self._wait = WebDriverWait(self.driver, 3, 0.1)
        self.driver.get("https://freightsmart.oocl.com/")
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.get("https://freightsmart.oocl.com/")

        self.__click_place_order_link__()
        self.__enter_start_port__()
        self.__enter_target_port__()

    def run(self):
        if self._start_port and self._target_port:
            self.__sailing_product_btn_search__().click()
            self.__log__("Search button is clicked.")
        if self._start_port:
            self._wait.until(EC.presence_of_element_located((By.XPATH, '//div[text() = "%s"]' % self._start_port)))
        if self._target_port:
            self._wait.until(EC.presence_of_element_located((By.XPATH, '//div[text() = "%s"]' % self._target_port)))

        expand = self.driver.find_element_by_xpath('//button/span[text() = "展开所有产品"]/parent::button')
        expand.click()
        purchases = self._wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[text() = '购买']/parent::div")))

        for p in purchases:
            self.__purchase__(p)


    def __purchase__(self, element):
        element.click()
        self.__log__("购买 is clicked.")

        element = self._wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//table[@class = "container-amount"]/tbody/tr/td[text() = "40HQ"]/parent::tr/td[7]/div/div/input')),
            "Unable to find 40HQ.")
        max_amount = element.get_attribute('max')
        element.send_keys(max_amount)

    def __sailing_product_location__(self, port):
        return self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//li[starts-with(@name, "sailing_product_location")]/span[starts-with(text(), "%s")]/parent::li' % port)),
            "Unable to locate sailing_product_location.")

    def __enter_start_port__(self):
        element = self._wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[1]/section/div[1]/div/div[2]/div[2]/div[2]/div/div/input'))
        )
        if self._start_port:
            element.send_keys(self._start_port)
            self.__log__("Enter start port %s" % self._start_port)
            element = self.__sailing_product_location__(self._start_port)
            element.click()


    def __enter_target_port__(self):
        element = self._wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[1]/section/div[1]/div/div[2]/div[2]/div[4]/div/div/input'))
        )
        if self._target_port:
            element.send_keys(self._target_port)
            self.__log__("Enter target port " + self._target_port)
            element = self.__sailing_product_location__(self._target_port)
            element.click()

    def __click_place_order_link__(self):
        element = self._wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/section/header/div/ul/li'))
        )
        element.click()
        self.__log__("Place Order link is clicked.")

    def __sailing_product_btn_search__(self):
        return self.driver.find_element_by_name("sailing_product_btn_search")

    def __log__(self, message):
        log("[" + self._target_port + "]: " + message)
