import requests
from TOKEN import TOKEN
from tqdm import tqdm
import time
import datetime
from pprint import pprint
import json


def get_vk(id):
    url = "https://api.vk.com/method/photos.get"
    param = {
                'user_ids': id,
                'access_token': TOKEN,
                'v': '5.131'
            }

    response = requests.get('https://api.vk.com/method/users.get', params=param)
    resi = response.json()
    id = resi['response'][0]['id']

    params = {
        "owner_id": id,
        "album_id": "profile",
        "rev": "0",
        "extended": "1",
        "count": int(input("Введите колличество фотографий для скачивания: ")),
        "access_token": TOKEN,
        "v": "5.131"
    }

    response = requests.get(f'{url}', params = params)
    res = response.json()

    global file_dict
    likes = res['response']['items']
    photo_list = []
    file_dict = {}
    print('-' * 75)
    global img

    for photo in tqdm(likes, desc='Скачиваем фотки.....'):
        time.sleep(0.5)
        timestamp = photo['date']
        like = photo['likes']['count']
        time_value = datetime.datetime.fromtimestamp(timestamp)
        time_post = time_value.strftime('%d-%m-%Y_%H.%M.%S')

        for img in photo['sizes']:
            if img['type'] == 'w':
                jmg_url = img['url']
            elif img['type'] == 'z':
                jmg_url = img['url']
            else:
                jmg_url = photo['sizes'][-1]['url']
            sizes_type = img['type']

        pics_dict = {'likes': like,
            'date': time_post,
            'url': jmg_url,
            'type_size': sizes_type
            }
        photo_list.append(pics_dict)

    for element in photo_list:
        key = element['likes']
        if key not in file_dict.keys():
            file_dict[key] = (f"{element['likes']}.jpg", element['url'])
        else:
            key = f"{element['likes']}_{element['date']}.jpg"
            file_dict[key] = (f"{element['likes']}-{element['date']}.jpg", element['url'])
    print('-' * 75)
    return file_dict
    

def photos_upload(TOKEN_YA):
    photos_info = []
    time.sleep(1)
    headers = {'Content-Type': 'application/json',
            'Authorization': f'OAuth {TOKEN_YA}'
            }
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'
    name_papka = input('Напишите название папки которая будет создана на Я.Диске: ')
    print("Создаём папку Я.Диск.....")
    time.sleep(1)
    response1 = requests.put(f'{url}?path={name_papka}', headers=headers)
    if response1.status_code == 201:
        time.sleep(1)
        print(f'Папка {name_papka} создана.')
    else:
        print(response1.status_code)
        print('Папку создать не удалось.....((')


    print('-' * 75)
    time.sleep(1)
    method = 'upload'
    for lk in tqdm(file_dict, desc="Загружаем фото на Я.Диск....."):
        for name_file, url_link in file_dict.items():
            name_file = file_dict[lk][0]
            url_link = file_dict[lk][1]
        params = {'path': f"{name_papka}/{name_file}", 'url': url_link}
        response = requests.post(f'{url}{method}/', params=params, headers=headers)
        if response.status_code == 202:
            photo_info = {
                'name': name_file,
                'size': img['type']
                }
            photos_info.append(photo_info)

    with open('photos_info.json', 'w') as f:
        json.dump(photos_info, f, indent=2)

    if response.status_code == 202:
        print("Фото успешно загружены.")
        print('-' * 75)
    else:
        print(response.status_code)
        pprint(f'{response.json()}')
        print('Фото не загрузились.....((')

if __name__ == '__main__':
    get_vk(input("Введите id пользователя VK: "))
    photos_upload(input("Введите токен Я.Диска: "))