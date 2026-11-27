from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from api import get_holidays, get_timezone


def decode_slots(raw):
    parts = raw.split(" ")
    return {"date": parts[0], "start": parts[1], "end": parts[3]}


def change_timezone(date_str, time_str, timezone_str):
    local_str = date_str + " " + time_str
    local_dt = datetime.strptime(local_str, "%Y-%m-%d %H:%M")
    local_dt = local_dt.replace(tzinfo=ZoneInfo(timezone_str))
    return local_dt.astimezone(timezone.utc)

def check_holiday(day, holidays):
    i = 0
    while i < len(holidays):
        if holidays[i]["date"] == day:
            return True, holidays[i]["name"]
        i = i + 1
    return False, ""


def find_slots(start_date, own_avail, other_avail, holidays, tz_a, tz_b):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()

    if start_dt.weekday() >= 4:
        return None

    slots = []
    current = start_dt

    while current.weekday() < 5:
        day = current.strftime("%Y-%m-%d")

        is_holiday, name = check_holiday(day, holidays)
        if is_holiday == True:
            print(day + " is " + name + " and is skipped.")
            current = current + timedelta(days=1)
            continue

        own_today = []
        i = 0
        while i < len(own_avail):
            if own_avail[i]["date"] == day:
                own_today.append(own_avail[i])
            i = i + 1

        other_today = []
        i = 0
        while i < len(other_avail):
            if other_avail[i]["date"] == day:
                other_today.append(other_avail[i])
            i = i + 1

        i = 0
        while i < len(own_today):
            own_start = change_timezone(day, own_today[i]["start"], tz_a)
            own_end = change_timezone(day, own_today[i]["end"], tz_a)

            j = 0
            while j < len(other_today):
                other_start = change_timezone(day, other_today[j]["start"], tz_b)
                other_end = change_timezone(day, other_today[j]["end"], tz_b)

                if own_start > other_start:
                    start = own_start
                else:
                    start = other_start

                if own_end < other_end:
                    end = own_end
                else:
                    end = other_end

                if start < end:
                    slots.append({"date": day, "start_utc": start, "end_utc": end})

                j = j + 1
            i = i + 1

        current = current + timedelta(days=1)

    return slots


def format_and_save(slots, tz_a, tz_b, filename):
    if slots == None:
        text = "Try again next week. No meeting slots can be planned from Friday to Sunday."
    elif len(slots) == 0:
        text = "No overlapping meeting slots found."
    else:
        text = "Suggested meeting slots:\n\n"
        i = 0
        while i < len(slots):
            start = slots[i]["start_utc"].astimezone(ZoneInfo(tz_a))
            end = slots[i]["end_utc"].astimezone(ZoneInfo(tz_a))
            start_b = slots[i]["start_utc"].astimezone(ZoneInfo(tz_b))
            end_b = slots[i]["end_utc"].astimezone(ZoneInfo(tz_b))

            text = text + slots[i]["date"] + ":\n"
            text = text + "  Own time:   " + start.strftime("%H:%M") + " - " + end.strftime("%H:%M") + "\n"
            text = text + "  Other time: " + start_b.strftime("%H:%M") + " - " + end_b.strftime("%H:%M") + "\n\n"
            i = i + 1

    print(text)
    file = open(filename, "w")
    file.write(text)
    file.close()


print("Cross-border Meeting Planner")
print("Country Codes: DE and US")
own_country = input("Your country code: ").upper()
own_city = input("Your city: ")
other_country = input("Other country code: ").upper()
other_city = input("Other city: ")

start_date = input("Start date (yyyy-mm-dd): ")

while True:
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        break
    except ValueError:
        print("Invalid date. Please use yyyy-mm-dd.")
        start_date = input("Start date (yyyy-mm-dd): ")

tz_a = get_timezone(own_city, own_country)
tz_b = get_timezone(other_city, other_country)

if tz_a == None or tz_b == None:
    print("Error: Timezone not found.")
    exit()

year = int(start_date[0:4])
holidays = get_holidays(own_country, year) + get_holidays(other_country, year)

print("\nOwn available slots. Format: yyyy-mm-dd hh:mm - hh:mm, 'done' for finish.")
own_strings = []
entry = ""
while entry != "done":
    entry = input("> ").strip()
    if entry.lower() == "done":
        break
    parts = entry.split(" ")
    if len(parts) != 4 or parts[2] != "-":
        print("Invalid format! Use: yyyy-mm-dd hh:mm - hh:mm")
    else:
        own_strings.append(entry)

print("\nOther available slots. Format: yyyy-mm-dd hh:mm - hh:mm, 'done' for finish.")
other_strings = []
entry = ""
while entry != "done":
    entry = input("> ").strip()
    if entry.lower() == "done":
        break
    parts = entry.split(" ")
    if len(parts) != 4 or parts[2] != "-":
        print("Invalid format! Use: yyyy-mm-dd hh:mm - hh:mm")
    else:
        other_strings.append(entry)


own_avail = []
i = 0
while i < len(own_strings):
    slot = decode_slots(own_strings[i])
    own_avail.append(slot)
    i = i + 1

other_avail = []
i = 0
while i < len(other_strings):
    slot = decode_slots(other_strings[i])
    other_avail.append(slot)
    i = i + 1


slots = find_slots(start_date, own_avail, other_avail, holidays, tz_a, tz_b)
format_and_save(slots, tz_a, tz_b, "results.txt")
