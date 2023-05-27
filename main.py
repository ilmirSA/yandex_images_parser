import aiofiles
import aiohttp
import asyncio
import json
import os
import random
from aiohttp_socks import ProxyConnector
from bs4 import BeautifulSoup


async def read_json_file(filename):
    async with aiofiles.open(filename, 'r') as file:
        async for line in file:
            data = json.loads(line)
            yield {'img': data['img'], 'url': data['url']}


async def text_and_url_extraction(img_name, img_url, proxy):
    connector = ProxyConnector.from_url(proxy)
    async with aiohttp.ClientSession(connector=connector) as session:
        url = f'https://yandex.ru/images/search?rpt=imageview&url={img_url}'

        await asyncio.sleep(1)

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
        'socks5://QvxNH2:spDUfH@185.183.160.:8000',
        'socks5://JNFnSz:SJmgCX@213.226.79.159:8000',
        'socks5://JNFnSz:SJmgCX@213.226.79.152:8000',
        'socks5://JNFnSz:SJmgCX@213.226.78.221:8000',
        'socks5://1szZnA:ZQ4QHm@95.181.172.148:8000'
    ]

    processed_files = set()
    if os.path.exists('processed_images.txt'):
        async with aiofiles.open('processed_images.txt', 'r') as f:
            processed_files = {line.strip() for line in await f.readlines()}

    results = []
    if os.path.exists('result.json'):
        async with aiofiles.open('result.json', 'r') as f:
            results = json.loads(await f.read())

    async for data in read_json_file('dataset_dict.json'):
        name, link = data['img'], data['url']
        if name in processed_files:
            print(f'Skipping {name}, already processed.')
            continue

        random_proxy = random.choice(proxies)
        print(random_proxy)
        try:
            result = await text_and_url_extraction(name, link, random_proxy)
            if result is not None:
                results.append(result)
                async with aiofiles.open('result.json', 'w') as f:
                    await f.write(json.dumps(results))
                async with aiofiles.open('processed_images.txt', 'a') as f:
                    await f.write(name + '\n')
        except aiohttp.ClientResponseError as exc:
            if exc.status == 400:
                print(exc)
                print(f'{name} got a 400 Bad Request error, waiting for 5 minutes...')
                await asyncio.sleep(1)  # 5 minutes
        except Exception as exc:
            print(f'{name} generated an exception: {exc}')


if __name__ == '__main__':
    asyncio.run(main())
