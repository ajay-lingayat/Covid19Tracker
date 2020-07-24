import re
import requests
from bs4 import BeautifulSoup

def grab_data():
    try:
        URL = r"https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1%3F"
        r = requests.get(URL)
        r = r.text
        soup = BeautifulSoup(r, 'html.parser')

        div = soup.find_all('div', attrs = {'class', 'maincounter-number'})

        regex_pattern = "<span.*>(.+?)</span>"

        items = list()
        for i in div:
            item = re.findall(regex_pattern, str(i))
            items.append(item)

        cases = items[0][0]
        deaths = items[1][0]
        recovered = items[2][0]

        data = soup.find_all('table', attrs = {'id' : 'main_table_countries_today'})
        data = str(data)

        soup = BeautifulSoup(data, 'html.parser')

        data = soup.find_all('tr')
        for i in range(8):
            data.pop(0)

        regex_pattern = r">(.*?)<"

        rows = list()

        for i in data:
            soup = BeautifulSoup(str(i), 'html.parser')
            Data = soup.find_all('td')
            Data = str(Data)

            item = re.findall(regex_pattern, Data)
            for i in range(item.count(', ')):
                item.pop(item.index(', '))
            
            try:
                rows.append(item)
            except Exception as e:
                print(e)
        
        data = data_grab()
        if data:
           actives = data[0]
           closed = data[1]
        else:
            return False

        Info = [rows, cases, deaths, recovered, actives, closed]
        return Info
    except Exception as e:
        print(e)
        return False

def get_data( URL ):
    
    try:
        r = requests.get(URL)
        r = r.text

        soup = BeautifulSoup(r, 'html.parser')
        div = soup.find_all('div', attrs = {'class', 'maincounter-number'})

        regex_pattern = "<span.*>(.+?)</span>"

        items = list()
        for i in div:
            item = re.findall(regex_pattern, str(i))
            items.append(item)

        cases = items[0][0].replace(',','')
        deaths = items[1][0].replace(',','')
        recovered = items[2][0].replace(',','')

        cases_int = cases.strip()
        deaths_int = deaths.strip()
        recovered_int = recovered.strip()

        cases_str = items[0][0]
        deaths_str = items[1][0]
        recovered_str = items[2][0]

        div = soup.find_all('div', attrs = {'class': 'content-inner'})
        div = str(div[0])
        
        soup = BeautifulSoup(div, 'html.parser')
        head = soup.find_all('h1')
        head = str(head[0])
        
        regex_pattern = r">(.+?)<"

        items = re.findall(regex_pattern, head)
        items.pop(0)
        
        Country_Name = str(items[0][7:]).strip()

        data = [cases_int, deaths_int, recovered_int, cases_str, deaths_str, recovered_str, Country_Name]

        return data
    except Exception as e:
        print(e)
        return False

def data_grab():
    try:
        URL = r"https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1%3F"
        r = requests.get(URL)
        r = r.text
        soup = BeautifulSoup(r, 'html.parser')

        data = soup.find_all('div', attrs = {'class': 'panel_front'})

        regex_pattern = r">(.+?)<"

        main_numbers = list()
        for i in data:
            soup = BeautifulSoup(str(i), 'html.parser')
            item = soup.find_all('div', attrs = {'class': 'number-table-main'})
            if item:
                for j in item:
                    val = re.findall(regex_pattern, str(j))
                    if val:
                        for k in val:
                            main_numbers.append(k)

        regex_pattern = r">\s*(.+?)<"

        secondary_numbers = list()
        for i in data:
            soup = BeautifulSoup(str(i), 'html.parser')
            item = soup.find_all('span', attrs = {'class': 'number-table'})
            if item:
                for j in item:
                    val = re.findall(regex_pattern, str(j))
                    if val:
                        for k in val:
                            secondary_numbers.append(k)
            
        combined_List = list()
        for i in range(4):
            try:
                combined_List.append(main_numbers[i])
            except Exception as e:
                print(e)
            try:
                combined_List.append(secondary_numbers[i])
            except Exception as e:
                print(e)

        combined_Int_List = list()
        for i in combined_List:
            combined_Int_List.append(i.replace(',','').strip())

        data = [combined_List, combined_Int_List]
        if data:
            return data
        else:
            return False
    except Exception as e:
        print(e)
        return False

def grab_graph_data():
    try:
        URL = r"https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1%3F"
        r = requests.get(URL)
        r = r.text
        soup = BeautifulSoup(r, 'html.parser')

        data = soup.find_all('script', attrs = {'type': 'text/javascript'})

        regex_pattern = r".+(xAxis:?).+"

        Found_Scripts = list()
        for i in data:
            item = re.findall(regex_pattern, str(i))
            if item:
                Found_Scripts.append(str(i))

        regex_pattern = r"xAxis:(.+?)"
        for i in Found_Scripts:
            item = re.findall(regex_pattern, i)
            print(item)

    except Exception as e:
        print(e)
        return False

# grab_graph_data()