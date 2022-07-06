import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

url = 'https://www.nottinghamcity.gov.uk/terms'
site = BeautifulSoup(requests.get(url).content, 'html.parser')

termOutput = "Term,Starts,Ends\n"
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
                    
                    day   = termDates[1].split(' ')[-2]
                    month = datetime.strptime(termDates[1].split(' ')[-1], '%B').month
                    year  = termName[n].text[-4:]
                    date  = '{0}/{1}/{2}'.format(day, month, year)
                    print('{0} {1} on {2}'.format(termName[n].text,termDates[0], date))
                    if termDates[0] == 'Starts':
                        start = date
                    else:
                        end = date
        termOutput += '{0},{1},{2}\n'.format(termName[n].text,start, end)
        print()
print()
print(termOutput)
out_file = open('termTimes.csv', 'w+')
out_file.write(termOutput)
out_file.close()