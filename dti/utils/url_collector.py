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
    """
    Get onion links from AHMIA Search Engine and store them in the database
    :param keyword: search keyword
    """
    print_info("Running Ahmia")
    url = f"http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={keyword}"
    web_content = get_web_content(url)

    if web_content == -1:
        print_error(f"Failed to search {keyword} on Ahmia")
        return -1

    links = get_onion_links(web_content)

    for link in links:
        ol = OnionLinks(url=link,
                        source_name="Ahmia",
                        source_url=url,
                        visited=False,
                        keyword_searched=keyword
                        )
        ol.save()
        print_info(f"Saved --- {link}", color=colors.BRIGHT_GREEN)

    print_info(f"Total number of links found = {links.__len__()}", colors.BRIGHT_YELLOW)

    print_info("All the links saved to database successfully", color=colors.BRIGHT_YELLOW)


def torch(keyword):
    """
    Get onion links from Torch Search Engine and store them in the database
    :param keyword: search keyword
    """
    pass


def onionland(keyword):
    """
    Get onion links from onionland Search Engine and store them in the database
    :param keyword: search keyword
    """
    pass
