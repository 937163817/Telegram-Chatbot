
import requests
import datetime



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


token = '606184614:AAEaapXpdRswzj3L--saKbCWr7K2kzyIcn0' #改成我們的token
magnito_bot = BotHandler(token) #Your bot's name



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
                    r=sr.Recognizer() 
					new_offset = first_update_id + 1
                    with sr.Microphone() as source:
                        magnito_bot.send_message(first_chat_id, 'Please wait. Calibrating microphone...')
                        #print("Please wait. Calibrating microphone...") 
                        r.adjust_for_ambient_noise(source, duration=5)
                        magnito_bot.send_message(first_chat_id, 'Say something!')
                        #print("Say something!")
                        audio=r.listen(source)

                    try:
                        magnito_bot.send_message(first_chat_id, 'I thinks you said:')
                        magnito_bot.send_message(first_chat_id, r.recognize_google(audio, language="zh-TW"))
                        #first_chat_text = r.recognize_google(audio, language="zh-TW")
                        #new_offset = first_update_id + 1                                    
                        break                                 
                    except sr.UnknownValueError:
                        magnito_bot.send_message(first_chat_id, 'Sorry,I could not understand audio')
                        break
                    except sr.RequestError as e:
                        magnito_bot.send_message(first_chat_id, 'No response from Google Speech Recognition service: {0}'.format(e))
                        break	
                else :
                    magnito_bot.send_message(first_chat_id, 'Enter another instruction\n╰(*°▽°*)╯'+first_chat_name)
                    new_offset = first_update_id + 1 
					


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
