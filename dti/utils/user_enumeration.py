import datetime

from ..models import *
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class UserEnumeration:
    def __init__(self):
        pass

    def enumerate_users(self):
        users = set()
        threads_users = Threads.objects.values_list('thread_author', )
        commented_users = ThreadComments.objects.values_list('comment_author', 'comment_author_title')

        for cu in commented_users:
            if not DarkwebUsers.objects.filter(user_name=cu[0].strip(), user_title=None).exists():
                DarkwebUsers(user_name=cu[0].strip(), user_title=cu[1]).save()

        for u in threads_users:
            if u[0] is not None:
                if not DarkwebUsers.objects.filter(user_name=u[0].strip(), user_title=None).exists():
                    DarkwebUsers(user_name=u[0].strip())
        # for t in threads_users:
        #     user_name = t[0]
        #     if user_name is not None:
        #         users.add(user_name)
        #
        # for user in users:
        #     # print(user)
        #     DarkwebUsers(user_name=user).save()


class GoogleDork:
    def __init__(self, user_name):
        self.user_name = user_name
        # self.base_url = f'"https://www.google.com/search?q="{self.user_name}"+%26+("dark+web"+|+"darkweb"+|+"deep+web"+|+"deepweb")+%26+("Breach+Forum"+|+"Breachforum")"'
        self.base_url = f'https://www.google.com/search?q=%22{self.user_name}%22+%26+(%22dark+web%22+|+%22darkweb%22+|+%22deep+web%22+|+%22deepweb%22)+%26+(%22Breach+Forum%22+|+%22Breachforum%22)'

    def dork_it(self):
        try:
            options = Options()
            options.add_argument('--headless')
            chrome = Chrome(options=options)
            chrome.get(self.base_url)
            chrome.implicitly_wait(100)
            bs4_contents = BeautifulSoup(chrome.page_source, 'html.parser')
            results = bs4_contents.find_all('div', class_='N54PNb')
            if not results:
                print('No results')
            else:
                for result in results:
                    title = result.find('h3').get_text()
                    desc = result.find('div', class_='VwiC3b').get_text()
                    link = result.find('a')['href']
                    print(title, '\n', desc, '\n', link)
                    print("===================")
                    darkweb_user = DarkwebUsers.objects.filter(user_name=self.user_name)
                    darkweb_user[0].last_enumerated = datetime.datetime.now()
                    darkweb_user[0].save()

                    ugd = UserGoogleDork(user_name=darkweb_user[0], result_title=title, result_description=desc,
                                         result_link=link, query_string=self.base_url)
                    ugd.save()

            # print(chrome.page_source)
            chrome.quit()
            return True
        except:
            print_error(f"Error while enumerating user --- {self.user_name}")
            return False


def user_enumeration(user_name):
    print_info(f"Enumerating user information")
    # ue = UserEnumeration()
    # ue.enumerate_users()
    gd = GoogleDork(user_name)
    return gd.dork_it()
