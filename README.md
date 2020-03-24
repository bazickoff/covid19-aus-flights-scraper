# COVID-19 Flights Tracker

This project aims at automating getting data from various Australian State Government Websites to report on flights which a confirmed case of COVID-19 has been on.

The latest dataset for each state is available at:

- [New South Wales](./flight_data/nsw/latest.csv)
- [South Australia](./flight_data/sa/latest.csv)
- [Western Australia](./flight_data/wa/latest.csv)
- [Queensland](./flight_data/qld/latest.csv)
- [Nothern Territory](./flight_data/nt/latest.csv)
- [Australian Capital Territory](./flight_data/act/latest.csv)

## Static Data

- [Victoria](./flight_data/vic/latest.csv)

## Other Datasets

- [All (Compiled)](./flight_data/all/latest.csv)

This dataset automatically updates every second hour in UTC time (0:00, 2:00, 4:00, 8:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00), which is equivalent to:

- (10am, 12pm, 2pm, 4pm, 6pm, 8pm, 10pm, 12am, 2am, 4am, 8am) [Australian Eastern Standard Time (AEST)](https://www.timeanddate.com/time/zones/aest)
- (11am, 1pm, 3pm, 5pm, 7pm, 9pm, 11pm, 1am, 3am, 5am, 7am, 9am) [Australian Eastern Daylight Time/Daylight Savings Time (AEST)](https://www.timeanddate.com/time/zones/aedt)

## Data Sources

The data is sourced from various health departments in each state of Australia:

- NSW Department of Health: [Known flights with confirmed cases of COVID-19](https://www.health.nsw.gov.au/Infectious/diseases/Pages/coronavirus-flights.aspx)
- SA Health: [Known flights with confirmed cases of COVID-19](https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/health+topics/health+topics+a+-+z/covid+2019/latest+updates/known+flights+with+confirmed+cases+of+covid-19)
- WA Department of Health: [Locations visited by confirmed cases](https://healthywa.wa.gov.au/Articles/A_E/Coronavirus/Locations-visited-by-confirmed-cases)
- Queensland Department of Health: [Current status and contact tracing alerts](https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/current-status-and-contact-tracing-alerts)
- NT Government: [Contact tracing](https://coronavirus.nt.gov.au/home/homepage-news/contact-tracing)
- ACT Health: [Known flights with ACT confirmed cases of COVID-19](https://www.health.act.gov.au/about-our-health-system/novel-coronavirus-covid-19/known-flights-act-confirmed-cases-covid-19)

### Note for Victorian Data

As of 14th March 2020, the Victorian Department of Health and Human Services (Vic DHHS) has stopped reporting official location history for each suspected case. As such, data of flights for each confirmed case will not be available and require manual updates.

# API Layer

The API layer will be available soon!

# Development

## Installing Dependencies

To install dependencies, simply run:

```bash
pip install -r requirements.txt
```

or if you are using pip3 as an alias

```bash
pip3 install -r requirements.txt
```

## Running the Script

After install the dependencies, simply run:

```bash
python3 main.py
```

# LICENSE

This project is licensed under MIT. See [LICENSE](./LICENSE) for more details
