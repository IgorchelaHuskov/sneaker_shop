"""Вспомогательные функции для объектов datetime, timezone и timedelta"""
import time
from collections import namedtuple
from datetime import datetime, timedelta, timezone


DT_AWARE = "%m/%d/%y %I:%M:%S %p %Z"
DT_NAIVE = "%m/%d/%y %I:%M:%S %p"
DATE_MONTH_NAME = "%b %d %Y"
ONE_DAY_IN_SECONDS = 86400

timespan = namedtuple(
    "timespan",
    [
        "days",
        "hours",
        "minutes",
        "seconds",
        "miliseconds",
        "microseconds",
        "total_seconds",
        "total_miliseconds",
        "total_microseconds",
    ],
)

def utc_now():
    """Текущая дата и время в формате UTC со значением в микросекундах, нормализованным до нуля.""" 
    return datetime.now(timezone.utc).replace(microsecond=0)


def localized_dt_string(dt, use_tz=None):
    """Преобразовать значение даты и времени в строку, локализованную для указанного часового пояса.""" 
    if not dt.tzinfo and not use_tz:
        return dt.strftime(DT_NAIVE)
    if not dt.tzinfo:
        return dt.replace(tzinfo=use_tz).strftime(DT_AWARE)
    return dt.astimezone(use_tz).strftime(DT_AWARE) if use_tz else dt.strftime(DT_AWARE)


def get_local_utcoffset():
    """Получить смещение UTC из локальной системы и вернуть его как объект часового пояса.""" 
    utc_offset = timedelta(seconds=time.localtime().tm_gmtoff)
    return timezone(offset=utc_offset)


def make_tzaware(dt, use_tz=None, localize=True):
    """Создать простой объект datetime с учетом часового пояса.""" 
    if not use_tz:
        use_tz = get_local_utcoffset()
    return dt.astimezone(use_tz) if localize else dt.replace(tzinfo=use_tz)


def dtaware_fromtimestamp(timestamp, use_tz=None):
    """Объект даты и времени с учетом часового пояса из временной метки UNIX.""" 
    timestamp_naive = datetime.fromtimestamp(timestamp)
    timestamp_aware = timestamp_naive.replace(tzinfo=get_local_utcoffset())
    return timestamp_aware.astimezone(use_tz) if use_tz else timestamp_aware


def remaining_fromtimestamp(timestamp):
    """Calculate time remaining from now until UNIX timestamp value."""
    now = datetime.now(timezone.utc)
    dt_aware = dtaware_fromtimestamp(timestamp, use_tz=timezone.utc)
    if dt_aware < now:
        return timespan(0, 0, 0, 0, 0, 0, 0, 0, 0)
    return get_timespan(dt_aware - now)


def format_timespan_dgits(ts):
    """Отформатирывать временной интервал с именованным кортежем как строку, напоминающую цифровой дисплей.""" 
    if ts.days:
        day_or_days = "days" if ts.days > 1 else "day"
        return(
            f"{ts.days} {day_or_days}, "
            f"{ts.hours:02d}:{ts.minutes:02d}:{ts.seconds:02d}"
        ) 
    if ts.seconds:
        return f"{ts.hours:02d}:{ts.minutes:02d}:{ts.seconds:02d}"
    return f"00:00:00.{ts.total_microseconds}"


def format_timedelta_digits(td):
    """Отформатирывать объект timedelta как строку, напоминающую цифровой дисплей.""" 
    return format_timespan_dgits(get_timespan(td))


def format_timespan_str(ts):
    """Отформатирывать промежуток времени с именованым кортежем как читаемую строку.""" 
    if ts.days:
        day_or_days = "days" if ts.days > 1 else "day"
        return (
            f"{ts.days} {day_or_days} "
            f"{ts.hours:.0f} hours {ts.minutes:.0f} minutes {ts.seconds} seconds"
        )
    if ts.hours:
        return f"{ts.hours:.0f} hours {ts.minutes:.0f} minutes {ts.seconds} seconds"
    if ts.minutes:
        return f"{ts.minutes:.0f} minutes {ts.seconds} seconds"
    if ts.seconds:
        return f"{ts.seconds} seconds {ts.milliseconds:.0f} milliseconds"
    return f"{ts.total_microseconds} mircoseconds"


def format_timedelta_str(td):
    """Отформатирывать объект timedelta как читаемую строку.""" 
    return format_timespan_str(get_timespan(td))


def get_timespan(td):
    """Преобразовать объект timedelta во временной интервал с именованым кортежом.""" 
    (milliseconds, microseconds) = divmod(td.microseconds, 1000)
    (minutes, seconds) = divmod(td.seconds, 60)
    (hours, minutes) = divmod(minutes, 60)
    total_seconds = td.seconds + (td.days * ONE_DAY_IN_SECONDS)
    return timespan(
        td.days,
        hours,
        minutes,
        seconds,
        milliseconds,
        microseconds,
        total_seconds,
        (total_seconds * 1000 + milliseconds),
        (total_seconds * 1000 * 1000 + milliseconds * 1000 + microseconds),
    )
