#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import selenium.common
import selenium.webdriver
from selenium.webdriver import ActionChains

WAIT_TO_LOAD = 3
SCROLL_NUMBER = 15

TEAM = "_TEAM_NAME_"
EMAIL = "EMAIL@gmail.com"
PASSWORD = "_PASS_WORD_"

if __name__ == '__main__':
    driver = selenium.webdriver.Firefox()
    driver.get("https://slack.com/signin")

    team_field = driver.find_element_by_id("domain")
    team_field.send_keys(TEAM)
    driver.find_element_by_id("submit_team_domain").click()
    time.sleep(3)

    email_field = driver.find_element_by_id("email")
    pass_field = driver.find_element_by_id("password")

    email_field.send_keys(EMAIL)
    pass_field.send_keys(PASSWORD)
    time.sleep(3)
    driver.find_element_by_id("signin_btn").click()
    time.sleep(5)

    actions = ActionChains(driver)

    for a in driver.find_elements_by_class_name("p-channel_sidebar__channel"):
        if str(a.get_attribute('href')).split('/')[-1] == "CA32Y4W03":
            a.click()
            break

    print "COMEÇOU A LIMPEZA"

    element_list = driver.find_element_by_class_name("c-virtual_list__scroll_container")
    element = element_list.find_element_by_class_name("c-message--last")

    i = 0
    while element:
        try:
            actions.move_to_element(element).perform()
            act_buttons_list = driver.find_element_by_class_name("c-message_actions__container")
            actions_buttons = act_buttons_list.find_elements_by_tag_name("button")

            time.sleep(1)
            actions_buttons[-1].click()

            time.sleep(1)
            driver.find_element_by_class_name('p-message_actions_menu__delete_message').click()

            time.sleep(1)
            driver.find_element_by_class_name('c-button--danger').click()

            driver.implicitly_wait(5)

            actions = ActionChains(driver)
            element = element_list.find_element_by_class_name("c-message--last")

            i += 1

        except selenium.common.exceptions.StaleElementReferenceException as ex:
            print i+1, "Failed STALE", str(ex).strip('\n')
            actions = ActionChains(driver)
            time.sleep(1)
            element_list = driver.find_element_by_class_name("c-virtual_list__scroll_container")
            element = element_list.find_element_by_class_name("c-message--last")
            continue
        except Exception as error:
            print i+1, "Failed GENERAL", str(error).strip('\n')
            driver.refresh()
            driver.implicitly_wait(5)
            element_list = driver.find_element_by_class_name("c-virtual_list__scroll_container")
            element = element_list.find_element_by_class_name("c-message--last")
            continue
        print i, "OK"

    time.sleep(10)
    driver.quit()
