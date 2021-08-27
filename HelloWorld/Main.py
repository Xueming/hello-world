import sys
import threading
import pickle

import arguments
import traceback
import time

from FreightSmart import FreightSmart
from commons import log


from os import path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def freight_smart(port, cookies):
    log("Creating player for [%s]" % port)
    try:
        return FreightSmart("", port, cookies)
    except BaseException as err:
        log("Failed to create player for " + port + " - " + str(err))
        traceback.print_exc()
        return None


login_driver = webdriver.Chrome(executable_path="bin/chromedriver")
login_account = arguments.login_account()

drivers = [login_driver]


def __load_cookies__():
    if path.exists("data/cookies.pkl") is False:
        return
    for cookie in pickle.load(open("data/cookies.pkl", "rb")):
        login_driver.add_cookie(cookie)
        log("Add Cookie: " + str(cookie))


def __store_cookies__():
    pickle.dump(login_driver.get_cookies(), open("data/cookies.pkl", "wb"))


def __cookie_notice_dialog__():
    try:
        return login_driver.find_element_by_class_name("cookie-notice-dialog")
    except NoSuchElementException:
        return None


def __auth_container__():
    try:
        return login_driver.find_element_by_class_name("auth-container")
    except NoSuchElementException:
        return None


def __login__():
    login_driver.get("https://freightsmart.oocl.com/")

    __load_cookies__()

    login_driver.get("https://freightsmart.oocl.com/")

    if login_driver.title == "403 Forbidden":
        raise Exception(login_driver.title)

    __store_cookies__()

    element = __cookie_notice_dialog__()
    if element is not None:
        log("Cookie Notice Dialog...")
        element.find_element_by_class_name("el-button--danger").click()
        log("Allow All button is clicked.")
    else:
        log("Cookie Notice is skipped.")

    element = __auth_container__()

    if element is None:
        return

    element.click()
    log("Auth container is clicked.")
    login_driver.find_element_by_name("login_dialog_username").send_keys(login_account[0])
    log("Username is entered.")
    login_driver.find_element_by_id("login-password-input").send_keys(login_account[1])
    log("Password is entered.")
    login_driver.find_element_by_name("login_dialog_btn_login").click()
    log("Login button is clicked.")


__login__()
for i in range(0, 10):
    print(end='.')
    time.sleep(0.5)
print()


threads = []
try:
    lines = arguments.target_ports()
    log("Target ports: " + str(lines))
    for line in lines:
        player = freight_smart(line.strip(), login_driver.get_cookies())
        if player is not None:
            t = threading.Thread(target=player.run)
            t.start()
            threads.append(t)
finally:
    for t in threads:
        t.join()
    log("Please enter to stop...")
    sys.stdin.readline()
    for d in drivers:
        d.close()

