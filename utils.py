import datetime
import time
from sys import stdout

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from user_config import DEFAULT_ELEMENT_WAITING_TIMEOUT


def wait_for_element(from_driver, by, selector, time_to_wait=DEFAULT_ELEMENT_WAITING_TIMEOUT):
    return WebDriverWait(from_driver, time_to_wait).until(lambda d: d.find_element(by, selector))


def wait_for_element_clickable(from_driver, by, selector, time_to_wait=DEFAULT_ELEMENT_WAITING_TIMEOUT):
    return WebDriverWait(from_driver, time_to_wait).until(EC.element_to_be_clickable((by, selector)))


def wait_for_element_visibility(from_driver, by, selector, time_to_wait=DEFAULT_ELEMENT_WAITING_TIMEOUT):
    return WebDriverWait(from_driver, time_to_wait).until(EC.visibility_of_element_located((by, selector)))


def wait_for(time_to_wait, interrupt_ahead=0, single_line=False):
    last_delta = time_to_wait - time.time()
    while True:
        current_time = time.time()
        delta = time_to_wait - current_time
        if last_delta - delta > 1:
            stdout.write(("\r" if single_line else "") +
                         f'Time left: {str(datetime.timedelta(seconds=delta))[:-7]}' +
                         ("" if single_line else "\r\n"))
            if single_line:
                stdout.flush()
            last_delta = delta
        if delta < interrupt_ahead:
            break


def check_element_exists(from_driver, by, selector):
    try:
        from_driver.find_element(by, selector)
    except NoSuchElementException:
        return False
    return True


def add_options(to_options, from_options_list):
    for option in from_options_list:
        to_options.add_argument(option)


def add_experimental_options(to_options, from_options_list):
    for option in from_options_list:
        to_options.add_experimental_option(*option)


def add_user_profile_preferences(to_option, from_options_list):
    for option in from_options_list:
        to_option.AddUserProfilePreference(*option)


class TaskSuccess(Exception):
    def __init__(self, index):
        print(f'Task #{index} successful.')
