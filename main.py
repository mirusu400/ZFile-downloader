import requests
import json
import os
import os.path
import collections
import urllib.parse
from typing import Union
q = collections.deque()

try:
    with open("data.json", "r") as f:
        data = json.load(f)
except:
    data = {}

def crawl(url, upstream_object: Union[list, dict]):
    r = requests.get(url)
    _data = r.json()
    files = _data["data"]["files"]
    for file in files:
        print(file)
        # Check upstream_object have files key
        if "files" not in upstream_object:
            upstream_object["files"] = []
        upstream_object["files"].append(file)
        if file["type"] == "FOLDER":
            q.append(file)
        else:
            print("this is file")

    return r.content

def download_recursive(item: Union[list, dict]):
    if "files" in item:
        for file in item["files"]:
            if file["type"] == "FOLDER":
                download_recursive(file)
            else:
                path_str = file["path"]
                name_str = file["name"]
                url_str = file["url"]
                print(f"Downloading {path_str}/{name_str}")
                if os.path.exists(f"./downloads/{path_str}/{name_str}"):
                    print("File already exists")
                    continue
                r = requests.get(url_str, stream=True)
                print(r.status_code)
                if r.status_code == 200:
                    os.makedirs(f"./downloads/{path_str}", exist_ok=True)
                    with open(f"./downloads/{path_str}/{name_str}", "wb") as f:
                        for chunk in r:
                            f.write(chunk)
            

def main(link):
    crawl(f"{link}/api/list/1?path=%2F&password=&orderBy=&orderDirection=", data)
    while q:
        file = q.popleft()
        crawl(f"{link}/api/list/1?path={urllib.parse.quote(file['path'])}%2F{urllib.parse.quote(file['name'])}&password=&orderBy=&orderDirection=", file)
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    link = input("Enter link: ")

    download_recursive(data)
    # main()