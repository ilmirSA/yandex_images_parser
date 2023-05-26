import asyncio
import json
import os
import random

import aiofiles
import aiohttp
from aiohttp_socks import ProxyConnector
from bs4 import BeautifulSoup


async def read_json_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            data = json.loads(line)
            yield {'img': data['img'], 'url': data['url']}


async def text_and_url_extraction(img_name, img_url, proxies):
    proxy = random.choice(proxies)
    connector = ProxyConnector.from_url(proxy)
    async with aiohttp.ClientSession(connector=connector) as session:
        url = f'https://yandex.ru/images/search?rpt=imageview&url={img_url}'

        async with session.get(url) as response:
            response.raise_for_status()
            soup = BeautifulSoup(await response.text(), 'lxml')

            main_url_image = soup.find('img', class_='CbirPreview-Image').get('src')

            links_text = [{link.get('href'): link.text} for link in soup.find_all('a', class_='Link Link_view_default')]

            result = {
                'image_name': img_name,
                'image_link': main_url_image,
                'image_text': links_text,
            }

            return result


async def main():
    proxies = [
        'socks5://QvxNH2:spDUfH@185.183.160.62:8000',
        'socks5://JNFnSz:SJmgCX@213.226.79.159:8000',
        'socks5://JNFnSz:SJmgCX@213.226.79.152:8000',
        'socks5://JNFnSz:SJmgCX@213.22678.221:8000',
        'socks5://1szZnA:ZQ4QHm@95.181.172.148:8000'
    ]

    if not os.path.exists('processed_images.txt'):
        open('processed_images.txt', 'w').close()

    with open('processed_images.txt', 'r') as f:
        processed_files = [line.strip() for line in f.readlines()]

    if not os.path.exists('result.json'):
        set = []
        with open('result.json', 'w') as f:
            json.dump(set, f)

    async for data in read_json_file('dataset_dict.json'):
        name, link = data['img'], data['url']
        if name in processed_files:
            print(f'Skipping {name}, already processed.')
            continue

        for proxy in proxies:

            try:
                result = await text_and_url_extraction(name, link, [proxy])
                if result is not None:
                    async with aiofiles.open('result.json', 'r') as f:
                        data = json.loads(await f.read())
                        data.append(result)
                    async with aiofiles.open('result.json', 'w') as f:
                        await f.write(json.dumps(data))
                    with open('processed_images.txt', 'a') as f:
                        f.write(name + '\n')
                    break
            except aiohttp.ClientResponseError as exc:
                if exc.status == 400:
                    print(f'{name} got a 400 Bad Request error, waiting for 5 minutes...')
                    await asyncio.sleep(300)  # 5 minutes
            except Exception as exc:
                print(f'{name} generated an exception: {exc}')
        else:
            print(f'{name} failed to download with all proxies')


if __name__ == '__main__':
    asyncio.run(main())
