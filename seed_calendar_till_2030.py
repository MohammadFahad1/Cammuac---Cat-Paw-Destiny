import os
import sys
from datetime import date

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    import django
    django.setup()

from activities.models import DayStatus, DayStatusType
from activities.calendar_generator import seed_calendar_range

# ==============================================================================
# Verified entries extracted from actual calendar photos:
# October 2026: 31 days
# November 2026: 30 days
# December 2026: 31 days
# ==============================================================================
OCTOBER_2026 = [
    (date(2026, 10, 1), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 2), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 3), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 10, 4), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 5), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 10, 6), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 10, 7), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 8), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 10, 9), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 10, 10), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 11), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 10, 12), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 13), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 10, 14), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 15), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 16), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 17), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 10, 18), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 19), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 20), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 10, 21), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 10, 22), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 23), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 10, 24), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 25), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 10, 26), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 27), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 28), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 10, 29), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 10, 30), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 10, 31), DayStatusType.NORMAL, "平 (Normal)"),
]

NOVEMBER_2026 = [
    (date(2026, 11, 1), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 11, 2), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 11, 3), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 4), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 11, 5), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 6), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 11, 7), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 8), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 9), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 10), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 11, 11), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 12), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 13), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 14), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 15), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 11, 16), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 11, 17), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 11, 18), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 19), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 20), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 21), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 22), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 11, 23), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 24), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 11, 25), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 11, 26), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 27), DayStatusType.BAD_LUCK, "凶 (Bad Luck - 陷阱日)"),
    (date(2026, 11, 28), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 11, 29), DayStatusType.LUCKY, "吉 (Lucky - 七大吉日)"),
    (date(2026, 11, 30), DayStatusType.NORMAL, "平 (Normal)"),
]

DECEMBER_2026 = [
    (date(2026, 12, 1), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 2), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 3), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 4), DayStatusType.BAD_LUCK, "凶 (Bad Luck)"),
    (date(2026, 12, 5), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 6), DayStatusType.LUCKY, "吉 (Lucky - 九大吉日)"),
    (date(2026, 12, 7), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 8), DayStatusType.LUCKY, "吉 (Lucky - 九大吉日)"),
    (date(2026, 12, 9), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 10), DayStatusType.BAD_LUCK, "凶 (Bad Luck)"),
    (date(2026, 12, 11), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 12), DayStatusType.LUCKY, "吉 (Lucky - 九大吉日)"),
    (date(2026, 12, 13), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 14), DayStatusType.LUCKY, "吉 (Lucky - 九大吉日)"),
    (date(2026, 12, 15), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 16), DayStatusType.BAD_LUCK, "凶 (Bad Luck)"),
    (date(2026, 12, 17), DayStatusType.LUCKY, "吉 (Lucky - 九大吉日)"),
    (date(2026, 12, 18), DayStatusType.LUCKY, "吉 (Lucky - 九大吉日)"),
    (date(2026, 12, 19), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 20), DayStatusType.LUCKY, "吉 (Lucky - 九大吉日)"),
    (date(2026, 12, 21), DayStatusType.BAD_LUCK, "凶 (Bad Luck)"),
    (date(2026, 12, 22), DayStatusType.BAD_LUCK, "凶 (Bad Luck)"),
    (date(2026, 12, 23), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 24), DayStatusType.LUCKY, "吉 (Lucky - 九大吉日)"),
    (date(2026, 12, 25), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 26), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 27), DayStatusType.BAD_LUCK, "凶 (Bad Luck)"),
    (date(2026, 12, 28), DayStatusType.BAD_LUCK, "凶 (Bad Luck)"),
    (date(2026, 12, 29), DayStatusType.LUCKY, "吉 (Lucky - 九大吉日)"),
    (date(2026, 12, 30), DayStatusType.NORMAL, "平 (Normal)"),
    (date(2026, 12, 31), DayStatusType.NORMAL, "平 (Normal)"),
]

PHOTO_CALENDAR_ENTRIES = OCTOBER_2026 + NOVEMBER_2026 + DECEMBER_2026


def main():
    print("=" * 65)
    print("Seeding Calendar Day Statuses in Database (2025 - 2030)...")
    print("=" * 65)

    # 1. First ensure all real calendar entries from photos are applied
    photo_count = 0
    for day_date, status_val, note_val in PHOTO_CALENDAR_ENTRIES:
        DayStatus.objects.update_or_create(
            date=day_date,
            defaults={'status': status_val, 'note': note_val}
        )
        photo_count += 1
    print(f"[*] Verified/Applied {photo_count} days for Oct, Nov, Dec 2026 from photo calendars.")

    # 2. Seed remaining dates through 2030
    created, skipped = seed_calendar_range(start_year=2025, end_year=2030)
    print(f"[*] Seeded remaining range 2025-2030: Created {created}, Kept existing {skipped}")

    total_in_db = DayStatus.objects.count()
    print("=" * 65)
    print(f"SUCCESS! Database now contains {total_in_db} DayStatus entries through 2030-12-31.")
    print("=" * 65)


if __name__ == '__main__':
    main()
elif __name__ == 'django.core.management.commands.shell' or 'main' in globals():
    main()

