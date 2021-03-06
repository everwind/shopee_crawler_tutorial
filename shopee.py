import requests
import json
import pandas
from selenium import webdriver
from time import sleep

def get_id(pages, new=0):
    '''
    抓取商品id，並傳回字典型態
    '''
    content = {                #設定get參數
        'by': 'pop',
        'order': 'desc',
        'categoryids': 69,
        'newest': new,
        'limit': pages,
        'skip_price_adjust': False,
    }
    # https://shopee.tw/api/v1/search_items/?by=pop&order=desc&categoryids=69&newest=0&limit=50&skip_price_adjust=false
    get_item = requests.get(
        'https://shopee.tw/api/v1/search_items/', params=content)
    payload = str({"item_shop_ids": get_item.json()['items']})
    payload = payload.replace("'", '"')  #json要求用""不能用''    
    return json.loads(payload)

def get_page(url, pages):
    '''
    用selenium抓cookie、csrf token
    用post傳json去
    得到物品資料
    '''
    driver = webdriver.Chrome('D:\code\ceiba\driver\chromedriver.exe')  #initiate chrome
    driver.get(url)
    sleep(1)    #給他一點時間載入 不然好像會壞掉QQ
    cookie = ';'.join(['{}={}'.format(item['name'], item['value'])  #抓cookie
                for item in driver.get_cookies()])
    token = driver.get_cookie('csrftoken')['value']          
    driver.quit()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'x-csrftoken': token,
        'Referer': url,
        'Cookie': cookie,
    }

    result = []
    if pages <= 100:            #經過測試發現一次最多傳回100筆資料，所以如果要求超過100筆，要另外處理
        payload = get_id(pages)
        res = requests.post('https://shopee.tw/api/v1/items/',   #post
                            json=payload, headers=headers)
        result.append(res.json())
    else:
        x = 0
        while x < pages:
            payload = get_id(100, x)
            res = requests.post('https://shopee.tw/api/v1/items/',
                                json=payload, headers=headers)
            result.append(res.json())
            x += 100
    return result



if __name__ == '__main__':
    url = 'https://shopee.tw/3C%E7%9B%B8%E9%97%9C-cat.69'
    for i in get_page(url, 20):
        for r in i:
            print('******************************************************')
            print(r['name'], r['price'])
