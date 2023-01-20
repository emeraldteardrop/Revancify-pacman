"""
Fetch latest version from the github of the corresponding source repository.
"""

from requests import get
import math
from json import load

with open('sources.json', 'r') as sourcesfile:
    sourcesjson = load(sourcesfile)

for source in sourcesjson:
    if source['sourceStatus'] == "on":
        sourcemaintainer = source['sourceMaintainer']

with open(f'.{sourcemaintainer}latest', 'w') as mainfile:
    try:
        data = []
        for component in ["cli", "patches", "integrations"]:
            json = get(f"https://api.github.com/repos/{sourcemaintainer}/revanced-{component}/releases/latest", headers={'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" }).json()
            data.append(json['tag_name'].replace("v", ""))
            for asset in json['assets']:
                data.append(asset['browser_download_url'])
                data.append(str(int(asset['size'])))
        mainfile.write("\n".join(data))
    except:
        mainfile.write("error")
