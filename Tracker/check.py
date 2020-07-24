import requests
from bs4 import BeautifulSoup
import re

def check_country( name ):
    try:
        url = r'https://www.worldometers.info/coronavirus/country/'
        location = r'https://www.worldometers.info/coronavirus/country/{}'.format(name.replace(' ','-'))
    
        URL = r"https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1%3F"
        r = requests.get(URL)
        r = r.text
        soup = BeautifulSoup(r, 'html.parser')

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
            new_List = [Data[1]]
            Data = str(new_List)

            item = re.findall(regex_pattern, Data)
            for i in range(item.count(', ')):
                item.pop(item.index(', '))
            
            try:
                rows.append(item)
            except Exception as e:
                print(e)
        
        for i in rows:
            try:
               i.pop(0)
               i.pop(-1)
            except:
               pass
        
        rows.pop(0)
        for i in range(8):
            rows.pop(-1)

        new_row = list()
        
        for i in rows:
            if i:
               try:
                   if i[0].upper().strip() == 'CURAÇAO':
                       new_row.append('CURACAO')
                   else:
                       new_row.append(i[0].upper().strip())
               except:
                   pass

        customs = ['US', 'UNITED-ARAB-EMIRATES','UNITED ARAB EMIRATES', 'COTE-D-IVOIRE', 'CZECH REPUBLIC', 'CZECH-REPUBLIC', 'SOUTH KOREA', 'STATE OF PALESTINE', 'MACEDONIA', 'DEMOCRATIC REPUBLIC OF THE CONGO', 'CENTRAL AFRICAN REPUBLIC', 'CHINA HONG KONG SAR', 'SWAZILAND', 'VIET NAM', 'BRUNEI DARUSSALAM', 'TURKS AND CAICOS ISLANDS', 'SAINT VINCENT AND THE GRENADINES', 'CHINA MACAO SAR', 'FALKLANDS ISLANDS MALVINAS', 'HOLY SEE', 'SAINT BARTHELEMY', 'SAINT PEIRRE AND MIQUELON']
        cust_dict = {'USA': 'US', 'UAE': 'UNITED-ARAB-EMIRATES', 'IVORY COAST': 'COTE-D-IVOIRE', 'CZECHIA': 'CZECH REPUBLIC', 'S. KOREA': 'SOUTH KOREA', 'PALESTINE': 'STATE OF PALESTINE', 'NORTH MACEDONIA': 'MACEDONIA', 'DRC': 'DEMOCRATIC REPUBLIC OF THE CONGO', 'CAR': 'CENTRAL AFRICAN REPUBLIC', 'HONG KONG': 'CHINA HONG KONG SAR', 'ESWATINI': 'SWAZILAND', 'VIETNAM': 'VIET NAM', 'BRUNEI': 'BRUNEI-DARUSSALAM', 'TURKS AND CAICOS': 'TURKS AND CAICOS ISLANDS', 'ST. VINCENT GRENADINES': 'SAINT VINCENT AND THE GRENADINES', 'MACAO': 'CHINA MACAO SAR', 'FALKLANDS ISLANDS': 'FALKLANDS ISLANDS MALVINAS', 'VATICAN CITY': 'HOLY SEE', 'ST. BARTH': 'SAINT BARTHELEMY', 'SAINT PEIRRE MIQUELON': 'SAINT PEIRRE AND MIQUELON'}

        if new_row:
            if name.upper() in new_row:
                if name.upper() in cust_dict:
                    return url+str(cust_dict[name.upper()].replace(' ','-'))
                else:
                    return location
            elif name.upper() in customs:
                return url+name.replace(' ','-').lower()
            else:
                return False
        else:
            return False

    except Exception as e:
        print(e)
        return False