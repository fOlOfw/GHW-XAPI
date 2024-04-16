import requests
import re #regex

# https://www.goodreads.com/list/show/8231.Best_Books_About_Mathematics

book_titles = []

cookies = {
    'ccsid': '784-5723893-5304937',
    'locale': 'en',
    '_session_id2': 'ca09aa7361979d45e1427ef5e5cb2761',
    'blocking_sign_in_interstitial': 'true',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.goodreads.com/genres/science',
    # 'Cookie': 'ccsid=784-5723893-5304937; locale=en; _session_id2=ca09aa7361979d45e1427ef5e5cb2761; blocking_sign_in_interstitial=true',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}

response = requests.get(
    'https://www.goodreads.com/list/show/8231.Best_Books_About_Mathematics',
    headers=headers
)
pattern = r' <a title="([^"]*)'
matches = re.findall(pattern, response.text)
#print(matches) 

with open('book_titles.txt','w') as f: #creates a text file and stores the data
    for match in matches:
        f.write(match.strip() + '\n')
        #book_titles.append(match.strip())
        #print(match.strip())

