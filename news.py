import requests
from bs4 import BeautifulSoup


def main():
    print('FreeNews:')
    dom = requests.get('http://news.ltn.com.tw/list/newspaper').text
    soup = BeautifulSoup(dom, 'html5lib')
    for ele in soup.find('ul', 'list').find_all('li'):
        print(ele.find('a', 'tit').text.strip())

if __name__ == '__main__':
    main()