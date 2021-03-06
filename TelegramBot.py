
import requests
import datetime
import sports_py
import speech_recognition as sr
import telebot
import re
import time

from icrawler.builtin import GoogleImageCrawler
from bs4 import BeautifulSoup
from weather import Weather, Unit

class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = '581600809:AAE-g_1zc1qQAd1kYXwT48dHHEVsxU5O-PM' #改成我們的token
magnito_bot = BotHandler(token) #Your bot's name


def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_movies(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    movies = []
    rows = soup.find_all('div', 'release_info_text')
    for row in rows:
        movie = dict()
        #movie['推薦度'] = row.find('div', 'leveltext').span.text.strip()
        movie['ch_name'] = row.find('div', 'release_movie_name').a.text.strip()
        #movie['eng_name'] = row.find('div', 'release_movie_name').find('div', 'en').a.text.strip()
        #movie['release_date'] = get_date(row.find('div', 'release_movie_time').text)
        trailer_a = row.find_next_sibling('div', 'release_btn color_btnbox').find_all('a')[1]
        movie['trailer_url'] = trailer_a['href'] if 'href' in trailer_a.attrs.keys() else ''
        movies.append(movie)
    return movies

def get_date(date_str):
    pattern = '\d+-\d+-\d+'
    match = re.search(pattern, date_str)
    if match is None:
        return date_str
    else:
        return match.group(0)

def get_movie_id(url):
    try:
        movie_id = url.split('.html')[0].split('-')[-1]
    except:
        movie_id = url
    return movie_id

def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html5lib')

    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').text.strip() == date:
            push_count = 0
            push_str = d.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    if push_str == 'burst':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            if d.find('a'):
                href = d.find('a')['href']
                title = d.find('a').text
                author = ''
                articles.append({
                    'title':title,
                    'href':'https://www.ptt.cc'+href,
                    'push_count': push_count,
                })
    return articles, prev_url

def get_author_ids(posts, pattern):
    ids = set()
    for post in posts:
        if pattern in post['author']:
            ids.add(post['author'])
    return ids

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

def main():
    new_offset = 0
    print('hi, now launching...')

    while True:
        all_updates=magnito_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text='New member'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"
				
				magnito_bot.send_message(first_chat_id, first_chat_name + ' start chat with me!')
				
                if first_chat_text == 'Hi':
                    magnito_bot.send_message(first_chat_id, 'Hi ' + first_chat_name )
                    new_offset = first_update_id + 1
				
                elif first_chat_text == 'hi':
                    magnito_bot.send_message(first_chat_id, 'How do you do '+first_chat_name)
                    new_offset = first_update_id + 1 
			
		elif first_chat_text == 'news':
                    magnito_bot.send_message(first_chat_id, '自由時報今日焦點新聞')
                    dom = requests.get('http://news.ltn.com.tw/list/newspaper').text
                    soup = BeautifulSoup(dom, 'html5lib')
                    for ele in soup.find('ul', 'list').find_all('li'):
                        #magnito_bot.send_message(first_chat_id,ele.find('a', 'tit').text.strip())
                        hr='http://news.ltn.com.tw/'+ele.find('a').get('href')
                        #magnito_bot.send_message(first_chat_id,'http://news.ltn.com.tw/')
                        #magnito_bot.send_message(first_chat_id,ele.find('a').get('href'))
                        magnito_bot.send_message(first_chat_id,hr)
                    new_offset = first_update_id + 1

                elif first_chat_text == 'weather':
                    weather = Weather(unit=Unit.CELSIUS)
                    lookup = weather.lookup(560743)
                    condition = lookup.condition
                    weather = Weather(unit=Unit.CELSIUS)
                    magnito_bot.send_message(first_chat_id, 'Input your location : ')

                    new_offset = first_update_id + 1
                    updates=magnito_bot.get_updates(new_offset)
                    if len(updates) > 0:
                        for current_update in updates:
                            if 'text' not in current_update['message']:
                                first_chat_text='New member'
                            else:
                                first_chat_text = current_update['message']['text']
                    #magnito_bot.send_message(first_chat_id,first_chat_text)
                    
                    new_offset = first_update_id + 1
                    local=first_chat_text
                    #local=first_chat_text
                    
                    location = weather.lookup_by_location(local)
                    forecasts = location.forecast
                    for forecast in forecasts:
                        te='Day: '+forecast.date+'| '+forecast.low+'°C~'+forecast.high+'°C'+'| '+forecast.text
                        magnito_bot.send_message(first_chat_id, te)
		
		elif first_chat_text == 'sport':
                    magnito_bot.send_message(first_chat_id, 'Input sports type : ')
                    new_offset = first_update_id + 1
                    updates=magnito_bot.get_updates(new_offset)
                    if len(updates) > 0:
                        for current_update in updates:
                            #if 'text' not in current_update['message']:
                            #    first_chat_text='New member'
                            #else:
                                first_chat_text = current_update['message']['text']
                    
                    matches = sports_py.get_sport_scores(first_chat_text)
                    for match in matches:
                        sp='{} vs {}: {}-{}'.format(match.home_team, match.away_team, match.home_score, match.away_score)
                        magnito_bot.send_message(first_chat_id, sp)

                elif first_chat_text == 'speak':
                    new_offset = first_update_id + 1
                    r=sr.Recognizer() 
                    with sr.Microphone() as source:
                        magnito_bot.send_message(first_chat_id, 'Please wait. Calibrating microphone...')
                        #print("Please wait. Calibrating microphone...") 
                        r.adjust_for_ambient_noise(source, duration=5)
                        magnito_bot.send_message(first_chat_id, 'Say something!')
                        #print("Say something!")
                        audio=r.listen(source)

                    try:
                        magnito_bot.send_message(first_chat_id, 'I think you said:')
                        s_tex = r.recognize_google(audio, language="zh-TW")
                        magnito_bot.send_message(first_chat_id, s_tex)
                        first_chat_text = s_tex
                        if first_chat_text == 'news':
                            magnito_bot.send_message(first_chat_id, '自由時報今日焦點新聞')
                            dom = requests.get('http://news.ltn.com.tw/list/newspaper').text
                            soup = BeautifulSoup(dom, 'html5lib')
                            for ele in soup.find('ul', 'list').find_all('li'):
                                hr='http://news.ltn.com.tw/'+ele.find('a').get('href')
                                magnito_bot.send_message(first_chat_id,hr)
                            new_offset = first_update_id + 1
                        elif first_chat_text == 'weather':
                            weather = Weather(unit=Unit.CELSIUS)
                            lookup = weather.lookup(560743)
                            condition = lookup.condition
                            weather = Weather(unit=Unit.CELSIUS)
                            magnito_bot.send_message(first_chat_id, 'Input your location : ')

                            new_offset = first_update_id + 1
                            updates=magnito_bot.get_updates(new_offset)
                            if len(updates) > 0:
                                for current_update in updates:
                                    if 'text' not in current_update['message']:
                                        first_chat_text='New member'
                                    else:
                                        first_chat_text = current_update['message']['text']
                            new_offset = first_update_id + 1
                            local=first_chat_text

                            location = weather.lookup_by_location(local)
                            forecasts = location.forecast
                            for forecast in forecasts:
                                te='Day: '+forecast.date+'| '+forecast.low+'°C~'+forecast.high+'°C'+'| '+forecast.text
                                magnito_bot.send_message(first_chat_id, te)
                    
                        elif first_chat_text == 'sport':
                            magnito_bot.send_message(first_chat_id, 'Input sports type : ')
                            new_offset = first_update_id + 1
                            updates=magnito_bot.get_updates(new_offset)
                            if len(updates) > 0:
                                for current_update in updates:
                                    first_chat_text = current_update['message']['text']
                            matches = sports_py.get_sport_scores(first_chat_text)
                            for match in matches:
                                sp='{} vs {}: {}-{}'.format(match.home_team, match.away_team, match.home_score, match.away_score)
                                magnito_bot.send_message(first_chat_id, sp)
			elif first_chat_text == 'movie':
                            page = get_web_page('https://tw.movies.yahoo.com/movie_thisweek.html')
                            if page:
                                movies = get_movies(page)
                            for movie in movies:
                                magnito_bot.send_message(first_chat_id,movie['ch_name'])
                                magnito_bot.send_message(first_chat_id,movie['trailer_url'])
                            new_offset = first_update_id + 1
							
                        elif first_chat_text == 'PTT':
                            current_page = get_web_page('https://www.ptt.cc/bbs/Gossiping/index.html')
                            if current_page:
                                articles = []
                                today = time.strftime("%m/%d").lstrip('0')
                                current_articles, prev_url = get_articles(current_page, today)
                                while current_articles:
                                    articles += current_articles
                                    current_page = get_web_page('https://www.ptt.cc' + prev_url)
                                    current_articles, prev_url = get_articles(current_page, today)
                                    threshold = 50

                                for a in articles:
                                    if int(a['push_count']) > threshold:
                                        magnito_bot.send_message(first_chat_id,a['href'])
                            new_offset = first_update_id + 1
			elif first_chat_text == 'food':
                            my_bot.send_message(first_chat_id, 'Input place : ')
                            new_offset = first_update_id + 1
                            updates=my_bot.get_updates(new_offset)
                            if len(updates) > 0:
                                for current_update in updates:
                                    if 'text' not in current_update['message']:
                                        first_chat_text='New member'
                                    else:
                                        first_chat_text = current_update['message']['text']
                                
                            LIST_URL = 'http://www.ipeen.com.tw/search/'+first_chat_text+'/000/1-0-0-0/'
                    
                            list_req = requests.get(LIST_URL)
                            if list_req.status_code == requests.codes.ok:
                                soup = BeautifulSoup(list_req.content, HTML_PARSER)
                                shop_links_a_tags = soup.find_all('a', attrs={'data-label': '店名'})

                                shop_links = []
                                for link in shop_links_a_tags:
                                    shop_link = ROOT_URL + link['href']
                                    my_bot.send_message(first_chat_id,shop_link)
                                    shop_links.append(shop_link)
                                    parse_shop_information(shop_link)
                            new_offset = first_update_id + 1
                        break                                                      
                    except sr.UnknownValueError:
                        magnito_bot.send_message(first_chat_id, 'Sorry,I could not understand audio')
                        break
                    except sr.RequestError as e:
                        magnito_bot.send_message(first_chat_id, 'No response from Google Speech Recognition service: {0}'.format(e))
                        break
			
                elif first_chat_text == 'movie':
                    page = get_web_page('https://tw.movies.yahoo.com/movie_thisweek.html')
                    if page:
                        movies = get_movies(page)
                    for movie in movies:
                        magnito_bot.send_message(first_chat_id,movie['ch_name'])
                        magnito_bot.send_message(first_chat_id,movie['trailer_url'])
                    new_offset = first_update_id + 1
		
                elif first_chat_text == 'PTT':
                    current_page = get_web_page('https://www.ptt.cc/bbs/Gossiping/index.html')
                    if current_page:
                        articles = []
                        today = time.strftime("%m/%d").lstrip('0')
                        current_articles, prev_url = get_articles(current_page, today)
                        while current_articles:
                            articles += current_articles
                            current_page = get_web_page('https://www.ptt.cc' + prev_url)
                            current_articles, prev_url = get_articles(current_page, today)

                            #print('There are today', len(articles), 'Article')
                            threshold = 50
                            #print('popular articles(> %d Push):' % (threshold))
                        for a in articles:
                            if int(a['push_count']) > threshold:
                                magnito_bot.send_message(first_chat_id,a['href'])
                    new_offset = first_update_id + 1
                
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
		
                else :
                    magnito_bot.send_message(first_chat_id, 'Enter another instruction\n╰(*°▽°*)╯'+first_chat_name)
                    new_offset = first_update_id + 1 
					


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
