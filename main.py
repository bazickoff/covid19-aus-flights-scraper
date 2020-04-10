import csv
import os
import re
import json
from datetime import datetime
from datetime import timedelta

import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        pass

    def get_data(self, table):
        rows = []
        trs = table.find_all('tr')
        headerow = [td.get_text(strip=True)
                    for td in trs[0].find_all('th')]  # header row
        if headerow:  # if there is a header row include first
            rows.append(headerow)
            trs = trs[1:]
        for tr in trs:  # for every table row
            rows.append([td.get_text('',
                                     strip=True).strip('\u200b')
                         for td in tr.find_all('td')])  # data row
        return rows

    def get_html(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def get_nsw_flight_data(self):
        data_url = "https://www.health.nsw.gov.au/Infectious/diseases/Pages/coronavirus-flights.aspx"
        table = self.get_html(data_url).find('table', class_="moh-rteTable-6")
        return self.get_data(table)

    def get_sa_flight_data(self):
        data_url = "https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/health+topics/health+topics+a+-+z/covid+2019/latest+updates/known+flights+with+confirmed+cases+of+covid-19"
        middle_column = self.get_html(data_url).find(
            'div', class_="middle-column")
        table = middle_column.find('table')
        return self.get_data(table)

    def get_wa_flight_data(self):
        target_url = "https://healthywa.wa.gov.au/Articles/A_E/Coronavirus/Locations-visited-by-confirmed-cases"
        content = self.get_html(target_url).find('div', id="contentText")
        table = content.find('table')
        return self.get_data(table)

    def get_qld_flight_data(self):
        target_url = "https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/current-status-and-contact-tracing-alerts"
        table = self.get_html(target_url).find('table', id="table54931")
        return self.get_data(table)

    def get_nt_flight_data(self):
        target_url = 'https://coronavirus.nt.gov.au/home/homepage-news/contact-tracing'
        table = self.get_html(target_url).find(
            'table', class_="au-table au-table--striped")
        rows = []
        header = table.find_all('thead')[0]
        headerow = [td.get_text(strip=True)
                    for td in header.find_all('th')]  # header row
        if(headerow):
            rows.append(headerow)

        tablebody = table.find_all('tbody')[0]
        trs = tablebody.find_all('tr')
        for tr in trs:  # for every table row
            rows.append([td.get_text('',
                                     strip=True).strip('\u200b')
                         for td in tr.find_all('td')])  # data row
        return rows

    def get_act_flight_data(self):
        target_url = 'https://www.health.act.gov.au/about-our-health-system/novel-coronavirus-covid-19/known-flights-act-confirmed-cases-covid-19'
        inner_content = self.get_html(target_url).find(text="Known flights")
        table = inner_content.findNext('table')
        return self.get_data(table)

    def get_static_data(self, state):
        target_uri = f'./flight_data/{state}/latest.csv'
        data = []
        with open(target_uri) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)
            for row in csv_reader:
                flight = {
                    'airline': row[0],
                    'flight_number': row[1],
                    'origin': row[2],
                    'destination': row[3],
                    'arrival_date': datetime.strptime(row[4], '%a %d %B %Y'),
                    'symptoms_onset_date': row[5],
                    'close_contact_rows': row[6],
                    'reporting_state': state.upper(),
                }
                data.append(flight)
        return data

    def get_global_data(self):
        nsw_flight_data = self.get_nsw_flight_data()
        sa_flight_data = self.get_sa_flight_data()
        wa_flight_data = self.get_wa_flight_data()
        qld_flight_data = self.get_qld_flight_data()
        nt_flight_data = self.get_nt_flight_data()
        act_flight_data = self.get_act_flight_data()

        data = []
        current_timestamp = datetime.now()

        for row in nsw_flight_data[1:]:
            if(row[0] != ''):
                flight_number = row[0]
                arrival_date = datetime.strptime(row[4].strip(" "), '%d %B %Y')
                symptoms_onset_date = arrival_date + timedelta(days=14)
                close_contact_rows = row[5].replace(
                    '\xa0', ',').replace('\r\n', '&')

                airline = row[1]
                flight_path = row[2].split('/')
                # print(flight_path)
                if(len(flight_path) == 3):
                    origin = f'{flight_path[0]} (via {flight_path[1]})'
                    destination = f'{flight_path[2]}'
                else:
                    if ' to ' in row[2]:
                        flight_path = row[2].split(' to ')
                    origin = flight_path[0]
                    destination = flight_path[1]

                flight = {'airline': airline, 'flight_number': flight_number, 'origin': origin, 'destination': destination, 'arrival_date': arrival_date,
                          'close_contact_rows': close_contact_rows, 'reporting_state': 'NSW', 'symptoms_onset_date': symptoms_onset_date.strftime('%a %d %B %Y')}
                data.append(flight)

        for row in sa_flight_data[1:]:
            flight_number = row[0]

            date_str = row[3].split('/')
            day = date_str[0]
            month = date_str[1]
            year = '2020'  # hard-coded

            airline = row[1]

            flight_path = row[2]
            if '–' in flight_path:
                [origin, destination] = flight_path.split(' – ')
            elif '-' in flight_path:
                [origin, destination] = flight_path.replace(
                    u'\xa0', u' ').split(' - ')
            else:
                [origin, destination] = ['', '']

            final_date_str = f'{day.zfill(2)} {month.zfill(2)} {year}'

            arrival_date = datetime.strptime(final_date_str, '%d %m %Y')
            symptoms_onset_date = arrival_date + timedelta(days=14)
            close_contact_rows = ''
            flight = {'airline': airline, 'flight_number': flight_number, 'origin': origin, 'destination': destination, 'arrival_date': arrival_date,
                      'close_contact_rows': close_contact_rows, 'reporting_state': 'SA', 'symptoms_onset_date': symptoms_onset_date.strftime('%a %d %B %Y')}

            data.append(flight)

        for row in wa_flight_data[1:]:
            flight_number = row[0]
            arrival_date = row[3]
            arrival_date = datetime.strptime(row[3], '%d/%m/%Y')

            airline = row[1]
            [origin, destination] = row[2].split(' to ')

            symptoms_onset_date = arrival_date + timedelta(days=14)
            close_contact_rows = row[4]
            flight = {'airline': airline, 'flight_number': flight_number, 'origin': origin, 'destination': destination, 'arrival_date': arrival_date,
                      'close_contact_rows': close_contact_rows, 'reporting_state': 'WA', 'symptoms_onset_date': symptoms_onset_date.strftime('%a %d %B %Y')}

            data.append(flight)

        for row in qld_flight_data[1:]:
            if(row[0] != ''):
                flight_number = row[0]
                airline = row[1]
                date = row[4].split('-')
                arrival_date = datetime.strptime(
                    row[4], '%d-%b-%y')
                symptoms_onset_date = arrival_date + timedelta(days=14)
                close_contact_rows = ''

                origin, destination = row[2], row[3]

                flight = {'airline': airline, 'flight_number': flight_number, 'origin': origin, 'destination': destination, 'arrival_date': arrival_date,
                          'close_contact_rows': close_contact_rows, 'reporting_state': 'QLD', 'symptoms_onset_date': symptoms_onset_date.strftime('%a %d %B %Y')}
                data.append(flight)

        for row in nt_flight_data[1:]:
            arrival_date = datetime.strptime(row[0], '%d %B %Y')
            symptoms_onset_date = arrival_date + timedelta(days=14)
            [flight_number, airline] = row[1].split(' - ')
            [origin, destination] = row[2].split(' to ')

            flight = {'airline': airline, 'flight_number': flight_number, 'origin': origin, 'destination': destination, 'arrival_date': arrival_date,
                      'close_contact_rows': close_contact_rows, 'reporting_state': 'NT', 'symptoms_onset_date': symptoms_onset_date.strftime('%a %d %B %Y')}
            data.append(flight)

        for row in act_flight_data[1:]:
            date = row[4].split('-')
            if(len(date) == 2):
                arrival_date = datetime.strptime(f'{row[4]}-2020', '%d-%b-%Y')
            else:
                arrival_date = datetime.strptime(f'{row[4]}-2020', '%d %B-%Y')

            symptoms_onset_date = arrival_date + timedelta(days=14)

            flight_number = row[0]

            airline = row[1]
            close_contact_rows = row[5]
            flight_path = row[2].split('/')
            if(len(flight_path) == 3):
                origin = f'{flight_path[0]} (via {flight_path[1]})'
                destination = f'{flight_path[2]}'
            elif 'to' in row[2]:
                flight_path = row[2].split(' to ')
                origin = f'{flight_path[0]}'
                destination = f'{flight_path[1]}'
            else:
                origin = f'{flight_path[0]}'
                destination = f'{flight_path[1]}'

            flight = {'airline': airline, 'flight_number': flight_number, 'origin': origin, 'destination': destination, 'arrival_date': arrival_date,
                      'close_contact_rows': close_contact_rows, 'reporting_state': 'ACT', 'symptoms_onset_date': symptoms_onset_date.strftime('%a %d %B %Y')}
            data.append(flight)

        data += self.get_static_data('vic')

        data = sorted(data, key=lambda x: x['arrival_date'], reverse=True)

        for flight in data:
            flight['arrival_date'] = flight['arrival_date'].strftime(
                '%a %d %B %Y')
        return data


