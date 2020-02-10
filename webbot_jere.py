from selenium import webdriver
# from bs4 import BeautifulSoup
URL = "https://aava.site-ym.com/searchserver/people.aspx?id=88D26135-6899-4AB1-998E-455D0D07FEF3&cdbid=&canconnect=0&canmessage=0&map=True&toggle=False&hhSearchTerms="

temp = 'https://aava.site-ym.com/members/?id=61051743'



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



def mine_data(driver, website):
    driver.get(website)
    employee_json = {
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
        'phone':''
    }   
    employee_json['website'] = website
    texts = driver.find_element_by_class_name('big').text
    texts = str(texts).split(',')[0]
    employee_json['full_name'] = str(texts)
    texts = str(texts).split(' ')
    if texts[0].__contains__('.'):
        employee_json['title'] = str(texts[0]).strip()
        employee_json['first_name'] = (texts[1]).strip()
    else:
        employee_json['first_name'] = texts[0].strip()
    employee_json['last_name'] = texts[len(texts)-1]
    

    #find email
    email = ''
    try:
        info_section = driver.find_elements_by_class_name('ViewTable1')
        for info in info_section:
            links = info.find_elements_by_tag_name('a')
            for link in links:
                if (link.get_attribute('href').__contains__('mailto:')):
                    email = link.text
    except:
        pass
    employee_json['email'] = str(email)
    

    #address zip
    info_section = driver.find_element_by_id('tdEmployerName')
    texts = str(info_section.text).split('\n')
    if texts[len(texts)-1].__contains__("[ Map ]"):
        texts.pop()
    space = ' '
    addresss = space.join(texts)
    employee_json['address'] = addresss

    links = info_section.find_elements_by_tag_name('a')
    for link in links:
        link_text = (link.get_attribute('href'))
        if link_text.__contains__('city'):
            employee_json['city'] = str(link.text).strip()
        if link_text.__contains__('state'):
            employee_json['state'] = str(link.text).strip()
        if link_text.__contains__('country'):
            employee_json['country'] = str(link.text).strip()
            for text in texts:
                if text.__contains__(str(link.text)):
                    temp = text.split(link.text)
                    employee_json['zip'] = str(temp[0]).strip()

    #phone
    try:
        phone_element = driver.find_element_by_id('tdWorkPhone')
        try:
            phone = str(phone_element.text).split('(Phone)')[0]
            employee_json['phone'] = phone
        except:
            employee_json['phone'] = str(phone.text)
    except:
        employee_json['phone'] = ''
    return employee_json
        

if __name__ == "__main__":
    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome('/home/lurayy/chromedriver', chrome_options=options)



    # get_links
    data = mine_data(driver, temp)
    print(data)
    # next_page(driver)
    driver.close()

# firstname, lastname, fullname, title,email, website,
#  address, city, state,country, zip, , phone ,