import requests
from urllib.parse import quote_plus
def send_file(file:bytearray,file_type:str,file_name):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.8',
        'content-length': len(file),
        'content-type':file_type,
        'origin': 'https://console.liara.ir',
        'priority': 'u=1, i',
        'referer': 'https://console.liara.ir/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36',
    }

    params = {
        'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
        'X-Amz-Credential': '6b96162b-d379-44a7-ae3f-e3cd178bbf19/20240617/us-east-1/s3/aws4_request',
        'X-Amz-Date': '20240617T104438Z',
        'X-Amz-Expires': '86400',
        'X-Amz-SignedHeaders': 'host',
        'X-Amz-Signature': '8c2915c9a5ccff0116806ed481de7e7e4705b6d27b6135b4274ce36ad9a3e077',
    }

    response = requests.put(
        quote_plus(f'https://main-storage-non-taken.storage.c2.liara.space//{file_name}'),
        params=params,
        headers=headers,
        data=file
    )
    print(response)