if __name__ == "__main__":
    scraper = Scraper()
    nsw_flight_data = scraper.get_nsw_flight_data()
    sa_flight_data = scraper.get_sa_flight_data()
    wa_flight_data = scraper.get_wa_flight_data()
    qld_flight_data = scraper.get_qld_flight_data()
    nt_flight_data = scraper.get_nt_flight_data()
    act_flight_data = scraper.get_act_flight_data()
    combined_flight_data = scraper.get_global_data()

    current_timestamp = datetime.now()

    if not os.path.exists('./flight_data'):
        os.makedirs('./flight_data')
    states = ['nsw', 'sa', 'wa', 'qld', 'nt', 'act']

    for state in states:
        if not os.path.exists(f'./flight_data/{state}'):
            os.makedirs(f'./flight_data/{state}')

    if not os.path.exists('./flight_data/all'):
        os.makedirs('./flight_data/all')

    if not os.path.exists('./json/all'):
        os.makedirs('./json/all')

    today = f"{current_timestamp.year}-{current_timestamp.month}-{current_timestamp.day}"
    with open(f'./flight_data/nsw/flights_{today}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(nsw_flight_data)
    with open(f'./flight_data/nsw/latest.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(nsw_flight_data)

    with open(f'./flight_data/sa/flights_{today}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sa_flight_data)
    with open(f'./flight_data/sa/latest.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sa_flight_data)

    with open(f'./flight_data/wa/flights_{today}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(wa_flight_data)
    with open(f'./flight_data/wa/latest.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(wa_flight_data)

    with open(f'./flight_data/qld/flights_{today}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(qld_flight_data)
    with open(f'./flight_data/qld/latest.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(qld_flight_data)

    with open(f'./flight_data/nt/flights_{today}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(nt_flight_data)
    with open(f'./flight_data/nt/latest.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(nt_flight_data)

    with open(f'./flight_data/act/flights_{today}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(act_flight_data)
    with open(f'./flight_data/act/latest.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(act_flight_data)

    header = ['airline', 'flight_number',  'origin', 'destination', 'arrival_date', 'symptoms_onset_date',
              'close_contact_rows', 'reporting_state']

    with open(f'./flight_data/all/flights_{today}.csv', 'w', newline='') as file:
        writer = csv.DictWriter(
            file, header)
        writer.writeheader()
        writer.writerows(combined_flight_data)

    with open(f'./flight_data/all/latest.csv', 'w', newline='') as file:
        writer = csv.DictWriter(
            file, header)
        writer.writeheader()
        writer.writerows(combined_flight_data)

    with open(f'./json/all/latest.json', 'w') as file:
        json.dump(combined_flight_data, file, sort_keys=True,  indent=2)
