'''get all the profile's link from the page'''
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


'''get the attached pages'''
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


'''calculates and clicks on the next page'''
def next_page(page_data, driver):
    for i in range(len(page_data['other_pages'])):
        if page_data['current_page'] < page_data['other_pages'][i]['id']:
            page_data['other_pages'][i]['element'].click()
            print('---- Clicked on page : ',page_data['other_pages'][i]['id'])
            return True
    return False
