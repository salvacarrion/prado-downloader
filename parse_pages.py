import os
import json
import glob
import pandas
from bs4 import BeautifulSoup
from url_normalize import url_normalize


# Constants
PAGES_PATH = "pages"
files = glob.glob(PAGES_PATH + '/**/*.json', recursive=True)
savepath = "works_urls.txt"


# Parse files
works_urls = set()
for i, file in enumerate(files):
    print(f"Parsing page {i+1}/{len(files)}")
    with open(file, "r") as f:
        try:
            # Load JSON and extract HTML
            r = json.load(f)

            # Check if there is something to parse
            html = r.get('Value')
            if html:
                # Parse HTML
                soup = BeautifulSoup(html, 'html.parser')

                # Get links to works
                tmp_works_urls = soup.select("div.mostrable.miniaturas > figure > figcaption.presentacion-listado > dl > dt > a")
                tmp_works_urls = [url_normalize(elem.attrs['href']) for elem in tmp_works_urls]
                works_urls.update(tmp_works_urls)

        except Exception as e:
            print("[EXCEPTION]: " + str(e))

    # if i==10:  # Debugging
    #     break

# Save URLs
with open(savepath, "w") as f:
    for line in works_urls:
        f.write(line + "\n")

print("")
print(f"{len(works_urls)} URLs were saved!")
print("done!")
