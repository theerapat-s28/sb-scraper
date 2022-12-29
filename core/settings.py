from pathlib import Path


#=== Siambit configs ===========================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#(v) Use to fake using Requests as browser
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '\
             'AppleWebKit/537.36 (KHTML, like Gecko) '\
             'Chrome/39.0.2171.95 Safari/537.36'

DOMAIN = 'https://www.siambit.me'
MAIN_SEARCH_SIAMBIT_URL = 'https://www.siambit.me/viewbrsb.php'
SIAMBIT_LOGIN_URL = 'https://www.siambit.me/takelogin.php'
SEARCH_PICTURE_KEYWORDS = ['.png', '.jpg', '.jpeg', '.gif']
MAX_IMAGE_LIMIT = 2



#=== xidol configs =============================================================
XIDOL_SEARCH_LISTS = [
  'https://xidol.net/?s=imaizumi',
]