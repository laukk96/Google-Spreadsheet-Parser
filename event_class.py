from datetime import datetime, timedelta

def findEndTime(startTime):
    startTime = datetime(2022, )


class Event:
    def __init__(
        summary='',
        location='Amakara Dublin',
        description='',
        startTime='',
        endTime='',
        timeZone='America/San_Francisco',
        recurrence='RRULE:FREQ=DAILY;COUNT=1',
        attendee_email='',
        reminders=''
    ):
        event_dict = {
            'summary': summary,
            'location': location,
            'start': {
                # 'dateTime': '2011-06-03T10:00:00.000-07:00',
                'dateTime': startTime.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': timeZone
            },
            'end': {
                'dateTime': findEndTime(startTime),
                'timeZone': timeZone
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=20110617T065959Z',
            ],
            'attendees': [
                {'email': attendee_email}
            ],
            'reminders': {
                'useDefault':False,
                'overrides': [
                    {'method': 'popup', 'minutes': 30}
                ]
            }
        }
        
        