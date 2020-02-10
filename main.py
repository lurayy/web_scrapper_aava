from selenium import webdriver
import json 
import time

# MAIN_SITE = 'https://aava.site-ym.com/search/newsearch.asp'
URL = "https://aava.site-ym.com/searchserver/people.aspx?id=442E05AF-6FBE-4AF3-8239-2355D016EF90&cdbid=&canconnect=0&canmessage=0&map=True&toggle=False&hhSearchTerms="


def mine_data(website):
    print('mining')
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    child_driver = webdriver.Chrome('/home/lurayy/chromedriver', chrome_options=options)
    # child_driver = webdriver.Chrome('/home/lurayy/chromedriver')
    try:
        child_driver.get(website)

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
        texts = child_driver.find_element_by_class_name('big').text
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
            info_section = child_driver.find_elements_by_class_name('ViewTable1')
            for info in info_section:
                links = info.find_elements_by_tag_name('a')
                for link in links:
                    if (link.get_attribute('href').__contains__('mailto:')):
                        email = link.text
        except:
            pass
        employee_json['email'] = str(email)
        

        #address zip
        info_section = child_driver.find_element_by_id('tdEmployerName')
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
            phone_element = child_driver.find_element_by_id('tdWorkPhone')
            try:
                phone = str(phone_element.text).split('(Phone)')[0]
                employee_json['phone'] = phone
            except:
                employee_json['phone'] = str(phone.text)
        except:
            employee_json['phone'] = ''
            child_driver.quit()
        return {'data':employee_json, 'status':1}
            
    except:
        print('error on ',website)
        child_driver.quit()
        return {'status':0}
    finally:
        child_driver.quit()
    

def get_links(driver):
    member_links = []
    list_of_docs = driver.find_elements_by_class_name('lineitem')
    for doc in list_of_docs:
        try:
            link_element = (doc.find_element_by_tag_name('a'))
            member_links.append(link_element.get_attribute('href'))
        except:
            pass
    return(member_links)
    

def get_page_list(driver):
    print('getting page list')
    page_data = {
        'current_page':0,
        'other_pages':[]
    }
    info_grid = driver.find_element_by_id('SearchResultsGrid')
    page_info_tr_element = driver.find_element_by_class_name('DotNetPager')
    current_page = page_info_tr_element.find_element_by_tag_name('b').text
    page_data['current_page'] = int(current_page)
    pages = page_info_tr_element.find_elements_by_tag_name('a')
    #for sorting the pages just in case
    for page in pages:
        temp_page = {
        'id':0,
        'element':''
        }
        try:
            temp_page['id'] = int(page.text)
        except:
            temp_page['id'] = 999999999999
        temp_page['element'] = page
        page_data['other_pages'].append(temp_page)
    return page_data


def mine_main(driver):
    output = []
    error_list = []
    time.sleep(10)
    member_links = get_links(driver)
    for member_link in member_links:
        print('Mining on : ',member_link)
        response_json = mine_data(member_link)
        if response_json['status']:
            output.append(response_json['data'])
            print(response_json['data'])
        else:
            error_list.append(member_link)
    return (output, error_list)


def save_data(output, error_list):
    print('saving data')
    with open('data/output_json.json', 'a') as output_file:
            json.dump(temp_output, output_file)

    with open('data/error_list.json', 'a') as output_file:
        json.dump(error_list, output_file)


def next_page(page_data, driver):
    for i in range(len(page_data['other_pages'])):
        if page_data['current_page'] < page_data['other_pages'][i]['id']:
            print('clicking')
            page_data['other_pages'][i]['element'].click()
            print('clicked')
            return True
        print('caluclating')
    return False

if __name__ == "__main__":
    # options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # driver = webdriver.Chrome('/home/lurayy/chromedriver', chrome_options=options)
    driver = webdriver.Chrome('/home/lurayy/chromedriver')
    driver.get(URL)


    page_data = get_page_list(driver)
    state = True
    
    while state:
        print('Mining on page number: ',page_data['current_page'])
        output, error_list = mine_main(driver)
        page_data = get_page_list(driver)
        state = next_page(page_data, driver)

    driver.close()

    # print(temp_output)

    
# firstname, lastname, fullname, title,email, website,
#  address, city, state,country, zip, , phone ,