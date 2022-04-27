from unicodedata import category
import requests

def luzScrapper(ini_date: str, end_date: str):
    url = ''+\
        'https://apidatos.ree.es/'+\
        '{lang}'+\
        '/datos'+\
        '/{category}'+\
        '/{widget}?'+\
        'start_date={ini_date}&'+\
        'end_date={end_date}&'+\
        'time_trunc={time_frame}&'+\
        'geo_trunc=electric_system&'+\
        'geo_limit={electric_zone}&'+\
        'geo_ids=8741'

    url = url.format(lang='es', category='balance', widget='balance-electrico',
        ini_date=ini_date, end_date=end_date, time_frame='hour', 
        electric_zone='peninsular')

    r = requests.get(url)

    print(r.json())
    with open('test.txt', 'w+') as file:
        file.write(r.text)

    return r.json()


def main():
    luz = luzScrapper('2022-04-27T00:00', '2022-04-27T10:00')

if __name__ == '__main__':
    main()
