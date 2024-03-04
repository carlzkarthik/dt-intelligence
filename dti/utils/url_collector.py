import datetime
import re
import requests
from .utils import *
from .print_utils import *
from ..models import OnionLinks

search_engines = {'ahmia': "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q=",
                  'Torch': "http://torch.onion"}


def onion_url_collector(keyword, choice):
    print_info("Running onion_link_collector")
    if 'all' in choice:
        print("Running All Search Engines")
    elif 'ahmia' in choice:
        ahmia(keyword)


def ahmia(keyword):
    print_info("Running Ahmia")
    url = f"http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={keyword}"
    try:
        web_content = get_web_content(url)
    except:
        print_error(f"Failed to run Ahmia search engine for keyword {keyword}")
        return

    links = get_onion_links(web_content)

    for link in links:
        ol = OnionLinks(url=link,
                        source_name="Ahmia",
                        source_url=url,
                        visited=False,
                        keyword_searched=keyword
                        )
        ol.save()
        print_info(f"Saved --- {link}")

    print_info("All the links saved to database successfully")
