import os
import json
import glob
import pandas as pd
from bs4 import BeautifulSoup
from url_normalize import url_normalize
import unidecode
from tqdm import tqdm

# Constants
DELIMITER = "\n@@@\n"
PAGES_PATH = "works"
files = glob.glob(PAGES_PATH + '/**/*', recursive=True)
savepath = "prado_dataset.csv"

# Selectors
css_work_url = "head > link:nth-child(4)"
css_work_image_url = "meta[name='og:image']"
css_author = "#ficha-obra > div.autor > h2"
css_author_bio = "#ficha-obra > div.autor > p"
css_author_page = "#ficha-obra > div.autor > a"
css_author_id = None  # Derived
css_work_title = "#ficha-obra > div.obra > article > h1"
css_work_subtitle = "#ficha-obra > div.obra > article > strong"
css_work_exposed = None  # Derived
css_work_description = "#ficha-obra > div.obra > article > div"
css_work_tags = "#ficha-obra > div.side-der > div > span > a"
css_technical_sheet_headers = "#ficha > div > div.ficha-tecnica > dl > dt"
css_technical_sheet_fields = "#ficha > div > div.ficha-tecnica > dl > dd"
css_bibliography = "#ficha > div > div.ficha-tecnica > div:nth-child(2) > p"
css_inventory = "#ficha > div > div.ficha-tecnica > div:nth-child(3) > p"
css_expositions = "#ficha > div > div.ficha-tecnica > div:nth-child(4) > p"
css_ubication = "#ficha > div > div.ficha-tecnica > div:nth-child(5) > p"


def read_file(filename, i=None):
    exception = False
    html = None

    # Read file as text (fast; 10it/s)
    try:
        with open(filename, 'r') as f:  # "b" needed. Problems with UnicodeDecodeError
            html = f.read()
    except Exception as e:
        exception = True
        errors.append((i, filename, e))
        print(f"[EXCEPTION TEXT]: idx={i}; file={filename}; error={e}")

    # Try to read file as binary (slower; 2it/s)
    if exception:
        try:
            print("Reading file as binary...")
            with open(file, 'rb') as f:  # "b" needed. Problems with UnicodeDecodeError
                html = f.read()
        except Exception as e:
            errors.append((i, filename, e))
            print(f"[EXCEPTION BINARY]: idx={i}; file={filename}; error={e}")
    return html

# Selection (debugging)
# files = files[3848:4890]

# Parse files
rows = []
columns = []
errors = []
for i, file in tqdm(enumerate(files), total=len(files)):
    # print(f"Parsing page {i+1}/{len(files)}")
    with open(file, "r") as f:
            # To speed-up the reading of the file
            html = read_file(file, i)

            # Check if there is something to parse
            if html:
                # Parse HTML
                soup = BeautifulSoup(html, 'html.parser')
                row = {}

                xml = soup.select(css_work_url)
                row['work_url'] = xml[0].attrs["href"] if xml else None

                xml = soup.select(css_work_image_url)
                row['work_image_url'] = xml[0].attrs["content"] if xml else None

                xml = soup.select(css_author)
                row['author'] = xml[0].getText().strip() if xml else None

                xml = soup.select(css_author_bio)
                row['author_bio'] = "\n\n".join([item.getText().strip() for item in xml]) if xml else None

                xml = soup.select(css_author_page)
                row['author_url'] = xml[0].attrs["href"] if xml else None

                xml = row['author_url'].split("/") if row['author_url'] else None
                row['author_id'] = xml[-1] if xml else None

                xml = soup.select(css_work_title)
                row['work_title'] = xml[0].getText().strip() if xml else None

                xml = soup.select(css_work_subtitle)
                if xml:
                    subtitle = xml[0].getText().strip()
                    s_subtitle = subtitle.split('\n')

                    if len(s_subtitle) == 1:
                        row['work_subtitle'] = subtitle.strip()
                        row['work_exposed'] = None
                    elif len(s_subtitle) == 2:
                        row['work_subtitle'] = s_subtitle[0].strip()
                        row['work_exposed'] = s_subtitle[1].strip()
                    else:
                        raise ValueError("Unknown type")
                else:
                    row['work_subtitle'] = None
                    row['work_exposed'] = None

                xml = soup.select(css_work_description)
                row['work_description'] = xml[0].getText().strip() if xml else None

                xml = soup.select(css_work_tags)
                row['work_tags'] = ";".join([item.getText().strip() for item in xml]) if xml else None

                headers = soup.select(css_technical_sheet_headers)
                fields = soup.select(css_technical_sheet_fields)
                assert len(headers) == len(fields)
                for h, f in zip(headers, fields):
                    header_code = h.getText().replace(" ", "_").lower().strip()
                    header_code = unidecode.unidecode(header_code)
                    row[f'technical_sheet_{header_code}'] = f.getText().strip()

                xml = soup.select(css_bibliography)
                row['bibliography'] = f"{DELIMITER}".join([item.getText().strip() for item in xml]) if xml else None

                xml = soup.select(css_inventory)
                row['inventory'] = f"{DELIMITER}".join([item.getText().strip() for item in xml]) if xml else None

                xml = soup.select(css_expositions)
                row['expositions'] = xml[0].getText().strip() if xml else None

                xml = soup.select(css_ubication)
                row['ubication'] = xml[0].getText().strip() if xml else None

                # Add rows
                rows.append(row)

    # if i+1==200:  # Debugging
    #     break

# Save File
data = pd.DataFrame(rows)
data.to_csv(savepath, index=False)

# Summary
print("")
print(f"{len(data)} rows were saved!")
print("-"*30)
print(f"Errors:")
print(errors)
print("done!")
