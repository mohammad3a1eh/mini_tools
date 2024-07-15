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
arg_parser.add_argument("--format", dest="format_f", type=str,
                        help="Set format file")
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

if args.format_f:
    format_f = args.format_f
else:
    print("Entering the format is mandatory")
    print("The program exited\n")
    arg_parser.print_help()
    sys.exit()


tags = [
    ["a", "href"],
    ["link", "src"],
    ["script", "src"],
    ["img", "src"],
    ["video", "poster"],
    ["source", "src"]
]
site_links = []
site_files = []


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

        for tag in tags:
            for a in soup.findAll(tag[0]):
                href = a.get(tag[1])
                if href and not href.startswith("#") and href != site_url and href not in site_links:
                    if len(site_files) >= limit:
                        return True
                    else:
                        if format_f in href:
                            if url in href:
                                site_files.append(href)
                                print(f"Crawling {(len(site_files) * 100) // limit}%", end='\r', flush=True)
                            else:
                                site_files.append(urljoin(url, href))
                                print(f"Crawling {(len(site_files) * 100) // limit}%", end='\r', flush=True)
                        else:
                            if url in href:
                                site_links.append(href)
                                print(f"Crawling {(len(site_files) * 100) // limit}%", end='\r', flush=True)
                            else:
                                site_links.append(urljoin(url, href))
                                print(f"Crawling {(len(site_files) * 100) // limit}%", end='\r', flush=True)



    else:
        print(response.status_code)
        print(f"Error: Unable to retrieve content from the '{url}'.")
        return False


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
print(f"Find {len(site_files)} file")

filename = f"{site_url}_{str(datetime.datetime.now())}"

for i in "#%&{}\\<>*?$!'\":@+`|=-. ":
    filename = filename.replace(i, "")
filename = filename.replace("https", "").replace("http", "").replace("/", "")

with open(f"FileCrawler_{filename}_{limit}.crawler", "w", encoding="utf-8") as f:
    for s in site_files:
        f.write(f"{s}\n")

print(f"Values were saved in \"FileCrawler_{filename}.crawler\" file")