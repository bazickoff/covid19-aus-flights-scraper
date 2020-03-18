# COVID-19 Flights Tracker

This project aims at automating getting data from various Australian State Government Websites to report on flights which a confirmed case of COVID-19 has been on.

The latest dataset for each state is available at:

- [New South Wales](./flight_data/nsw/latest.csv)
- [South Australia](./flight_data/sa/latest.csv)
- [Western Australia](./flight_data/wa/latest.csv)

- [All (Compiled)](./flight_data/all/latest.csv)

This dataset automatically updates every second hour (0:00, 2:00, 4:00, 8:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00), which is equivalent to:

- 10:00am [Australian Eastern Standard Time (AEST)](https://www.timeanddate.com/time/zones/aest)
- 11:00am [Australian Eastern Daylight Time/Daylight Savings Time (AEST)](https://www.timeanddate.com/time/zones/aedt)

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
