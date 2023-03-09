import datetime


async def calculate_date(all_date):
    hours = 0
    days = 0
    for date in all_date:
        now_date = datetime.datetime.now()
        date = datetime.datetime.strptime(date['date'], "%Y-%m-%d %H:%M:%S")
        now_time = datetime.datetime.now().strftime("%H")
        user_time = date.strftime("%H")
        date3_days = now_date - datetime.timedelta(days=3)
        if date > date3_days:
            days += 1
            if now_time == user_time:
                hours += 1
    return days, hours
