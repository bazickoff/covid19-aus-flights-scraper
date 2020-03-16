import requests
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime


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
            rows.append([td.get_text(strip=True).strip('\u200b')
                         for td in tr.find_all('td')])  # data row
        return rows

    def get_nsw_flight_data(self):
        nsw_flights_url = "https://www.health.nsw.gov.au/Infectious/diseases/Pages/coronavirus-flights.aspx"
        page = requests.get(nsw_flights_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', class_="moh-rteTable-6")
        return self.get_data(table)

    def get_sa_flight_data(self):
        nsw_flights_url = "https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/health+topics/health+topics+a+-+z/covid+2019/latest+updates/known+flights+with+confirmed+cases+of+covid-19"
        page = requests.get(nsw_flights_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        middle_column = soup.find('div', class_="middle-column")
        table = middle_column.find('table')
        return self.get_data(table)

    def get_wa_flight_data(self):
        target_url = "https://healthywa.wa.gov.au/Articles/A_E/Coronavirus/Locations-visited-by-confirmed-cases"
        page = requests.get(target_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.find('div', id="contentText")
        table = content.find('table')
        return self.get_data(table)

    def get_global_data(self):
        nsw_flight_data = self.get_nsw_flight_data()
        sa_flight_data = self.get_sa_flight_data()
        wa_flight_data = self.get_wa_flight_data()

        data = []

        for row in nsw_flight_data[1:]:
            flight_number = row[0]
            arrival_date = datetime.strptime(row[4], '%d %B %Y')
            symptoms_onset_date = arrival_date + datetime.timedelta(days=14)
            close_contact_rows = row[5]
            flight = {'flight_number': flight_number, 'arrival_date': arrival_date,
                      'close_contact_rows': close_contact_rows, 'reporting_state': 'NSW', 'symptoms_onset_date': symptoms_onset_date}
            data.append(flight)

        for row in sa_flight_data[1:]:
            flight_number = row[1].split(' ')[0]
            arrival_date = datetime.strptime(row[3], '%d %B %Y')
            symptoms_onset_date = arrival_date + datetime.timedelta(days=14)
            close_contact_rows = ''
            flight = {'flight_number': flight_number, 'arrival_date': arrival_date,
                      'close_contact_rows': close_contact_rows, 'reporting_state': 'SA', 'symptoms_onset_date': symptoms_onset_date}
            data.append(flight)

        for row in wa_flight_data[1:]:
            flight_number = row[0]
            arrival_date = row[3]
            arrival_date = datetime.strptime(row[3], '%d/%m/%Y')
            symptoms_onset_date = arrival_date + datetime.timedelta(days=14)
            close_contact_rows = row[4]
            flight = {'flight_number': flight_number, 'arrival_date': arrival_date,
                      'close_contact_rows': close_contact_rows, 'reporting_state': 'WA', 'symptoms_onset_date': symptoms_onset_date}
            data.append(flight)

        return data


if __name__ == "__main__":
    scraper = Scraper()
    nsw_flight_data = scraper.get_nsw_flight_data()
    sa_flight_data = scraper.get_sa_flight_data()
    wa_flight_data = scraper.get_wa_flight_data()

    combined_flight_data = scraper.get_global_data()

    current_timestamp = datetime.now()

    if not os.path.exists('./flight_data'):
        os.makedirs('./flight_data')
    if not os.path.exists('./flight_data/nsw'):
        os.makedirs('./flight_data/nsw')
    if not os.path.exists('./flight_data/sa'):
        os.makedirs('./flight_data/sa')
    if not os.path.exists('./flight_data/wa'):
        os.makedirs('./flight_data/wa')

    if not os.path.exists('./flight_data/all'):
        os.makedirs('./flight_data/all')

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

    header = ['reporting_state', 'arrival_date', 'symptoms_onset_date',
              'flight_number', 'close_contact_rows']

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
