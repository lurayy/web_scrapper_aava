from selenium import webdriver
import json 

URL = "https://aava.site-ym.com/searchserver/people.aspx?id=88D26135-6899-4AB1-998E-455D0D07FEF3&cdbid=&canconnect=0&canmessage=0&map=True&toggle=False&hhSearchTerms="


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
    

def next_page(driver):
    next_page_section = driver.find_element_by_class_name('DotNetPager')
    page_list = next_page_section.find_elements_by_tag_name('a')
    x = len(page_list)
    print(x)
    page_list[9].click()



def mine_data(website):
    # options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # child_driver = webdriver.Chrome('/home/lurayy/chromedriver', chrome_options=options)
    child_driver = webdriver.Chrome('/home/lurayy/chromedriver')
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
        

if __name__ == "__main__":
    
    # options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # driver = webdriver.Chrome('/home/lurayy/chromedriver', chrome_options=options)
    driver = webdriver.Chrome('/home/lurayy/chromedriver')
    driver.get(URL)

    temp_output = []
    error_list = []
    member_links = get_links(driver)
    
    for member_link in member_links:
        response_json = mine_data(member_link)
        if response_json['status']:
            temp_output.append(response_json['data'])
        else:
            error_list.append(member_link)
        
    driver.close()

    print(temp_output)

    with open('output_json.json', 'w') as output_file:
        json.dump(temp_output, output_file)

    with open('error_list.json', 'w') as output_file:
        json.dump(error_list, output_file)

# firstname, lastname, fullname, title,email, website,
#  address, city, state,country, zip, , phone ,