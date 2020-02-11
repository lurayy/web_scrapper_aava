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
    }
    info_grid = driver.find_element_by_id('SearchResultsGrid')
    page_info_tr_element = driver.find_element_by_class_name('DotNetPager')
    current_page = get_active_page_number(driver)
    pages = page_info_tr_element.find_elements_by_tag_name('a')
    for page in pages:
        try:
            page_data[int(page.text)] = page
        except:
            page_data[0] = page
    return page_data


'''calculates and clicks on the next page'''
def next_page(page_data, driver):
    current_page = get_active_page_number(driver)
    print(page_data.keys())
    for i in page_data.keys():
        if current_page < i:
            page_data[i].click()
            print('----- Clicked on page : ',i, '------------------')
            return True
    try:
        page_data[0].click()
        print('----- Clicked on page : ',"NEXT", '------------------')
        return True
    except:
        pass
    print('############################### NO NEXT PAGE ############################')
    return False
        



def get_active_page_number(driver):
    temp_s = driver.find_element_by_id('SearchResultsGrid')
    temp_s = temp_s.find_element_by_class_name('DotNetPager')
    temp_s = temp_s.find_element_by_tag_name('b').text
    return int(temp_s)