import re
import time
from typing import List, Tuple, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


def init_driver() -> WebDriver:
    options = Options()
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(options=options)
    return driver


def login(driver: WebDriver, owa_url: str, username: str, password: str) -> None:
    driver.get(owa_url)
    time.sleep(2)
    try:
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        time.sleep(3)
    except Exception as e:
        print("Login error:", e)
        driver.quit()
        exit()


def fetch_calendar_events(driver: WebDriver, owa_url: str) -> Tuple[List[str], List[Tuple[str, str]]]:
    driver.get(owa_url + "/#path=/calendar/view/Month")
    time.sleep(5)

    events = driver.find_elements(By.CSS_SELECTOR, "div._wx_32")
    days = driver.find_elements(By.CSS_SELECTOR, "div._wx_42")
    dates = [day.get_attribute("aria-label") for day in days]

    all_events: List[Tuple[str, str]] = []
    for event in events:
        try:
            time_elem = event.find_element(By.CSS_SELECTOR, "span._cb_Y1")
            title_elem = event.find_element(By.CSS_SELECTOR, "span._cb_Z1")
            event_time = time_elem.text
            event_title = title_elem.text
            all_events.append((event_time, event_title))
        except:
            continue

    return dates, all_events


def map_events_to_days(dates: List[str], all_events: List[Tuple[str, str]]) -> List[Dict[str, List[Tuple[str, str]]]]:
    mapped: List[Dict[str, List[Tuple[str, str]]]] = []
    event_index = 0

    for date_text in dates:
        if not date_text:
            continue

        match = re.search(r"(\d+) events?", date_text)
        if match:
            count = int(match.group(1))
        else:
            count = 0

        day_events = all_events[event_index:event_index + count]
        event_index += count

        mapped.append({
            "date": date_text,
            "events": day_events
        })

    return mapped
