from __future__ import print_function
from datetime import datetime
from datetime import timedelta
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys , getopt
from collections import defaultdict


print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Seoul South Korea
# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

eventIns = {
  'summary': 'Google I/O 2019',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2019-03-26T09:00:00+09:00',
  },
  'end': {
    'dateTime': '2019-03-26T17:00:00+09:00',
  },
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

chart = defaultdict(dict)
chartLevel1 = defaultdict(dict)
chartLevel2 = defaultdict(dict)
chartallsubitem1 = defaultdict(dict)
chartallsubitem2 = defaultdict(dict)

def main(argv):
    year = ''
    month = ''
    try:
        opts, args = getopt.getopt(argv,"hy:m:",["year=","month="])
    except getopt.GetoptError:
        print('statistics.py -y <year> -m <month>')
        print('default (no arguments) : get info until current year and month')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('statistics.py -y <year> -m <month>')
            sys.exit()
        elif opt in ("-y", "--year"):
            year = arg
        elif opt in ("-m", "--month"):
            month = arg

    now = datetime.datetime.utcnow()
    if year == '' :
        year = str(now.year)
    if month == '' :
        month = str(now.month)

    print('Year is "', year)
    print('Month is "', month)

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

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    # '2019-03-26T09:00:00+09:00' , now
    yearInt = int(year)
    monthInt = int(month)
    yearIntOrg = yearInt
    monthIntOrg = monthInt
    startTime = "%d-01-02T00:00:00+09:00"%(yearInt)
    if monthInt == 12 :
        yearInt += 1
        endTime =   "%d-01-01T00:00:00+09:00"%(yearInt)
    else :
        endTime =   "%d-%02d-01T00:00:00+09:00"%(yearInt,monthInt+1)
    print(startTime,endTime)
    #print(now)

    events_result = service.events().list(calendarId='primary', 
                                        timeMin=startTime,
                                        timeMax=endTime,
                                        maxResults=5000, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    print(chart)

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print("===",start, event['summary'] , event['end'] , event['id'])
        #print(event['start'].get('dateTime'))
        #print(event['end'].get('dateTime'))
        xs = event['start'].get('dateTime').strip().split('T')
        ms = xs[0].strip().split('-')
        unit = "%s-%s"%(ms[0],ms[1])
        #print("unit",unit)
        #print(xs)
        ts = xs[1].strip().split(':')
        #print(ts)
        sHour = int(ts[0])
        sMin = int(ts[1])
        xe = event['end'].get('dateTime').strip().split('T')
        #print(xe)
        te = xe[1].strip().split(':')
        #print(te)
        eHour = int(te[0])
        eMin = int(te[1])
        calMinute = (eHour - sHour) * 60
        calMinute += (eMin - sMin)
        #print(calMinute)
        titles = event['summary'].strip().split('/')
        countTitle = len(titles)
        #print(titles,countTitle)
        for title in titles :
            t2 = title.strip().split('-')
            if chartLevel2[unit].get( t2[0].strip().lower() , -1) == -1:
                chartLevel2[unit][t2[0].strip().lower()] = int(calMinute / countTitle)
            else :
                chartLevel2[unit][t2[0].strip().lower()] += int(calMinute / countTitle)
            chartallsubitem2[t2[0].strip().lower()] = 0

            t1 = t2[0].strip().split(' ')
            if chartLevel1[unit].get( t1[0].strip().lower() , -1) == -1:
                chartLevel1[unit][t1[0].strip().lower()] = int(calMinute / countTitle)
            else :
                chartLevel1[unit][t1[0].strip().lower()] += int(calMinute / countTitle)
            chartallsubitem1[t1[0].strip().lower()] = 0
            #print("-",t1,"-",t1[0].strip().lower(),"=",t2[0].strip().lower(),"=")

        if chart[unit].get( event['summary'].strip().lower() , -1) == -1:
            chart[unit][event['summary'].strip().lower()] = calMinute
        else :
            chart[unit][event['summary'].strip().lower()] += calMinute

        if xs[0] != xe[0] :
            print(event['summary'] , event['start'] , event['end'] , event['id'])
            print(xs[0])
            print(xe[0])
            sys.exit()
    print(chart)
    print(chartLevel1)
    print(chartLevel2)

    f = open("%d-short.json"%(yearIntOrg),"w")
    f.write("[\n");

    f.write("  {\n");
    f.write("    \"key\": \"%d\",\n"%(yearIntOrg))
    f.write("    \"values\": [\n")
    for j,keyj in enumerate( sorted(chartallsubitem1) ) :
        f.write("      {\n");
        f.write("        \"key\": \"%s\",\n"%(keyj));
        f.write("        \"value\": 0\n");
        if j == len(chartallsubitem1) -1 :
            f.write("      }\n");
        else :
            f.write("      },\n");
    f.write("    ]\n")
    f.write("  },\n");

    for i,keyi in enumerate( sorted(chartLevel1) ) :
        f.write("  {\n");
        print("i",i,keyi)
        f.write("    \"key\": \"%s\",\n"%(keyi))
        f.write("    \"values\": [\n")
        for j,keyj in enumerate( sorted(chartallsubitem1) ) :
            f.write("      {\n");
            f.write("        \"key\": \"%s\",\n"%(keyj));
            f.write("        \"value\": %s\n"%(chartLevel1[keyi].get(keyj,0)));
            if j == len(chartallsubitem1) -1 :
                f.write("      }\n");
                print("  j last")
            else :
                f.write("      },\n");
        f.write("    ]\n")
        if i == len(chartLevel1) -1 :
            f.write("  }\n");
            print("i last")
        else :
            f.write("  },\n");
    f.write("]\n");
    f.close()

    f = open("year.json","w")
    f.write("[\n");

    f.write("  {\n");
    f.write("    \"key\": \"%d\",\n"%(yearIntOrg))
    f.write("    \"values\": [\n")
    for j,keyj in enumerate( sorted(chartallsubitem1) ) :
        f.write("      {\n");
        f.write("        \"key\": \"%s\",\n"%(keyj));
        f.write("        \"value\": 0\n");
        if j == len(chartallsubitem1) -1 :
            f.write("      }\n");
        else :
            f.write("      },\n");
    f.write("    ]\n")
    f.write("  },\n");

    for i,keyi in enumerate( sorted(chartLevel1) ) :
        f.write("  {\n");
        print("i",i,keyi)
        f.write("    \"key\": \"%s\",\n"%(keyi))
        f.write("    \"values\": [\n")
        for j,keyj in enumerate( sorted(chartallsubitem1) ) :
            f.write("      {\n");
            f.write("        \"key\": \"%s\",\n"%(keyj));
            f.write("        \"value\": %s\n"%(chartLevel1[keyi].get(keyj,0)));
            if j == len(chartallsubitem1) -1 :
                f.write("      }\n");
                print("  j last")
            else :
                f.write("      },\n");
        f.write("    ]\n")
        if i == len(chartLevel1) -1 :
            f.write("  }\n");
            print("i last")
        else :
            f.write("  },\n");
    f.write("]\n");
    f.close()



    f = open("%d-long.json"%(yearIntOrg),"w")
    f.write("[\n");

    f.write("  {\n");
    f.write("    \"key\": \"%d\",\n"%(yearIntOrg))
    f.write("    \"values\": [\n")
    for j,keyj in enumerate( sorted(chartallsubitem2) ) :
        f.write("      {\n");
        f.write("        \"key\": \"%s\",\n"%(keyj));
        f.write("        \"value\": 0\n");
        if j == len(chartallsubitem2) -1 :
            f.write("      }\n");
        else :
            f.write("      },\n");
    f.write("    ]\n")
    f.write("  },\n");

    for i,keyi in enumerate( sorted(chartLevel2) ) :
        f.write("  {\n");
        print("i",i,keyi)
        f.write("    \"key\": \"%s\",\n"%(keyi))
        f.write("    \"values\": [\n")
        for j,keyj in enumerate( sorted(chartallsubitem2) ) :
            f.write("      {\n");
            f.write("        \"key\": \"%s\",\n"%(keyj));
            f.write("        \"value\": %s\n"%(chartLevel2[keyi].get(keyj,0)));
            print("  long j ",j,keyj,chartLevel2[keyi].get(keyj,0))
            if j == len(chartallsubitem2) -1 :
                f.write("      }\n");
                print("  j last")
            else :
                f.write("      },\n");
        f.write("    ]\n")
        if i == len(chartLevel2) -1 :
            f.write("  }\n");
            print("i last")
        else :
            f.write("  },\n");
    f.write("]\n");
    f.close()

	#/ This is delete source
    # current eventId has been deleted.
    #event = service.events().delete(calendarId='primary', eventId="1pcsgsu56j6vhmft6f70ghvuc8", sendUpdates=None).execute()

	#/ This is insert source
    #event = service.events().insert(calendarId='primary', body=eventIns).execute()
    #print 'Event created: %s'%(event.get('htmlLink'))


if __name__ == "__main__":
    main(sys.argv[1:])
