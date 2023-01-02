import requests
from core import settings
from bs4 import BeautifulSoup

headers = {'User-Agent': settings.USER_AGENT}

def download_rapidgator(url):
  '''
  Params: url<string>, ex. 'https://rg.to/file/2f0da6f32e0f8baf7f3da5da476779df'
  Desc: 
  '''
  pass


def output_as_text(urls, output_filename) -> None:
  '''
  Desc: Write list of url into text file line by line on output folder.
  '''
  result_file_path = settings.BASE_DIR/f'results/{output_filename}'
  with open(result_file_path, 'w') as f:
    for url in urls:
      s = str(url)
      f.write(s+'\n')


def get_rapidgator_url(page):
  r = requests.get(page, headers=headers)
  soup = BeautifulSoup(r.text, 'html.parser')
  topics = soup.find_all(name='h2', class_='post-title entry-title')
  
  detail_pages = []
  for topic in topics:
    detail_pages.append(topic.a.attrs['href'])

  rapidgators = []
  fail_pages = []
  for detail_page in detail_pages:
    try:
      r = requests.get(detail_page, headers=headers)
      detail_soup = BeautifulSoup(r.text, 'html.parser')
      rapidgator = detail_soup.find(text='Rapidgator').parent
      a_tags = rapidgator.find_all(name='a')
      for tag in a_tags:
        href =tag.attrs['href']
        rapidgators.append(href)
    except:
      print(f'** Error extracting rapidfator url @ {detail_page}')
      fail_pages.append(detail_page)
  
  return rapidgators, fail_pages


def main():
  pages = settings.XIDOL_SEARCH_LISTS

  rapidgator_links = []
  fail_subjects = []
  for page in pages:
    rapidgators, fail_pages = get_rapidgator_url(page)
    rapidgator_links += rapidgators
    fail_subjects += fail_pages

  # Create file output
  output_as_text(rapidgator_links, 'rapidgators.txt')
  output_as_text(fail_pages, 'rapidgator_fail_lists.txt')
