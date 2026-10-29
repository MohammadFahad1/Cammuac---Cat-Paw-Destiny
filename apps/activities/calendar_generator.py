import random
from calendar import monthrange
from datetime import date
from typing import Dict, Tuple, Optional
from activities.models import (
    DayStatus,
    DayStatusType,
    get_calendar_status_info,
    get_day_status_payload,
)


def get_deterministic_month_statuses(year: int, month: int) -> Dict[int, str]:
    """
    Generates a deterministic and authentic day-status distribution for a given year and month.
    Matches traditional Chinese almanac (通勝 / 黃曆) proportions:
    - ~7-9 Lucky days (吉 / Ji)
    - ~6-7 Bad Luck days (凶 / Xiong)
    - ~15-17 Normal days (平 / Ping)
    """
    days_in_month = monthrange(year, month)[1]
    rng = random.Random(year * 1000 + month * 37 + 2026)

    # Divide month into 4 quarters to guarantee even distribution
    q1 = list(range(1, 8))
    q2 = list(range(8, 16))
    q3 = list(range(16, 24))
    q4 = list(range(24, days_in_month + 1))

    # Pick 2 lucky days from each quarter (7-8 lucky days per month)
    lucky_days = set()
    for q in [q1, q2, q3, q4]:
        k = 2 if len(q) >= 6 else 1
        lucky_days.update(rng.sample(q, k))

    # Pick 6-7 bad luck days from remaining non-lucky days
    remaining = [d for d in range(1, days_in_month + 1) if d not in lucky_days]
    bad_count = 7 if days_in_month >= 31 else 6
    bad_luck_days = set(rng.sample(remaining, min(bad_count, len(remaining))))

    result = {}
    for d in range(1, days_in_month + 1):
        if d in lucky_days:
            result[d] = DayStatusType.LUCKY
        elif d in bad_luck_days:
            result[d] = DayStatusType.BAD_LUCK
        else:
            result[d] = DayStatusType.NORMAL

    return result


def seed_calendar_range(start_year: int = 2025, end_year: int = 2030) -> Tuple[int, int]:
    """
    Seeds DayStatus entries in the database from start_year through end_year (till Dec 31, end_year).
    Preserves all existing entries (including verified real calendar dates for Oct, Nov, Dec 2026).
    Returns (created_count, skipped_existing_count).
    """
    existing_dates = set(DayStatus.objects.values_list('date', flat=True))

    new_objects = []
    created_count = 0
    skipped_count = 0

    for yr in range(start_year, end_year + 1):
        for mo in range(1, 13):
            month_statuses = get_deterministic_month_statuses(yr, mo)
            for day_num, status_val in month_statuses.items():
                cur_date = date(yr, mo, day_num)
                if cur_date in existing_dates:
                    skipped_count += 1
                    continue

                info = get_calendar_status_info(status_val)
                note_val = f"{info['zh']}日 ({info['status_en']})"
                new_objects.append(
                    DayStatus(
                        date=cur_date,
                        status=status_val,
                        note=note_val,
                    )
                )
                created_count += 1

    if new_objects:
        DayStatus.objects.bulk_create(new_objects, batch_size=1000)

    return created_count, skipped_count


def build_calendar_response_data(
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> Tuple[dict, dict, dict]:
    """
    Builds the formatted calendar dictionaries for the API:
    - calendar_en: {"2026": {"10": {"1": "Ji", "2": "Ping", "3": "Xiong"}}}
    - calendar_zh: {"2026": {"10": {"1": "吉", "2": "平", "3": "凶"}}}
    - calendar_bilingual: {"2026": {"10": {"1": {"en": "Ji", "zh": "吉", ...}}}}
    """
    # Determine bounds
    if year is not None:
        y_start = year
        y_end = year
    else:
        y_start = start_year or 2026
        y_end = end_year or 2030

    m_start = month if (year is not None and month is not None) else 1
    m_end = month if (year is not None and month is not None) else 12

    # Query DB for this date range
    d_start = date(y_start, m_start, 1)
    last_day_of_end_month = monthrange(y_end, m_end)[1]
    d_end = date(y_end, m_end, last_day_of_end_month)

    db_entries = {
        item['date']: item['status']
        for item in DayStatus.objects.filter(date__range=(d_start, d_end)).values('date', 'status')
    }

    calendar_en = {}
    calendar_zh = {}
    calendar_bilingual = {}

    for y in range(y_start, y_end + 1):
        y_str = str(y)
        calendar_en[y_str] = {}
        calendar_zh[y_str] = {}
        calendar_bilingual[y_str] = {}

        cur_m_start = m_start if (y == y_start and year is not None and month is not None) else 1
        cur_m_end = m_end if (y == y_end and year is not None and month is not None) else 12

        for m in range(cur_m_start, cur_m_end + 1):
            m_str = str(m)
            calendar_en[y_str][m_str] = {}
            calendar_zh[y_str][m_str] = {}
            calendar_bilingual[y_str][m_str] = {}

            days_in_month = monthrange(y, m)[1]
            fallback_month = None

            for d in range(1, days_in_month + 1):
                cur_date = date(y, m, d)
                status_code = db_entries.get(cur_date)

                if not status_code:
                    if fallback_month is None:
                        fallback_month = get_deterministic_month_statuses(y, m)
                    status_code = fallback_month.get(d, DayStatusType.NORMAL)

                info = get_calendar_status_info(status_code)
                d_str = str(d)

                calendar_en[y_str][m_str][d_str] = info['en']
                calendar_zh[y_str][m_str][d_str] = info['zh']
                calendar_bilingual[y_str][m_str][d_str] = {
                    'en': info['en'],
                    'zh': info['zh'],
                    'code': info['code'],
                    'status_en': info['status_en'],
                    'status_zh': info['status_zh'],
                }

    return calendar_en, calendar_zh, calendar_bilingual

