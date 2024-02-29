import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import datetime
import sys

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--url", dest="url", type=str,
                        help="Enter the target site link. Example: \"https://site.link\"")
arg_parser.add_argument("--limit", dest="limit", type=int,
                        help="Set the limit of search amount of links. Default is 100")
args = arg_parser.parse_args()

if args.url:
    site_url = args.url
else:
    print("Entering the target site link is mandatory")
    print("The program exited\n")
    arg_parser.print_help()
    sys.exit()

if args.limit:
    limit = args.limit
else:
    limit = 100

site_links = []


def get_all_links(target_url=None):
    global site_url
    global site_links
    if target_url is None:
        url = site_url
    else:
        url = target_url
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.findAll("a")
        if len(links) == 0:
            print("Your site may be based on react")
            print("There is no ability to process the site")
            print("The program exited")
            sys.exit()
        for link in links:
            href = link.get("href")
            if href and not href.startswith("#") and href != site_url and href not in site_links:
                if len(site_links) >= limit:
                    return True
                else:
                    if url in href:
                        site_links.append(href)
                        print(f"Crawling {(len(site_links) * 100) // limit}%", end='\r', flush=True)
                    else:
                        site_links.append(urljoin(url, href))
                        print(f"Crawling {(len(site_links) * 100) // limit}%", end='\r', flush=True)

    else:
        print(response.status_code)
        print(f"Error: Unable to retrieve content from the '{site_url}'.")
        return False


print("You can stop the process at any time with Ctrl+C")
print("Crawling Start", flush=True)
print("Crawling", end='\r', flush=True)

try:
    _ = get_all_links()

    for site_link in site_links:
        is_full = get_all_links(target_url=site_link)
        if is_full:
            break
except KeyboardInterrupt:
    print("Processing was stopped by user intervention")



print(f"Crawling End!", flush=True)
print(f"Find {len(site_links)} link")

filename = f"{site_url}_{str(datetime.datetime.now())}"

for i in "#%&{}\\<>*?$!'\":@+`|=-. ":
    filename = filename.replace(i, "")
filename = filename.replace("https", "").replace("http", "").replace("/", "")

with open(f"LinkCrawler_{filename}_{limit}.crawler", "w", encoding="utf-8") as f:
    for s in site_links:
        f.write(f"{s}\n")

print(f"Values were saved in \"LinkCrawler_{filename}.crawler\" file")
