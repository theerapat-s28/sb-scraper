import os, requests, sys, re
from core import settings, credential
from . import custom_functions
from bs4 import BeautifulSoup
from alive_progress import alive_bar

def get_login_session():
  siambit_login_session = requests.Session()
  login_url = settings.SIAMBIT_LOGIN_URL
  data = {
    'username': credential.SIAMBIT_USERNAME,
    'password': credential.SIAMBIT_PASSWORD,
    'returnto': '/'
  }
  headers = {'User-Agent': settings.USER_AGENT}

  r = siambit_login_session.post(login_url, data=data, headers=headers)
  if r.status_code == 200:
      print('Login successful!')
  print(r.status_code, r.reason)

  return siambit_login_session


def get_torrents(siambit_page:str, min_seeding:int=0):
  '''
  Params: siambit_page, ex. 'https://www.siambit.me/viewbrsb.php?sortby=8&cat=911&page=0'
          min_seeding(default=0), ex. 50
  Return: List of detail url and screen shot url.
          Ex.
            {
              'detail_link': 'details.php?id=1853536&hashinfo=1912662',
              'ss_link': 'https://ibb.co/sQR3Nf0'
            }, ...
  Desc: Receive an siambit torrent list url that seeding number is greater or equal
        and return detail url and its ss
  '''

  login_session = get_login_session()
  r = login_session.get(siambit_page, headers={'User-Agent': settings.USER_AGENT})
  doc = BeautifulSoup(r.text, 'html.parser')

  rows = doc.find_all('tr', {"onmouseover" : "this.style.backgroundColor='#E6E6FA';"})

  torrent_details = []
  for row in rows:

    seeding_row = row.find_all('td')[-3]
    seeding = seeding_row.find('span', {'class': 'green'})
    if seeding == None:
      seeding = seeding_row.find('font', {'color': '#ff0000'})
      if seeding == None:
        seeding = seeding_row.find('font', {'color': '#000000'})

    if seeding == None:
      # if any above still cannot be found.
      seeding = 0
    else:
      seeding = int(seeding.text)

    tag = row.find('td', {'width': "900"})

    torrent_detail_link = ''
    screen_shot_link = ''

    torrent_tag = tag.find_all('a')[0]
    if torrent_tag.has_attr('href'):
      torrent_detail_link = torrent_tag.attrs['href']
    
    if len(tag.find_all('a')) > 1: # In case no screen shot
      ss_tag = tag.find_all('a')[1]
      if ss_tag.has_attr('href'):
        screen_shot_link = ss_tag.attrs['href']

    if seeding > min_seeding:
      torrent_details.append({
        'detail_url': settings.DOMAIN + '/' + torrent_detail_link,
        'ss_url': screen_shot_link
      })

  login_session.close()

  return torrent_details


def get_html_body_of_torrents(torrents):
  '''
  Desc: Create html body content of torrents for basic html file.
  '''

  content = ''
  for torrent in torrents:
    content += '<div>'
    for image in torrent['images']:
      img = f'<img src="{image}" style="width: 450px;" referrerpolicy="no-referrer">'
      content += img
    torrent_url = torrent['detail_url']
    a = f'<a href="{torrent_url}" target="_blank">{torrent_url}</a>'
    content += a
    content += '</div>'
  return content


def create_basic_html(content, filename):
  '''
  Desc: Create a basic html that output folder.
  '''

  header = '''
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
  </head>
  
  '''
  body = f'''
  <body>
  {content}
  </body>
  '''
  footer = '''
  </html>
  '''

  result_file_path = settings.BASE_DIR/f'results/{filename}'
  result_file = open(result_file_path, 'w')
  result_file.writelines(header)
  result_file.writelines(body)
  result_file.writelines(footer)
  result_file.close()

def user_input():
  return

def screen_shot_scrapper():

  #==== User Input =============================================================
  print('Case: 1 = All')
  print('      2 = Jav Uncen')
  print('      3 = Pics')
  print('      4 = Jav Cen')
  print('      5 = Clip')
  print('      6 = Custom specific')

  category = int(input('Please select: '))

  cat = ''
  cat_string = ''

  if category == 1:
    cat = ''
    cat_string = 'All'
  elif category == 2:
    cat = 'cat=904'
    cat_string = 'Jav Uncen'
  elif category == 3:
    cat = 'cat=911'
    cat_string = 'Pics'
  elif category == 4:
    cat = 'cat=903'
    cat_string = 'Jav Cen'
  elif category == 5:
    cat = 'cat=910'
    cat_string = 'Clip'
  elif category == 6:
    cat_custom_number = input('Please specifice cat number i.e. 912 : ')
    cat = f'cat={cat_custom_number}'
    cat_string = 'Custom'

  print('Sort by: 1 = Date, 2 = Seeding')
  sort = int(input('Sorting: '))

  sort_query =''
  sort_string = ''
  if sort == 1:
    sort_query = 'sortby=15'
    sort_string = 'Date'
  elif sort == 2:
    sort_query = 'sortby=8'
    sort_string = 'Seeding'

  page_num = int(input('Number of page to collect: '))

  seed_num_filter = int(input('Minimum seeding number: '))

  # Print conclusion
  print(f'--- Category = {cat_string}, Sort by = {sort_string}, Total page = {page_num}, Minimum Seeding = {seed_num_filter} ---')
  print(f'Pages to be extracted are :')

  scraping_urls = []
  for i in range(page_num):
    url = f'{settings.MAIN_SEARCH_SIAMBIT_URL}?{sort_query}&{cat}&page={i}'
    scraping_urls.append(url)
    print(f'  {url}')
    


  #==== End ====================================================================

  torrents = []
  for url in scraping_urls:
    torrents += get_torrents(url, seed_num_filter)

  torrents_with_ss = []
  with alive_bar(len(torrents), dual_line=True, title='Extract images') as bar:
    for torrent in torrents:
      if torrent['ss_url']:
        images = []

        #(v) If it is already an image just collect and go forward.
        if custom_functions.isImage(torrent['ss_url']):
          images.append(torrent['ss_url'])
        else:
          images = custom_functions.scrapingImages(torrent['ss_url'])
          #(v) Limit number showing images
          images = images[:settings.MAX_IMAGE_LIMIT]

      torrents_with_ss.append({
        'detail_url': torrent['detail_url'],
        'images': images
      })

      bar()

  html_body = get_html_body_of_torrents(torrents_with_ss)

  create_basic_html(html_body, 'output.html')
