import requests
import re
from datetime import date, datetime
from bs4 import BeautifulSoup
from icalendar import Calendar, Event, vCalAddress, vText
import pytz

url = 'https://www.nottinghamcity.gov.uk/terms'
site = BeautifulSoup(requests.get(url).content, 'html.parser')

cal = Calendar()


for i in range(1,6):
    terms = site.find('div', id='acc' + str(i)).find('div', class_='card card-body accordion')
    termName = terms.find_all('h3')
    termData = terms.find_all('ul')

    for n in range(0,len(termName)):
        start = ''
        end = ''
        for dates in termData[n]:
            if len(dates.text) > 1:
                t = re.sub(r'(\s?\(.*\)\s?)|(\s?[–]\s?.*)','',dates.text).replace(u'\xa0', u' ')
                termDates = t.split(':')
                if termDates[0] in ['Starts', 'Ends']:
                    event = Event()
                    day   = int(termDates[1].split(' ')[-2])
                    month = int(datetime.strptime(termDates[1].split(' ')[-1], '%B').month)
                    year  = int(termName[n].text[-4:])
                    myDate  = '{0}/{1}/{2}'.format(day, month, year)
                    print('{0} {1} on {2}'.format(termName[n].text,termDates[0], myDate))

                    event.add('summary', '{0} {1}'.format(termName[n].text,termDates[0]))
                    event.add('dtstart', date(year, month, day))
                    event.add('dtend', date(year, month, day))
                    event.add('location', 'Nottingham, UK')
                    cal.add_component(event)

        print()
print()
out_file = open('termTimes.ics', 'wb')
out_file.write(cal.to_ical())
out_file.close()


