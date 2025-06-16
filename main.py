import json

from utils.icalendar import create_icalendar, save_calendar_to_file
from utils.webdriver import init_driver, login, fetch_calendar_events, map_events_to_days


def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    credentials = load_config()

    username = credentials["username"]
    password = credentials["password"]
    owa_url = credentials["owa_url"]

    driver = init_driver()
    login(driver, owa_url, username, password)
    dates, all_events = fetch_calendar_events(driver, owa_url)
    driver.quit()

    mapped_events = map_events_to_days(dates, all_events)
    calendar = create_icalendar(mapped_events)
    save_calendar_to_file(calendar)

    print("Done!")
