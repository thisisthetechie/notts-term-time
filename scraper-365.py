import requests, re, json
from datetime import date, datetime
from bs4 import BeautifulSoup
from dateutil import tz
from O365 import Account, FileSystemTokenBackend

creds = json.load(open('credentials.json', 'r'))

credentials = (
    creds['application_key'], 
    creds['secret_key']
)

scopes = ['https://graph.microsoft.com/Calendars.ReadWrite']

token_backend = FileSystemTokenBackend(token_path='auth', token_filename='o365_token.txt')
account = Account(credentials, token_backend=token_backend, main_resource=creds['user_email'])

add_calendar = True
if not account.is_authenticated:
    print('Token Expired')
else:

    url = 'https://www.nottinghamcity.gov.uk/terms'
    site = BeautifulSoup(requests.get(url).content, 'html.parser')

    schedule = account.schedule()
    calendar = schedule.get_calendar(calendar_name=creds['calendar_name'])

    for i in range(1,6):
        terms = site.find('div', id='acc' + str(i)).find('div', class_='card card-body accordion')
        termName = terms.find_all('h3')
        termData = terms.find_all('ul')

        for n in range(0,len(termName)):
            for dates in termData[n]:
                eventStart = ''
                eventEnd = ''
                if len(dates.text) > 1:
                    t = re.sub(r'(\s?\(.*\)\s?)|(\s?[-]\s?.*)','',dates.text).replace(u'\xa0', u' ')
                    termDates = t.split(':')

                    if termDates[0] in ['Starts', 'Ends']:
                        day   = int(termDates[1].split(' ')[-2])
                        month = int(datetime.strptime(termDates[1].split(' ')[-1], '%B').month)
                        year  = int(termName[n].text[-4:])
                        myDate  = date(year,month,day)
                        print('{0} {1} on {2}'.format(termName[n].text,termDates[0], myDate))
                        eventStart = myDate
                        eventEnd   = myDate

                    elif termDates[0].startswith('Half'):
                        halfTerm = termDates[1].split(' to ')
                        for i in range(0,2):
                            day   = int(halfTerm[i].split(' ')[-2])
                            month = int(datetime.strptime(halfTerm[i].split(' ')[-1], '%B').month)
                            year  = int(termName[n].text[-4:])
                            myDate  = date(year,month,day)
                            if i == 0:
                                eventStart = myDate
                            else:
                                eventEnd   = myDate
                        print('{0} {1} between {2} and {3}'.format(termName[n].text,termDates[0], eventStart, eventEnd))

                    if add_calendar and eventStart:

                        string = '{0} {1}'.format(termName[n].text,termDates[0])
                        events = calendar.get_events(limit=200,include_recurring=False, query="contains(subject,'" + string + "')")
                        f = False

                        for event in events:
                            
                            if string in event.subject:
                                print(event)
                                print(string + ' exists')
                                f = True
                        
                        if not f:

                            print('Creating {0} {1} entry'.format(termName[n].text,termDates[0]) )
                            new_event = calendar.new_event()
                            new_event.subject = '{0} {1}'.format(termName[n].text,termDates[0])

                            new_event.start = eventStart
                            new_event.end   = eventEnd
                            new_event.is_all_day     = True
                            new_event.is_reminder_on = False
                            new_event.show_as        = "Free"

                            new_event.save()

            print()
    print()


