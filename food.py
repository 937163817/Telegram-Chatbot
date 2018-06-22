import re

def parse_shop_information(shop_link):
    shop_id = re.sub(re.compile(r'^.*/' + SHOP_PATH), '', shop_link).split('-')[0]
    print(shop_id)

    req = requests.get(shop_link)
    if req.status_code == requests.codes.ok:
        soup = BeautifulSoup(req.content, HTML_PARSER)
        shop_header_tag = soup.find('div', id='shop-header')
        name_tag = shop_header_tag.find('span', attrs={'itemprop': 'name'})
        print(re.sub(SPACE_RE, '', name_tag.text))
        category_tag = shop_header_tag.find("p", class_={'cate i'})
        print(re.sub(SPACE_RE, '', category_tag.a.text))
        address_tag = shop_header_tag.find('a', attrs={'data-label': '上方地址'})
        print(re.sub(SPACE_RE, '', address_tag.text))
        
        gps_str = address_tag['href']
        # print(gps_str)
        gps_str = re.search('/c=(\d+.\d*),(\d+.\d*)/', gps_str).group().replace('/', '')
        # print(gps_str)
        lat = gps_str.split(',')[0]
        lng = gps_str.split(',')[1]
        print(lat.split('=')[1], lng)

elif first_chat_text == 'food':
                    magnito_bot.send_message(first_chat_id, 'Input place : ')
                    new_offset = first_update_id + 1
                    updates=magnito_bot.get_updates(new_offset)
                    if len(updates) > 0:
                        for current_update in updates:
                            if 'text' not in current_update['message']:
                                first_chat_text='New member'
                            else:
                                first_chat_text = current_update['message']['text']
                                
                    #magnito_bot.send_message(first_chat_id,first_chat_text)
                    LIST_URL = 'http://www.ipeen.com.tw/search/'+first_chat_text+'/000/1-0-0-0/'
                    
                    list_req = requests.get(LIST_URL)
                    if list_req.status_code == requests.codes.ok:
                        soup = BeautifulSoup(list_req.content, HTML_PARSER)
                        shop_links_a_tags = soup.find_all('a', attrs={'data-label': '店名'})

                        shop_links = []
                        for link in shop_links_a_tags:
                            shop_link = ROOT_URL + link['href']
                            #print(shop_link)
                            magnito_bot.send_message(first_chat_id,shop_link)
                            shop_links.append(shop_link)
                            parse_shop_information(shop_link)
                    new_offset = first_update_id + 1
                    
                else:
                    magnito_bot.send_message(first_chat_id, 'Enter another instruction╰(*°▽°*)╯')
                    new_offset = first_update_id + 1
                    
   
