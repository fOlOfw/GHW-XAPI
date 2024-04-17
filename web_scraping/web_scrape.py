import requests
import re #regex

# https://www.goodreads.com/list/show/8231.Best_Books_About_Mathematics

book_titles = []

cookies = {
    'ccsid': '784-5723893-5304937',
    'locale': 'en',
    'blocking_sign_in_interstitial': 'true',
    'csm-sid': '383-3833589-7576837',
    '_session_id2': 'a46d58853fa45a605c536c80c798f677',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.goodreads.com/list/show/8231.Best_Books_About_Mathematics',
    # 'Cookie': 'ccsid=784-5723893-5304937; locale=en; blocking_sign_in_interstitial=true; csm-sid=383-3833589-7576837; _session_id2=a46d58853fa45a605c536c80c798f677',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'If-None-Match': 'W/"d0429aa9fcad25959398d23816ac0233"',
}

for i in range(1, 10):
    params = {
        'page': i,
    }
    print("Scraping page", params)

    response = requests.get('https://www.goodreads.com/list/show/8231.Best_Books_About_Mathematics?page={i}', params = params, headers = headers)
    #response = requests.get('https://www.goodreads.com/list/show/8231.Best_Books_About_Mathematics',headers=headers)
    pattern = r' <a title="([^"]*)'
    matches = re.findall(pattern, response.text)
    #print(matches) 

    #THIS BELOW COMMENTED PART WAS THE FIRST TRY - Tested with "next_page disabled" but didn't work
    # # if "next_page disabled" in response.text:
    # if "current" != "href=" " " in response.text:
    #     print("end of the book title pages", params)
    #     break
    # else:
    #     for match in matches:
    #         book_titles.append(match.strip())

    current_tag = re.search(r'<em class="current">([^<]*)</em>', response.text)
    if current_tag:
        current_content = current_tag.group(1).strip()  # Get the content inside the <em> tag and remove leading/trailing whitespace
        for match in matches:
            if current_content:
            # If there is content inside the <em> tag
                book_titles.append(match.strip())
            else:
            # If the <em> tag is empty
                print("End of the book title pages", params)
                break
    else:
        print("No 'current' class found!")
        break  
        
with open('book_titles_collection.txt','w') as f: #creates a text file and stores the data
    for book_title in book_titles:
       f.write(book_title.strip() + '\n')
         

# with open('book_titles.txt','w') as f: #creates a text file and stores the data
#    for match in matches:
#        f.write(match.strip() + '\n')
            # book_titles.append(match.strip())
            # print(match.strip())

