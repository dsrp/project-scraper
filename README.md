# project-scraper
Code for scraping communities and other interesting projects from public websites.

## Datasets
Readily crawled datasets live in the [data](data/) folder. Currently available are:
* Global Ecovillage Network (GEN) [gen.json](data/gen.json)
* Fellowship for Intentional Communities (FIC) [fic.json](data/fic.json)

## Installing
1. Make sure you have [GIT](https://git-scm.com/downloads) and [GIT-LFS](https://git-lfs.github.com/) installed.
2. Clone this repo: `git clone https://github.com/dsrp/project-scraper.git`.
3. Make sure you have [pipenv](https://pipenv.readthedocs.io/en/latest/) available; `pip install pipenv`
4. Clone repo: `git clone https://github.com/dsrp/project-scraper.git` and change into project directory.
5. Locally install dependencies: `pipenv install`

## Running
1. `pipenv shell`
2. `scrapy crawl <fic|gen>`
