import urllib2
from bs4 import BeautifulSoup
import tidecfg as cfg


 
#Main class which is responsible for interpretting the scrapped data off the site
class tideclass(object):
    
    def __new__(self,location):
        try:
            tideurl = cfg.quote_page % {"location":location}
            pagelink = urllib2.urlopen(tideurl)
            self.tidedata = BeautifulSoup(pagelink, 'html.parser')
            return super(tideclass, self).__new__(self)
        except Exception as e:
            print 'Invalid location specified {}'.format(e)
            return None
    
    def __init__(self,location):
        self.table = self.tidedata.find('table')
        
    def read_low_tide_data(self):
        table = self.tidedata.find('table')
        sunrise_ind = False
        low_tide_data=[]
        daily_record = {}
        for tr in table.find_all('tr'):
            columns = tr.find_all('td')
            ##At the start of rows with weekday reset each counters
            if (columns[0].getText()).startswith(cfg.weeknames):
                sunrise_ind = False
                daily_record = {}
            #get the day information at the start of a given set of day activities
                daily_record['event_date'] = columns[0].getText()
            if columns[4].getText() == 'Sunrise' or (len(columns) >= 6 and columns[5].getText() == 'Sunrise'):
                sunrise_ind = True
            if columns[4].getText() == 'Sunset' or (len(columns) >= 6 and columns[5].getText() == 'Sunset'):
                sunrise_ind = False
            if sunrise_ind:
                if columns[4].getText() == 'Low Tide':
                    daily_record['low_tide_time'] = columns[0].getText()
                    daily_record['low_tide_height'] = columns[2].getText()
                    low_tide_data.append({k:v for k,v in daily_record.items()})
                    daily_record['low_tide_time'] = ''
                    daily_record['low_tide_height'] = ''
        return low_tide_data
 
def create_output(low_tide_dict):
    with open('low_tide_data.txt', 'w') as file:
        for beaches,low_tide_rows in low_tide_dict.iteritems():
            file.write('Location: ' + beaches + '\n')
            for items in low_tide_rows: 
                file.write('     Day: ' + items['event_date']  + '\n')
                file.write('     Time: ' + items['low_tide_time']  + '\n')
                file.write('     Height: ' + items['low_tide_height']  + '\n')
                file.write('\n')
 
def main():
    tide_repo = {}
    for beaches in cfg.tide_locations:
        tideobject = tideclass(beaches.replace(' ','-').replace(',',''))
        if tideobject:
            tide_repo[beaches] = tideobject.read_low_tide_data()
    if tide_repo:
        create_output(tide_repo)
        
    print 'All Done!...'


if __name__=='__main__':
    main()