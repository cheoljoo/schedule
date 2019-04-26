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
sortedWorkContent = []
numOfWork = 0
projectContent = []
sortedProjectContent = []
numOfProject = 0
isSetStart = 0

def display():
    # datetime object containing current date and time
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    print("\n\n\n==WorkContents Max : 50 ==")
    #cnt = 0
    #for work in sortedWorkContent:
        #print(cnt,work)
        #cnt += 1

    i = 0
    print("[idx] {work:^40s}   |{project:^30s}".format(work="Work Contents", project="Project Contents"))
    print(" "*5, "-"*40 , " "*2, "-"*30);
    while ( (i < len(sortedWorkContent)) or ( i < len(sortedProjectContent)) ):
        print("[{index:3d}] {work:>40s}   |{project:>30s}".format(index=i, work=sortedWorkContent[i] if i < len(sortedWorkContent) else "   ", project=sortedProjectContent[i] if i < len(sortedProjectContent) else "   "))
        if (i+1) % 5 == 0 :
            print(" "*5, "-"*40 , " "*2, "-"*30);
        i += 1
#
    #print("Art: {a:5d},  Price: {p:8.2f}".format(a=453, p=59.058)
#
    
def inputValue():
    #'dateTime': '2019-03-26T09:00:00+09:00',
    global isSetStart
    global numOfWork
    global numOfProject
    global nowStart
    global nowEnd
    global msg
    if isSetStart == 1 :
        str1 = nowStart.strftime("%Y-%m-%dT")
        str1 += "%02d:%02d:00+09:00"%(nowStart.hour,nowStart.minute);
        print("already set the starting time : ", str1)
    print(") Set starting time (type -1; return)");
    print(") Number of WorkContents ; Number of ProjectContents (-1:none) ; Now is 1(Start),2(End) ; Counts of 15 Minute ; Messages ")
    print(") Number of WorkContents ; Number of ProjectContents (-1:none) ; Now is -1(use start from step1) ; AnyNumber  ; Messages ")
    inStr = input(" => ")
    now = datetime.datetime.utcnow() # 'Z' indicates UTC time
    x = inStr.split(';')
    numOfWork = int(x[0]);
    if numOfWork == -1 :
        isSetStart = 1
        nowStart = now + timedelta(hours = 9)  # + timezone
        nowStart -= timedelta(minutes = (now.minute % 15) )
        nowStart -= timedelta(seconds = now.second)
        return "skipAddCalendar"

    numOfProject = int(x[1]);
    startFlag = int(x[2]);
    count15Min = int(x[3]);
    msg = x[4];
    msg = msg.strip();
    print(numOfWork , numOfProject,startFlag, count15Min, msg , now , now.hour , now.minute)

    if (isSetStart == 1) and (startFlag == -1) :
        nowEnd = now + timedelta(hours = 9)  # + timezone
        nowEnd -= timedelta(seconds = now.second)
        nowEnd += timedelta(minutes = (15 - now.minute % 15) )
        return "addCalendar"
    
    nowStart = now + timedelta(hours = 9)  # + timezone
    nowEnd = now + timedelta(hours = 9)    # + timezone
    if startFlag == 1 :     # start
        nowStart -= timedelta(minutes = (now.minute % 15) )
        nowStart -= timedelta(seconds = now.second)
        nowEnd = nowStart + timedelta(minutes = 15 * count15Min)
        print("start",nowStart)
        print("end",nowEnd)
    else :                   # end
        nowEnd -= timedelta(seconds = now.second)
        nowEnd += timedelta(minutes = (15 - now.minute % 15) )
        nowStart = nowEnd - timedelta(minutes = 15 * count15Min)
        print("end",nowEnd)
        print("start",nowStart)

    return "addCalendar"

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

    smy = sortedWorkContent[numOfWork];
    if (numOfProject >= 0) and (numOfProject < len(sortedProjectContent))  :
        smy += " ({})".format(sortedProjectContent[numOfProject])
        print("smy=", smy , sortedProjectContent[numOfProject]);
    print(eventIns)
    if not msg :
        eventIns['summary'] = smy
    else:
        eventIns['summary'] = smy + " - " + msg
    eventIns['start']['dateTime'] = str1
    eventIns['end']['dateTime'] = str2
    print(eventIns)

    #start = event['start'].get('dateTime', event['start'].get('date'))
    #print(event['start'],start, event['summary'] , event['end'] , event['id'])

	# This is insert source
    event = service.events().insert(calendarId='primary', body=eventIns).execute()
    print('Event created: %s'%(event.get('htmlLink')))
    global isSetStart
    isSetStart = 0


def loop():
    while True:
        display()
        if inputValue() == "addCalendar" :
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

    # 2019  1/1 is work list
    events_result = service.events().list(calendarId='primary', 
										timeMin='2019-01-01T00:00:00+09:00',
										timeMax='2019-01-01T23:59:59+09:00',
                                        maxResults=50, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        #print(event['start'],start, event['summary'] , event['end'] , event['id'])
        x = event['summary'].split('-')
        node = x[0].strip().replace("  "," ")
        workContent.append(node)

    for workCount, workEvent in enumerate(sorted(workContent)):
        #print(workCount , "[",workEvent,"]")
        sortedWorkContent.append(workEvent)


    # 2019  1/2 is project list
    events_result = service.events().list(calendarId='primary', 
										timeMin='2019-01-02T00:00:00+09:00',
										timeMax='2019-01-02T23:59:59+09:00',
                                        maxResults=50, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        #print(event['start'],start, event['summary'] , event['end'] , event['id'])
        x = event['summary'].split('-')
        node = x[0].strip().replace("  "," ")
        projectContent.append(node)

    for projectCount, projectEvent in enumerate(sorted(projectContent)):
        #print(projectCount , "[",projectEvent,"]")
        sortedProjectContent.append(projectEvent)

	#/ This is delete source
    # current eventId has been deleted.
    #event = service.events().delete(calendarId='primary', eventId="1pcsgsu56j6vhmft6f70ghvuc8", sendUpdates=None).execute()

	#/ This is insert source
    #event = service.events().insert(calendarId='primary', body=eventIns).execute()
    #print 'Event created: %s'%(event.get('htmlLink'))

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

