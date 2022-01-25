import json
import asyncio
import traceback
from json import JSONDecodeError

from aiohttp import ClientSession
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from seleniumwire import webdriver
from system_config import *
from user_config import *
from utils import *


async def send_post(index, session):
    try:
        async with session.post(API_BUYING_URL, json=PURCHASE_INFO, timeout=30) as task_response:
            print(f'Start task #{index}', end=' ')
            response = await task_response.text()
    except Exception as e:
        print(e)
    else:
        try:
            response_obj = json.loads(response)
            print(f'Task #{index} ends: {response_obj}')
            if response_obj['success']:  # TODO disable for test usage, enable if you want to trying stop other tasks when it successes
                raise TaskSuccess(index)
        except JSONDecodeError as e:
            print("Error decode string." + str(e))


async def create_tasks(headers):
    async with ClientSession(headers=headers) as session:
        tasks = [asyncio.ensure_future(send_post(i, session)) for i in range(REQUESTS_COUNT)]
        try:
            await asyncio.gather(*tasks)
        except TaskSuccess:
            for task in tasks:
                task.cancel()


def start_buying_up(headers):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_tasks(headers))


# START  #TODO implement time synchronization with server
driver = None
try:
    # Waiting for LOGIN_BEFORE_TIME
    # wait_for(SALE_TIME, LOGIN_BEFORE_TIME, True)
    # Create options
    chrome_options = webdriver.ChromeOptions()
    add_options(chrome_options, CHROME_OPTIONS)
    # Disable selenium identification
    add_experimental_options(chrome_options, CHROME_EXPERIMENTAL_OPTIONS)
    # add_user_profile_preferences(chrome_options, CHROME_USER_PROFILE_PREFERENCES)
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)

    # Create capabilities
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  # interactive page load

    # Create driver
    driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
    # Disable selenium identification
    driver.maximize_window()
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                            'Chrome/96.0.4664.93 Safari/537.36'})
    driver.get(LOGIN_URL)
except WebDriverException:
    traceback.print_exc()
    exit("Unable to load login page. Check connection or may be you in ban list?")

try:
    print("Preparing to login in...")
    # Enter login
    login_field: WebElement = wait_for_element_clickable(driver, By.NAME, 'email')
    login_field.click()
    if login_field.text != "":
        login_field.clear()
    login_field.send_keys(LOGIN)
    # Enter password
    password_field = wait_for_element_clickable(driver, By.NAME, 'password')
    password_field.click()
    if password_field.text != "":
        login_field.clear()
    password_field.send_keys(PASSWORD)
    # Doing login
    login_button = wait_for_element_clickable(driver, By.ID, 'click_login_submit')
    login_button.submit()
    # Waiting for login
    wait_for_element(driver, By.XPATH,
                     '//*[@id="__APP"]/div/div[2]/main/div/div/div[8]/button[2]', DEFAULT_LOGIN_WAITING_TIMEOUT)
    print('Logged in.')

    # Waiting for PREPARE_REQUEST_BEFORE_TIME
    wait_for(SALE_TIME, PREPARE_REQUEST_BEFORE_TIME)

    print('Preparing template request header...')
    # Set price to 999999999
    price_field: WebElement = wait_for_element_clickable(driver, By.XPATH,
                                                         '/html/body/div[1]/div/div[2]/main/div/div/'
                                                         'div[5]/div[2]/div/div[1]/input')
    while ''.join(filter(str.isdigit, price_field.get_attribute('value'))) != "999999999":
        price_field.click()
        price_field.send_keys("9")

    # Open confirm window
    confirm_button = wait_for_element_clickable(driver, By.XPATH,
                                                '//*[@id="__APP"]/div/div[2]/main/div/div/div[8]/button[2]')
    confirm_button.click()
    # Confirm deal
    confirm_button = wait_for_element_clickable(driver, By.XPATH, '/html/body/div[5]/div/div/div[7]/button[2]')
    confirm_button.click()
    # Waiting for template request
    request = driver.wait_for_request(API_AUTH_URL)
    print('Template request received.')
    auth_headers = {
        'Host': 'www.binance.com',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'clienttype': 'web',
        'x-nft-checkbot-token': request.headers.get('x-nft-checkbot-token'),
        'x-nft-checkbot-sitekey': request.headers.get('x-nft-checkbot-sitekey'),
        'x-trace-id': request.headers.get('x-trace-id'),
        'x-ui-request-trace': request.headers.get('x-ui-request-trace'),
        'content-type': 'application/json',
        'cookie': request.headers.get('cookie'),
        'csrftoken': request.headers.get('csrftoken'),
        'device-info': request.headers.get('device-info'),
        'user-agent': request.headers.get('user-agent')
    }

    # Waiting for sale starts
    wait_for(SALE_TIME)

    requests_start_time = time.time()

    print('Start buying up...')
    start_buying_up(auth_headers)

    requests_stop_time = time.time()

    print(f'Elapsed time: {requests_stop_time - requests_start_time} second(s)')
except TimeoutException:
    print("Waiting for element timeout. You can increase limit by default in system config *_WAITING_TIMEOUT.")
    traceback.print_exc()
except NoSuchElementException or StaleElementReferenceException:
    print("May be page structure has been changed. Please check selectors.")
    traceback.print_exc()
finally:
    driver.quit()
