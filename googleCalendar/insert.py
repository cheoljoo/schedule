from __future__ import print_function
from datetime import datetime
from datetime import timedelta
import datetime
import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Seoul South Korea
# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

eventIns = {
  'summary': 'Google I/O 2019',
  #'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'insert.py',
  'start': {
    'dateTime': '2019-03-26T09:00:00+09:00',
  },
  'end': {
    'dateTime': '2019-03-26T17:00:00+09:00',
  },
  #'attendees': [
     #{'email': 'cheoljoo.lee@lge.com'},
  #],
  'reminders': {
    'useDefault': True,
    #'overrides': [
      #{'method': 'email', 'minutes': 15},
      #{'method': 'popup', 'minutes': 10},
    #],
  },
}

workContent = []
numOfWork = 0

def display():
    # datetime object containing current date and time
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    cnt = 0
    print("\n\n\n==WorkContents==")
    for work in workContent:
        print(cnt,work)
        cnt += 1

    
def inputValue():
    #'dateTime': '2019-03-26T09:00:00+09:00',
    now = datetime.datetime.utcnow() # 'Z' indicates UTC time
    str = now.strftime("%Y-%m-%dT")
    #print(str)
    inStr = input("Number of WorkContents ; Now is 1(Start),2(End) ; Count of 30 Mins ; Messages => ")
    x = inStr.split(';')
    global numOfWork
    numOfWork = int(x[0]);
    startFlag = int(x[1]);
    count30Min = int(x[2]);
    global msg
    msg = x[3];
    msg = msg.strip();
    print(numOfWork , startFlag, count30Min, msg , now , now.hour , now.minute)
    
    global nowStart
    global nowEnd
    nowStart = now + timedelta(hours = 9)  # + timezone
    nowEnd = now + timedelta(hours = 9)    # + timezone
    if startFlag == 1 :     # start
        nowStart -= timedelta(minutes = (now.minute % 30) )
        nowStart -= timedelta(seconds = now.second)
        nowEnd = nowStart + timedelta(minutes = 30 * count30Min)
        print("start",nowStart)
        print("end",nowEnd)
    else:                   # end
        nowEnd -= timedelta(seconds = now.second)
        nowEnd += timedelta(minutes = (30 - now.minute % 30) )
        nowStart = nowEnd - timedelta(minutes = 30 * count30Min)
        print("end",nowEnd)
        print("start",nowStart)

def addCalendar():
    print("add Calendar start",nowStart)
    print("add Calendar end",nowEnd)

    str1 = nowStart.strftime("%Y-%m-%dT")
    str1 += "%02d:%02d:00+09:00"%(nowStart.hour,nowStart.minute);
    #2019-03-26T09:00:00+09:00
    print(str1)
    str2 = nowEnd.strftime("%Y-%m-%dT")
    str2 += "%02d:%02d:00+09:00"%(nowEnd.hour,nowEnd.minute);
    #2019-03-26T09:00:00+09:00
    print(str2)

    print(eventIns)
    if not msg :
        eventIns['summary'] = workContent[numOfWork] 
    else:
        eventIns['summary'] = workContent[numOfWork] + " - " + msg
    eventIns['start']['dateTime'] = str1
    eventIns['end']['dateTime'] = str2
    print(eventIns)

    #start = event['start'].get('dateTime', event['start'].get('date'))
    #print(event['start'],start, event['summary'] , event['end'] , event['id'])

	# This is insert source
    event = service.events().insert(calendarId='primary', body=eventIns).execute()
    print('Event created: %s'%(event.get('htmlLink')))


def loop():
    while True:
        display()
        inputValue()
        addCalendar()
        input("Press any key to add calendar ........")

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    global service
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events',now)
    #'2019-03-26T09:00:00+09:00' , now
    events_result = service.events().list(calendarId='primary', 
										timeMin='2019-01-01T00:00:00+09:00',
										timeMax='2019-01-01T23:59:59+09:00',
                                        maxResults=50, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    workCount = 0
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        #print(event['start'],start, event['summary'] , event['end'] , event['id'])
        x = event['summary'].split('-')
        node = x[0].strip().replace("  "," ")
        workContent.append(node)
        print(workCount , "[",workContent[workCount],"]")
        workCount = workCount + 1

	#/ This is delete source
    # current eventId has been deleted.
    #event = service.events().delete(calendarId='primary', eventId="1pcsgsu56j6vhmft6f70ghvuc8", sendUpdates=None).execute()

	#/ This is insert source
    #event = service.events().insert(calendarId='primary', body=eventIns).execute()
    #print 'Event created: %s'%(event.get('htmlLink'))

    now = datetime.datetime.utcnow() # 'Z' indicates UTC time
    print("now =", now)
    print(now.strftime("%d/%m/%Y %H:%M:%S"))
    print("Current date and time using instance attributes:")
    print("Current year: %d" % now.year)
    print("Current month: %d" % now.month)
    print("Current day: %d" % now.day)
    print("Current hour: %d" % now.hour)
    print("Current minute: %d" % now.minute)
    print("Current second: %d" % now.second)
    print("Current microsecond: %d" % now.microsecond)

    loop()

if __name__ == '__main__':
    main()

