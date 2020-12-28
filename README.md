# Web scraping using scrapy

## Database Setup
MongoDB setup [watch this video](https://www.youtube.com/watch?v=djfnjtYB2co&list=PLhTjy8cBISEqkN-5Ku_kXG4QW33sxQo0t&index=18)

## Python setup

Python installation instruction [click here](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu)

For creating and activating virtual environment [click here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments)

## Project setup

After activating virtual environment then
```
$ pip3 install -r requirements.txt
```

## Running Spider
```
$ cd ws_moneycontrol/ws_moneycontrol
```
### scrap indian stock market data
```
$ scrapy crawl indian_stocks
```

### scrap international stock market data
```
$ scrapy crawl global_stocks
```

### scrap top performers data in mutual fund
```
$ scrapy crawl mutual_fund
```
