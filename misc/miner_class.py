from selenium import webdriver
import threading
import json

'''Miner class to do mining using multi thread for better performance'''
class Miner(threading.Thread):

    '''init fucntion'''
    def setup(self, website):
        self.website = website

    '''main fucntion'''
    def run(self):
        website = self.website
        print('mining on ', self.website)
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
            try:
                texts = child_driver.find_element_by_class_name('big').text
            except:
                print('error on ',website,' cannot find big')
                child_driver.quit()
                self.process_data({'status':0,'data':'cannot find big'})
                print('quit on : ',self.website)
                return

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
            self.process_data({'data':employee_json, 'status':1})
        except:
            print('error on ',website, ' cannot load site or smth in the main loop')
            child_driver.quit()
            self.process_data({'status':0, 'data':' cannot load site or smth in the main loop'})

    
    '''process the yeild'''
    def process_data(self, response_json):
        if response_json['status']:
            self.save_data(response_json['data'])
        else:
            self.add_on_error_list()

    '''save the mined data, if mining is successful'''
    def save_data(self, data):
        print('saving data for ',self.website)
        with open('data/output_json.json', 'a') as output_file:
            json.dump(data, output_file)
            output_file.write(',')
        
    '''if error occurs, this function will save the link to error_list.json'''
    def add_on_error_list(self):
        with open('data/error_list.json', 'a') as output_file:
            json.dump(self.website, output_file)
