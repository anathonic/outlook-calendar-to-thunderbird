import re
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple


def parse_datetime(date_str: str, time_str: str) -> Optional[datetime]:
    date_match = re.search(r"\w+, (\w+ \d+, \d{4})", date_str)
    if not date_match:
        return None
    date_part = date_match.group(1)
    date_obj = datetime.strptime(date_part, "%B %d, %Y")

    time_match = re.match(r"(\d+)([ap])", time_str.lower())
    if not time_match:
        return datetime(date_obj.year, date_obj.month, date_obj.day, 0, 0)

    hour = int(time_match.group(1))
    meridiem = time_match.group(2)

    if meridiem == "p" and hour != 12:
        hour += 12
    if meridiem == "a" and hour == 12:
        hour = 0

    return datetime(date_obj.year, date_obj.month, date_obj.day, hour, 0)


def create_icalendar(
    mapped_events: List[Dict[str, List[Tuple[str, str]]]]
) -> Calendar:
    cal = Calendar()
    cal.add('prodid', '-//Calendar//')
    cal.add('version', '2.0')

    for day in mapped_events:
        date_str = day["date"]
        for event_time, event_title in day["events"]:
            dtstart = parse_datetime(date_str, event_time)
            if not dtstart:
                continue
            dtend = dtstart + timedelta(hours=1)

            event = Event()
            event.add('summary', event_title)
            event.add('dtstart', dtstart)
            event.add('dtend', dtend)
            event.add('dtstamp', datetime.now())
            cal.add_component(event)

    return cal


def save_calendar_to_file(calendar: Calendar, filename: str = "calendar.ics") -> None:
    with open(filename, "wb") as f:
        f.write(calendar.to_ical())
