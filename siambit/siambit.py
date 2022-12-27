import os, requests, sys, re
from core import settings
from . import custom_functions
from bs4 import BeautifulSoup
from alive_progress import alive_bar


def create_credential_file():
  '''
  Create file that store username and password for siambit.
  '''
  try:
    username = input('Username: ')
    password = input('Password: ')
    credential_file_path = settings.BASE_DIR/'core/credential.py'
    with open(credential_file_path, 'x') as f:
        f.write(f'USERNAME="{username}"')
        f.write('\n')
        f.write(f'PASSWORD="{password}"')

  except:
      print("Error @ create_credential_file()")


def check_credential():
  '''
  desc: Check if credential file exist and create if does not.
  '''
  credential_file_path = settings.BASE_DIR/'core/credential.py'
  is_file_exist = os.path.exists(credential_file_path)
  
  if not is_file_exist:
    create_credential_file()
  else:
    from core import credential
    print(credential.USERNAME)


from core import credential

def get_login_session():
  siambit_login_session = requests.Session()
  login_url = settings.SCRAPING_URLS["SIAMBIT_LOGIN_URL"]
  data = {
    'username': credential.USERNAME,
    'password': credential.PASSWORD,
    'returnto': '/'
  }
  headers = {'User-Agent': settings.USER_AGENT}

  r = siambit_login_session.post(login_url, data=data, headers=headers)
  if r.status_code == 200:
      print('Login successful!')
  print(r.status_code, r.reason)

  return siambit_login_session


def get_torrents(siambit_page):
  '''
  Params: siambit_page, ex. 'https://www.siambit.me/viewbrsb.php?sortby=8&cat=911&page=0'
  Return: List of detail url and screen shot url.
          Ex.
            {
              'detail_link': 'details.php?id=1853536&hashinfo=1912662',
              'ss_link': 'https://ibb.co/sQR3Nf0'
            }, ...
  Desc: Receive an siambit torrent list url and return detail url and its ss
  '''

  login_session = get_login_session()
  r = login_session.get(siambit_page, headers={'User-Agent': settings.USER_AGENT})
  doc = BeautifulSoup(r.text, 'html.parser')

  rows = doc.find_all('tr', {"onmouseover" : "this.style.backgroundColor='#E6E6FA';"})

  torrent_details = []
  for row in rows:

    tag = row.find('td', {'width': "900"})

    torrent_detail_link = ''
    screen_shot_link = ''

    torrent_tag = tag.find_all('a')[0]
    if torrent_tag.has_attr('href'):
      torrent_detail_link = torrent_tag.attrs['href']
    
    ss_tag = tag.find_all('a')[1]
    if ss_tag.has_attr('href'):
      screen_shot_link = ss_tag.attrs['href']

    torrent_details.append({
      'detail_url': settings.DOMAIN + '/' + torrent_detail_link,
      'ss_url': screen_shot_link
    })

  login_session.close()

  return torrent_details


def write_result_html(torrents):
  '''
  Desc: Create a basic html that show torrent link with screen shot to output folder.
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
  <body>
  '''
  footer = '''
  </body>
  </html>
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

  result_file_path = settings.BASE_DIR/'results/output.html'
  result_file = open(result_file_path, 'w')
  result_file.writelines(header)
  result_file.writelines(content)
  result_file.writelines(footer)
  result_file.close()


def screen_shot_scrapper():

  #==== User Input =============================================================
  print('Case: 1="All"')
  print('      2="Jav Uncen"')
  print('      3="Pics"')
  print('      4="Jav Cen"')
  print('      5="Clip"')
  print('      6="Special"')

  category = int(input('Please select: '))

  if category == 1:
    scraping_urls = settings.SCRAPING_URLS["SIAMBIT_SCRAPING_URLS_ALL"]
  elif category == 2:
    scraping_urls = settings.SCRAPING_URLS["SIAMBIT_SCRAPING_URLS_JAVUNCEN"]
  elif category == 3:
    scraping_urls = settings.SCRAPING_URLS["SIAMBIT_SCRAPING_URLS_PIC"]
  elif category == 4:
    scraping_urls = settings.SCRAPING_URLS["SIAMBIT_SCRAPING_URLS_JAVCEN"]
  elif category == 5:
    scraping_urls = settings.SCRAPING_URLS["SIAMBIT_SCRAPING_URLS_CLIP"]
  elif category == 6:
    scraping_urls = settings.SCRAPING_URLS["SIAMBIT_SCRAPING_URLS_SPECIAL"]
  #==== End ====================================================================

  torrents = []
  for url in scraping_urls:
    torrents += get_torrents(url)

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

      torrents_with_ss.append({
        'detail_url': torrent['detail_url'],
        'images': images
      })

      bar()

  write_result_html(torrents_with_ss)