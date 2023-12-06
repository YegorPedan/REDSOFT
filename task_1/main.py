from datetime import datetime


def get_flight_status(schedule_time: str, actual_time: str) -> str:

    schedule_datetime = datetime.strptime(schedule_time, '%H:%M')
    actual_datetime = datetime.strptime(actual_time, '%H:%M')

    if actual_datetime > schedule_datetime:
        delay = actual_datetime - schedule_datetime
        return f'Самолет опаздывает. Задержка: {delay}'
    elif actual_datetime < schedule_datetime:
        ahead = schedule_datetime - actual_datetime
        return f'Самолет прилетел раньше. Опережение: {ahead}'
    else:
        return 'Самолет прилетел вовремя.'


if __name__ == '__main__':
    schedule_time = input('Время прибытия по расписанию ')
    actual_time = input('Фактическое время прибытия ')
    print(get_flight_status(schedule_time, actual_time))