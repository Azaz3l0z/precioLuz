import os
import requests
import calendar
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

    def __create_data(self, ini_date, end_date, time_frame: str = 'hour'):
        ini_date = datetime.strptime(ini_date, '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

        hour_cap = 28*24 - 1

        diff_month = (end_date.year - ini_date.year)*12 + end_date.month - \
            ini_date.month
        
        print(diff_month+1)
        
        for k in range(diff_month + 1):
            end = calendar.monthrange(ini_date.year, ini_date.month)[1]
            end = ini_date.replace(day=end, hour=23)
            if end > end_date:
                end = end_date
            url = self.__make_url(ini_date, end, time_frame)
            ini_date = end + timedelta(hours=1)

            data = self.session.get(url).json()['included'][0]['attributes']['values']
            self.data.extend(data)

            print(url)
    
    def get_data(self, ini_date: str, end_date: str, format: str = 'hour'):
        self.__create_data(ini_date, end_date)
        
        data = [x['value'] for x in self.data]
        times = [datetime.fromisoformat(x['datetime']) for x in self.data]

        return data, times


def main():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # Data
    scrpr = luzScrapper()
    price, hours = scrpr.get_data('2021-04-21T01:00', '2022-04-27T00:00')

    # Plotting
    fig, ax = plt.subplots()
    ax.scatter(hours, price, color='orange', s=10)
    ax.plot(hours, price)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=45))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))

    ax.set_xlabel('Día')
    ax.set_ylabel('€/MWh')
    
    plt.show()
    fig.savefig('precios.png')
    
if __name__ == '__main__':
    main()
