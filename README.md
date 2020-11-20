# Prado Museum's Project

Scrape data and images from the PRADO MUSEUM website to build a dataset for a Generative Adversarial Network.

**Website:** [https://www.museodelprado.es/coleccion/obras-de-arte](https://www.museodelprado.es/coleccion/obras-de-arte)

Steps:

1. Get list of work URLs

Download in ascending and descending order to overcome the 10,000 limit of the pagination (...normalize/canonicalize URLs and remove duplicates)

```bash
sh get_pages.sh
```

2. Extract work URLs

```bash
python parse_pages.py
```

3. Download HTML of the URLs

```bash
sh get_works.sh
```

4. Parse downloaded HTMLs

```bash
python parse_works.py
```
