import time
import requests
import json
import random


unformated_cookies = json.loads(open('cookies.json', 'r').read())
cookies = {}
for cookie in unformated_cookies:
    cookies[cookie['name']] = cookie['value']


get_followers_header = {
    'Host': 'i.instagram.com',
    'Sec-Ch-Ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'X-Ig-App-Id': '936619743392459',
    'X-Ig-Www-Claim': 'hmac.AR3q6q1uMuydZsiqxdqtrFYWTvdG37z7VXzox7bZKGQampq4',
    'Sec-Ch-Ua-Mobile': '?0',
    'Accept': '*/*',
    'X-Csrftoken': '{{set this value from browser}}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'X-Asbd-Id': '198387',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://www.instagram.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.instagram.com/',
    'Accept-Language': 'en-US,en;q=0.9,ar-IQ;q=0.8,ar;q=0.7',
}




get_id_header = {
    'Host': 'www.instagram.com',
    'Sec-Ch-Ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'Cache-Control': 'max-age=0',
    'Viewport-Width': '1229',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Prefers-Color-Scheme': 'dark',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.instagram.com/',
    'Accept-Language': 'en-US,en;q=0.9,ar-IQ;q=0.8,ar;q=0.7',
}

follow_header = {
    **get_followers_header,
    'Content-Type': 'application/x-www-form-urlencoded',
    'Sec-Ch-Prefers-Color-Scheme': 'dark',
    'X-Instagram-Ajax': '1005835478',
    'X-Requested-With': 'XMLHttpRequest',
}


def follow(id):
    follow_header['Viewport-Width'] = str(random.randint(1000, 1500))
    response = requests.post(f'https://www.instagram.com/web/friendships/{id}/follow/', cookies=cookies, headers=follow_header)
    return json.loads(response.text)


def get_user_id(user_name):
    response = requests.get(f'https://www.instagram.com/{user_name}/', headers=get_id_header, cookies=cookies,)
    return response.text.split('"id":"')[1].split('","')[0]

def get_followers(id, count = 12, max_id = None):
    params = {
        'count': str(count),
        'search_surface': 'follow_list_page',
    }
    if max_id:
        params['max_id'] = max_id
    response = requests.get(f'https://i.instagram.com/api/v1/friendships/{id}/followers/', params=params, cookies=cookies, headers=get_followers_header)
    response_dict = json.loads(response.text)
    users = response_dict['users']
    next_max_id = response_dict['next_max_id']
    return users, next_max_id


# test:

user_id = get_user_id('user.name')
page = 1
index = 1
next_max_id = None
while True:
    followers, next_max_id = get_followers(user_id, max_id = next_max_id)
    for follower in followers:
        follow_response = follow(follower['pk'])
        print(f'[+] (page:{page} / index:{index}) Started following {follower["username"]} whith status of ({follow_response["status"]}).')
        if follow_response["status"] == 'fail':
            print(follow_response["message"])
        index += 1
        time.sleep(2)
    page += 1
