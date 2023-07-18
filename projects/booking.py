import datetime
import pytz
from datetimerange import DateTimeRange  # third-party library used for comparing datetime ranges

def get_slots(hours, date, slot_duration, lat, lang, timezone=False, target_timezone=False, blocked=None):
    # Create an empty list to store available slots
    slots = []

    # Iterate through each hour object in the 'hours' input list
    for hour in hours:
        # Create slots for the current hour object
        created_slots = create_slots(hour.from_hour, hour.to_hour, date, hour.slot_duration, timezone, target_timezone)

        # If any slots were created, append the hour ID and list of slots to the 'slots' list
        if len(created_slots):
            data = []
            data.append(hour.id)
            data.append(created_slots)
            slots.append(data)

    # Get any existing appointments for the given date
    bookings = Appointments.objects.filter(start_time__date=date).values('start_time', 'end_time', 'id').all()

    # Convert the input timezone and target timezone to pytz timezone objects
    old_timezone = pytz.timezone(timezone)
    target_timezone = pytz.timezone(target_timezone)

    # Iterate through each blocked time range and remove any overlapping slots
    for block in blocked:
        start_time = datetime.datetime.combine(block['start_date'], block['start_time'])
        start_time = old_timezone.localize(start_time)
        start_time = start_time.astimezone(target_timezone)

        end_time = datetime.datetime.combine(block['end_date'], block['end_time'])
        end_time = old_timezone.localize(end_time)
        end_time = end_time.astimezone(target_timezone)

        # Find the slots that overlap with the current blocked time range and remove them
        for count, i in enumerate(slots):
            removing_objects = []
            for j in i[1]:
                if j in DateTimeRange(start_time, end_time) or start_time == j:
                    removing_objects.append(j)

            for remo in removing_objects:
                if remo in slots[count][1]:
                    slots[count][1].remove(remo)

    # Iterate through each existing appointment and remove any overlapping slots
    for booking in bookings:
        result_time = 0

        start_time = booking['start_time'] - datetime.timedelta(minutes=int(result_time))
        start_time = start_time.astimezone(old_timezone)
        end_time = booking['end_time'] + datetime.timedelta(minutes=int(result_time))
        end_time = end_time.astimezone(old_timezone)

        # Find the slots that overlap with the current appointment and remove them
        for count, i in enumerate(slots):
            removing_objects = []
            for j in i[1]:
                j = j.astimezone(old_timezone)
                if j in DateTimeRange(start_time, end_time) or start_time == j:
                    removing_objects.append(j)

            for remo in removing_objects:
                if remo in slots[count][1]:
                    slots[count][1].remove(remo)

    # Remove any empty hour objects from the 'slots' list
    slots = [slot for slot in slots if len(slot[1]) > 0]

    # Sort the 'slots' list in ascending order by the start time of each slot
    slots.sort(key=lambda x: x[1][0])

    return slots