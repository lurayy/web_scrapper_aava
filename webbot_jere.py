from selenium import webdriver
# from bs4 import BeautifulSoup
URL = "https://aava.site-ym.com/searchserver/people.aspx?id=88D26135-6899-4AB1-998E-455D0D07FEF3&cdbid=&canconnect=0&canmessage=0&map=True&toggle=False&hhSearchTerms="


def get_links(driver):
    list_of_docs = driver.find_elements_by_class_name('lineitem')
    for doc in list_of_docs:
        try:
            link_element = (doc.find_element_by_tag_name('a'))
            print(link_element.get_attribute('href'))
        except:
            pass
    
def next_page(driver):
    next_page_section = driver.find_element_by_class_name('DotNetPager')
    page_list = next_page_section.find_elements_by_tag_name('a')
    x = len(page_list)
    print(x)
    page_list[9].click()

if __name__ == "__main__":
    driver = webdriver.Chrome('/home/lurayy/chromedriver')
    driver.get(URL)
    next_page(driver)
    # driver.close()
