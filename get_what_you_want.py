import argparse
import os
import time

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import MaxRetryError, NewConnectionError

if __name__ == '__main__':

    args = argparse.ArgumentParser()
    args.add_argument('--key_word', type=str, default='图片')
    args.add_argument('--save_path', type=str, default='imgs', help='存放路径')
    args = args.parse_args()


    url = f"https://cn.bing.com/images/search?q={args.key_word}&form=HDRSC2&first=1&tsc=ImageHoverTitle"

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    session = requests.session()

    resp = session.get(url, headers=headers)

    page = BeautifulSoup(resp.text, 'html.parser')
    as_ = page.find_all('a', attrs={'class': 'iusc'})

    if not os.path.exists(args.save_path):
        os.mkdir(args.save_path)


    i = len(os.listdir(args.save_path))
    for a_ in as_:
        all_attrs = a_.get('m')[1: -1].replace('"', '')
        all_attrs = all_attrs.split(',')
        murl = all_attrs[4][5:]
        try:
            resp = requests.get(murl, headers=headers)
            img_name = 'img_' + str(i) + '.jpg'
            file = open(os.path.join(args.save_path, img_name), 'wb')
            file.write(resp.content)
            file.close()
            i += 1
            print('下载+1')
        except (Exception, MaxRetryError, NewConnectionError, ConnectionError) as e:
            print('有些图片无法下载')
        time.sleep(0.5)
    print('下载完成!')

    session.close()
