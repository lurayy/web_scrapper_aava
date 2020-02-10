import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# URL = "https://aava.site-ym.com/search/newsearch.asp"
main_data_url = "https://aava.site-ym.com/searchserver/people.aspx?id=88D26135-6899-4AB1-998E-455D0D07FEF3&cdbid=&canconnect=0&canmessage=0&map=True&toggle=False&hhSearchTerms="
response = requests.get(main_data_url)

print(response)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())