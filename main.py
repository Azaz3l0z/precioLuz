import os
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from datetime import datetime, timedelta

class luzScrapper():
    def __init__(self) -> None:
        self.session = requests.Session()
        self.data = []
    
    def __make_url(self, ini_date: datetime, end_date: datetime, time_frame: str = 'hour'):
        url = ''+\
        'https://apidatos.ree.es/'+\
        '{lang}'+\
        '/datos'+\
        '/{category}'+\
        '/{widget}?'+\
        'start_date={ini_date}&'+\
        'end_date={end_date}&'+\
        'time_trunc={time_frame}&'

        time_format = '%Y-%m-%dT%H:%M'
        ini_date = ini_date.strftime(time_format)
        end_date = end_date.strftime(time_format)

        url = url.format(lang='es', category='mercados',
            widget='precios-mercados-tiempo-real', ini_date=ini_date, 
            end_date=end_date, time_frame=time_frame)
        
        return url

    def __create_requests(self, ini_date: str, end_date: str, 
                          time_frame: str = 'hour'):
        ini_DATE = datetime.strptime(ini_date, '%Y-%m-%dT%H:%M')
        end_DATE = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
        hour_cap = 28*24 - 1

        diff = (end_DATE - ini_DATE)
        diff = int(diff.total_seconds()/3600)
        # https://stackoverflow.com/questions/2356501/how-do-you-round-up-a-number
        n = (diff // hour_cap) + (diff%hour_cap > 0)
        
        for k in range(n):
            # We calculate the end date adding more hours each time
            end = ini_DATE + timedelta(hours=hour_cap)
            # If we pass the end_date we don't do anything
            if end > end_DATE:
                end = end_DATE
            # We get the url and data
            url = self.__make_url(ini_DATE, end, time_frame)

            data = self.session.get(url)
            self.data.extend(data.json()['included'][0]['attributes']['values'])
            
            # We set the initial date to the last one
            ini_date = end
    
    def do(self):
        self.__create_requests('2022-02-22T01:00', '2022-04-26T00:00')
        print(len(self.data))

    #     data = r.json()['included'][0]['attributes']['values']
    # price = [x['value'] for x in data]
    # hours = [x['datetime'] for x in data]

def main():
    scrpr = luzScrapper()
    scrpr.do()
    # os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # price, hours = luzScrapper('2022-03-27T01:00', '2022-04-27T00:00')
    # hours = [datetime.fromisoformat(x) for x in hours]
    # print(len(hours))
    # print(hours[0:2])

    # # Plotting
    # fig, ax = plt.subplots()
    # ax.scatter(hours, price, color='orange', s=10)
    # ax.plot(hours, price)
    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H"))
    
    # plt.show()

if __name__ == '__main__':
    main()
