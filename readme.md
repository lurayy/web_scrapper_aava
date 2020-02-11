# Simple Web Scrapper
### How to use:

1. Install python3 
2. Install requirements
```
pip3 install -r requirements.txt 
```
3.Install and configure selenium

```
check your chrome version :->About Chrome 
https://sites.google.com/a/chromium.org/chromedriver/downloads
```
4. Use settings.py to set URL and number of threads
5. Use converter.py for converting .json file to .csv

### Structure of collected data
```
{
    'first_name':'',
    'last_name':'',
    'full_name':'',
    'title':'',
    'email':'',
    'website':'',
    'address':'',
    'city':'',
    'state':'',
    'country':'',
    'zip':'',
    'phone':'',
}
```
