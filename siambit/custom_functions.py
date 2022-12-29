from bs4 import BeautifulSoup
import requests, re
from io import BytesIO
from PIL import Image
from core import settings

# def get_attr(tag, search_attr):
#   if tag.has


def getAttr(searchTag, searchAttr, url, filterKeyword=None):
    returnArr = []
    bs = BeautifulSoup(url, 'html.parser')

    for link in bs.find_all(searchTag):
        if link.has_attr(searchAttr):
            if filterKeyword:
                if filterKeyword in link.attrs[searchAttr]:
                    returnArr.append(link.attrs[searchAttr])
            else:
                returnArr.append(link.attrs[searchAttr])

    return returnArr

def addImgTag(url):
    return f'<img src="{url}" style="width: 600px;" referrerpolicy="no-referrer">'

# callback for filter
def isImage(url):
    keywords = settings.SEARCH_PICTURE_KEYWORDS
    for keyword in keywords:
        condition = keyword+'$'
        if re.search(condition, url):
            return True
    return False

def isLargeImage(url):
    try:
        user_agent_value = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '\
                           'AppleWebKit/537.36 (KHTML, like Gecko) '\
                           'Chrome/39.0.2171.95 Safari/537.36'
        headers = {'User-Agent': user_agent_value}
        image_raw = requests.get(url, headers=headers)
        image = Image.open(BytesIO(image_raw.content))
        width, height = image.size
        if not(width < 300 or height < 250):
            return True
        else:
            return False
    except:
        return True

def isUrl(url):
    # (v) "^http" is regex syntax
    if re.search("^http", url):
        return True
    else:
        return False

def isNotFaviconOrLogo(url):
    keywords = ['favicon', 'Favicon', 'logo', 'Logo']
    for keyword in keywords:
        if keyword in url:
            return False
    return True

def isRedirect(url):
    return not isImage(url)

def arrMap(callback, arr):
    result = []
    for element in arr:
        result.append(callback(element))
    return result

def arrFilter(callback, arr):
    result = []
    for element in arr:
        if callback(element):
            result.append(element)
    return result

def scrapingImages(url):
    '''
    Params: url, String of image hosting url
    Return: [], List of image url
    Desc: Extract list of image from image hosting site.
          Ex.
          url = https://imgur.com/udCQEGH
          Return ['https://i.imgur.com/udCQEGHh.jpg']
    '''

    no_image_url = 'https://crpf.gov.in/writereaddata/Portal/DGIGMaster_Photos/1_126_1_istockphoto-1357365823-612x612.jpg'
    result = [no_image_url]

    if not isUrl(url):
        return result

    user_agent_value = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '\
                       'AppleWebKit/537.36 (KHTML, like Gecko) '\
                       'Chrome/39.0.2171.95 Safari/537.36'
    headers = {
      'User-Agent': user_agent_value,
      'Content-Type': 'text/html'
    }
    r = requests.get(url, headers=headers)
    result = re.findall("\"(.*?)\"", r.text)
    result = arrFilter(isUrl, result)
    result = arrFilter(isImage, result)
    result = arrFilter(isNotFaviconOrLogo, result)
    result = arrFilter(isLargeImage, result)
    # -- Remove duplicated
    result = list(set(result))
    # --
    return result
