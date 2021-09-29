import datetime

def calculate_duration(time_from: str):
    dt_time_from = datetime.datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S')
    time_delta = datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None) - dt_time_from
    return str(time_delta)