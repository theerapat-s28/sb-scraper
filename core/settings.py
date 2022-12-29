from pathlib import Path

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


# SCRAPING_URLS = {
#     "SIAMBIT_LOGIN_URL": "https://www.siambit.me/takelogin.php",
#     # (v) All 18+
#     "SIAMBIT_SCRAPING_URLS_ALL": [
#         f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&page=0', 
#         f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&page=1', 
#         f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&page=2'
#     ],
#     # (v) Japan uncen
#     "SIAMBIT_SCRAPING_URLS_JAVUNCEN": [
#         f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=904&page=0', 
#         f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=904&page=1', 
#         f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=904&page=2'        
#     ],
#     #(v) Pic
#     "SIAMBIT_SCRAPING_URLS_PIC": [
#         f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=911&page=0',
#         f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=911&page=1',
#         f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=911&page=2' 
#     ],
#     #(v) Jav cen
#     "SIAMBIT_SCRAPING_URLS_JAVCEN": [
#        f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=903&page=0',
#        f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=903&page=1',
#        f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=903&page=2'  
#     ],
#     #(v) Clip
#     "SIAMBIT_SCRAPING_URLS_CLIP": [
#        f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=910&page=0',
#        f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=910&page=1',
#        f'{MAIN_SEARCH_SIAMBIT_URL}?sortby=8&cat=910&page=2'  
#     ], 
#     #(v) Custom
#     "SIAMBIT_SCRAPING_URLS_SPECIAL": [
#         'https://www.siambit.me/upfin1.php?id=717041&page=0',
#         'https://www.siambit.me/upfin1.php?id=717041&page=1'
#     ]
# }