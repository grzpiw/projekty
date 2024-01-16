from datetime import datetime, timedelta
import calendar

def get_birthdays_per_week(users):
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    birthdays = {day: [] for day in calendar.day_name}

    for user in users:
        try:
            birthday_this_year = user['birthday'].replace(year=today.year)
        except ValueError:
            birthday_this_year = user['birthday'].replace(year=today.year, day=28)

        if birthday_this_year.weekday() in [5, 6]:
            birthdays['Monday'].append(user['name'])
        elif start_of_week <= birthday_this_year <= end_of_week:
            day_of_week = calendar.day_name[birthday_this_year.weekday()]
            birthdays[day_of_week].append(user['name'])

    for day, names in birthdays.items():
        if names:
            print(f"{day}: {', '.join(names)}")

users = [
    {'name': 'Andrzej', 'birthday': datetime(1990, 1, 10)},
    {'name': 'Tomek', 'birthday': datetime(1995, 1, 15)},
    {'name': 'Zofia', 'birthday': datetime(1985, 1, 8)},
    {'name': 'Jan', 'birthday': datetime(2000, 1, 12)},
    {"name": "Stefan", "birthday": datetime(1990, 1, 13)},  # Sobota
    {"name": "Katarzyna", "birthday": datetime(1990, 1, 14)},  # Niedziela
    {"name": "Edward", "birthday": datetime(1993, 1, 15)},
]

get_birthdays_per_week(users)