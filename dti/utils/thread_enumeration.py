import datetime
from urllib.parse import urljoin
from .utils import *
from ..models import *

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType


class OnniForum():
    def __init__(self):
        super().__init__()
        self.thread_base_url = "http://onnii6niq53gv3rvjpi7z5axkasurk2x5w5lwliep4qyeb2azagxn4qd.onion/thread-"
        self.thread_link_pattern = re.compile(r'thread-\d+\.html$')
        self.onni_forum_url = "http://onnii6niq53gv3rvjpi7z5axkasurk2x5w5lwliep4qyeb2azagxn4qd.onion/member.php?action=login"
        self.onni_forum_database_url = "http://onnii6niq53gv3rvjpi7z5axkasurk2x5w5lwliep4qyeb2azagxn4qd.onion/forum-7.html"

    def enumerate(self, driver):
        page = 1
        thread_urls = []
        while page < 13:
            driver.get(
                f"http://onnii6niq53gv3rvjpi7z5axkasurk2x5w5lwliep4qyeb2azagxn4qd.onion/forum-7-page-{page}.html")
            html = driver.page_source
            bs4_contents = BeautifulSoup(html, 'html.parser')
            a_tags = bs4_contents.find_all('a', href=True)

            for tag in a_tags:
                if self.thread_link_pattern.search(tag['href']):
                    thread_urls.append(f"{self.thread_base_url.rstrip('thread-')}{tag['href']}")

            print_info(f"Running OnniForum Thread Enumeration")

            for t in thread_urls:
                if not Threads.objects.filter(thread_url=t).exists():
                    try:
                        driver.get(t)
                        page_source = driver.page_source
                        bs4_contents = BeautifulSoup(page_source, 'html.parser')

                        thread_url = t
                        thread_title = bs4_contents.tbody.find_all('tr')[0].find_all('strong')[1].text
                        thread_desc = bs4_contents.find(id='posts').find(class_='post_body').text
                        thread_author = bs4_contents.select('#posts')[0].find(class_='author_information').find(
                            'a').text
                        thread_published = bs4_contents.find(id='posts').find(class_='post_date').text.split('\n')[0]
                        thread_published = convert_time_string(thread_published)

                        t = Threads(thread_url=thread_url,
                                    thread_title=thread_title,
                                    thread_desc=thread_desc,
                                    thread_author=thread_author,
                                    thread_published=thread_published)

                        t.save()

                        print_info(f"Successfully enumerated thread: [ {t} ]")

                        if page > 1:
                            scraper_state, created = ScraperState.objects.get_or_create(forum_name="OnniForum")
                            scraper_state.last_page_number = page + 1
                            scraper_state.save()

                    except Exception as e:
                        print_error(f"Error while enumerating thread: [ {t} ]")
                        print_error(f"{e}")

                else:
                    print_info(f"Thread already enumerated: [ {t} ]")
            page = ScraperState.objects.filter(forum_name='OnniForum')[0].last_page_number

    def login(self):
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'socksProxy': '127.0.0.1:9050',
            'socksVersion': 5,
        })

        options = Options()
        options.proxy = proxy
        options.binary_location = "/home/dimitri/Downloads/tor-browser/Browser/firefox"
        # options.add_argument('--headless')

        driver = Firefox(options=options)

        try:
            print_info(f"Navigating to {self.onni_forum_url}")
            driver.get(self.onni_forum_url)

            driver.find_element(By.NAME, 'username').send_keys('username')
            driver.find_element(By.NAME, 'password').send_keys('password')
            print_info(f"Please press enter once you looged in...")
            input()
            return driver
        except Exception as e:
            print_error(f"Error while logging in to Onni Forum\n{e}")


class BreachForum:
    def __init__(self):
        self.breach_forum_url = "http://breached26tezcofqla4adzyn22notfqwcac7gpbrleg4usehljwkgqd.onion/"
        self.thread_base_url = "http://breached26tezcofqla4adzyn22notfqwcac7gpbrleg4usehljwkgqd.onion/Thread-"
        self.breach_forum_database_url = "http://breached26tezcofqla4adzyn22notfqwcac7gpbrleg4usehljwkgqd.onion/Forum-Databases?page=1"

    def enumerate(self, driver):
        page = 1
        thread_urls = []

        while page < 20:
            driver.get(
                f"http://breached26tezcofqla4adzyn22notfqwcac7gpbrleg4usehljwkgqd.onion/Forum-Databases?page={page}")
            html = driver.page_source
            bs4_contents = BeautifulSoup(html, 'html.parser')
            inline_row = bs4_contents.find_all(class_='inline_row')
            tds = []

            for ir in inline_row:
                tds.append(ir.find_all('td')[1])

            for td in tds:
                thread_urls.append(f"{self.breach_forum_url}{td.find('a')['href'].replace('?action=newpost', '')}")

            print_info(f"Running Breach Forum Thread Enumeration")

            for t in thread_urls:
                if not Threads.objects.filter(thread_url=t).exists():
                    try:
                        driver.get(t)
                        page_source = driver.page_source
                        bs4_contents = BeautifulSoup(page_source, 'html.parser')

                        thread_url = t
                        thread_title = bs4_contents.find('tbody').find(class_='thread-info__name').text
                        thread_desc = bs4_contents.find('tbody').find(class_='post_body').text
                        thread_author = bs4_contents.find('tbody').find(class_='post__user-profile').text.strip()
                        thread_published = \
                            bs4_contents.find('tbody').find(class_='thread-info__datetime').text.split('-')[1].strip()
                        thread_published = convert_date_time(thread_published)
                        t = Threads(thread_url=thread_url,
                                    thread_title=thread_title,
                                    thread_desc=thread_desc,
                                    thread_author=thread_author,
                                    thread_published=thread_published,
                                    thread_source="Breach Forum")

                        t.save()

                        print_info(f"Successfully enumerated thread: [ {t} ]")



                    except Exception as e:
                        print_error(f"Error while enumerating thread: [ {t} ]")
                        print_error(f"{e}")

                else:
                    print_info(f"Thread is already enumerated: [ {t} ]")

            if page > 1:
                scraper_state, created = ScraperState.objects.get_or_create(forum_name="BreachForum")
                scraper_state.last_page_number = page + 1
                scraper_state.save()

            page = ScraperState.objects.filter(forum_name='BreachForum')[0].last_page_number

    def login(self):

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'socksProxy': '127.0.0.1:9050',
            'socksVersion': 5,
        })

        options = Options()
        options.proxy = proxy
        options.binary_location = "/home/dimitri/Downloads/tor-browser/Browser/firefox"
        # options.add_argument('--headless')

        driver = Firefox(options=options)

        try:
            print_info(f"Navigating to {self.breach_forum_url}")
            driver.get(self.breach_forum_url)
            print_info(f"Please press enter once you looged in...")
            input()
            return driver
        except Exception as e:
            print_error(f"Error while logging in to Breach Forum\n{e}")
