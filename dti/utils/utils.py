import re
from .print_utils import *

from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from requests_tor import RequestsTor
from .crypto_transaction import *
from ..models import OnionLinks

from datetime import datetime, timedelta


def connect_to_tor():
    """
    connect to TOR network
    :return: session object
    """
    sess = requests.session()
    sess.proxies = {'http': 'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'}
    return sess


def get_web_content(url):
    """
    Get HTML contents of a web page
    :param url: URL of the web page
    :return: HTML web content or -1 if an error occurs
    """

    print_info(f"Requesting web page {url}")
    try:
        rt = RequestsTor(tor_ports=(9050,), tor_cport=(9150,))
        web_content = rt.get(url).text
        return web_content
    except:
        print_error(f"Error while requesting webpage for ---> {url}")
        return -1


def get_web_content_selenium(url):
    """
    Get HTML contents of a web page using selenium
    :param url: URL of the web page
    :return: HTML web content or -1 if an error occurs
    """
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'socksProxy': '127.0.0.1:9050',
        'socksVersion': 5,
    })
    options = Options()
    options.proxy = proxy
    options.binary_location = "/home/dimitri/Downloads/tor-browser/Browser/firefox"
    # options.add_argument('--headless')
    # options.binary_location = '/path/to/normal/firefox'  # works
    driver = Firefox(options=options)  # use path to standard `Firefox`

    try:
        driver.get(url)
        contents = driver.page_source
        driver.quit()
    except Exception as e:
        print_error(f"Error While Enumerating {url}\n{e}")
        driver.close()
        return -1

    return contents


def get_emails(web_content):
    """
    Get emails from web page contents using regular expression
    :param web_content: HTML web content
    :return: List of email addresses
    """
    email_pattern = r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-z]+'
    matches = re.findall(email_pattern, web_content)
    return matches


def get_onion_links(web_content):
    """
    Get onion links from web page contents using regular expression
    :param web_content: HTML web content
    :return: List of onion links
    """
    onion_link_pattern = r'[htp\/\/:]{0,7}[a-z0-9]{16,56}\.onion\/*'
    matches = re.findall(onion_link_pattern, web_content)
    unique_urls = set()
    for m in matches:
        m = m.rstrip('/')
        if m.startswith("http://"):
            unique_urls.add(m)
        else:
            url = "http://" + m
            unique_urls.add(url)

    return unique_urls


def update_onion_link_queue(onion_links, src_name, src_url, visited=False, keyword_searched=None, ):
    """
    Update onion links queue
    If onion link already exists, do nothing else add it to queue(Database table)
    :param onion_links: List of onion links
    :param src_name: Name of the source where the links are found
    :param src_url: URL of the source where the links are found
    :param visited: Flag to indicate if the link is already visited
    :param keyword_searched: Keyword searched on the search engine
    :return: None
    """

    # Loop through all the links
    for link in onion_links:
        ol = OnionLinks(url=link,
                        visited=visited,
                        keyword_searched=keyword_searched,
                        source_name=src_name,
                        source_url=src_url)

        if not OnionLinks.objects.filter(url=link, source_name=src_name):
            ol.save()
            print_info(f"Saved --- {link}", color=colors.BRIGHT_GREEN, info=f"INFO-{src_name}")

    print_info(f"Total number of links found from {src_name} = {onion_links.__len__()}", colors.BRIGHT_YELLOW)
    print_info("All the links saved to database successfully", color=colors.BRIGHT_YELLOW)

def enumerate_crypto_address(address):
    print(address)
    bc = Blockchain()
    bc.get_transaction(address)


from datetime import datetime, timedelta
import re


def convert_time_string(time_string):
    # Strip any leading or trailing whitespace
    time_string = time_string.strip()

    # Regular expression to match absolute date time format
    absolute_time_pattern = re.compile(r'\d{2}-\d{2}-\d{4}, \d{2}:\d{2} [AP]M')

    if absolute_time_pattern.match(time_string):
        # Handle absolute date time format
        try:
            date_object = datetime.strptime(time_string, "%m-%d-%Y, %I:%M %p")
            return date_object
        except ValueError as e:
            print(f"[ ERROR ] {e}")
            return None
    else:
        # Handle relative time format
        now = datetime.now()
        parts = time_string.split()
        number = int(parts[0])
        unit = parts[1]

        if "hour" in unit:
            delta = timedelta(hours=number)
        elif "minute" in unit:
            delta = timedelta(minutes=number)
        elif "second" in unit:
            delta = timedelta(seconds=number)
        elif "day" in unit:
            delta = timedelta(days=number)
        else:
            raise ValueError("Unknown time unit")

        # Subtract the delta from the current time
        return now - delta


def convert_date_time(date_str):
    try:
        # Define the format for the full date string
        full_date_format = "%A %B %d, %Y at %I:%M %p"

        # Try to parse the full date string
        date_time = datetime.strptime(date_str, full_date_format)
        return date_time
    except ValueError:
        # If parsing fails, check for "x hours ago" or "x minutes ago" pattern
        match = re.match(r"(\d+) (hours|minutes) ago", date_str)
        if match:
            amount, unit = match.groups()
            amount = int(amount)
            now = datetime.now()
            if unit == "hours":
                return now - timedelta(hours=amount)
            elif unit == "minutes":
                return now - timedelta(minutes=amount)

    # If no patterns match, return None or raise an error
    return None
