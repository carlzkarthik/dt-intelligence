import datetime
from urllib.parse import urljoin
from .utils import *
from ..models import Threads, ThreadComments


class ThreadEnumeration:
    def __init__(self):
        self.website_url = ""
        self.thread_base_url = ""
        self.type_of_site = ""
        self.thread_link_pattern = ""

    def get_webcontent(self, url):
        """
        Get web contents of the thread link
        :param url: url of the thread
        :return: web contents of the thread
        """
        web_content = get_web_content(url)
        return web_content


class BreachForum(ThreadEnumeration):

    def __init__(self):
        super().__init__()
        self.thread_base_url = "http://breachedu76kdyavc6szj6ppbplfqoz3pgrk3zw57my4vybgblpfeayd.onion/Thread-"
        self.thread_link_pattern = "Thread-[\-\w]+"

    def enumerate(self, thread_url):
        """
        Extract all the relevant information about forum thread
        :param thread_url: url of the thread
        :return: None
        """
        global thread
        print_info(f"Running Breach Forum Thread Enumeration")
        print_info(f"Enumerating Thread ---> {thread_url}")
        web_content = self.get_webcontent(thread_url)
        bs4_content = BeautifulSoup(web_content, 'html.parser')
        thread_links = self.get_thread_links(bs4_content)
        self.save_thread_link_to_db(thread_links)
        first_page = True
        while True:
            current_page = bs4_content.find('span', class_='pagination_current')
            if current_page is not None:
                current_page = int(current_page.get_text())
            else:
                if first_page:
                    current_page = 1
                else:
                    print_info(f"Thread Enumeration Complete for {thread_url}")
                    return 1

            if current_page == 1:
                thread = self.save_thread_details(thread_url, bs4_content)

                if thread != -1:
                    comments = bs4_content.find_all('div', class_='post')
                    comments.pop(0)
                    self.save_comments(thread, comments)

            else:
                print_info(f"|____ Visiting page {current_page + 1}\n")
                comments = bs4_content.find_all('div', class_='post')
                self.save_comments(thread, comments)

            next_page_url = bs4_content.find('a', class_='pagination_next')

            if next_page_url is not None:
                next_page_url = next_page_url['href']
                next_page_url = urljoin(self.thread_base_url, next_page_url)
                bs4_content = BeautifulSoup(self.get_webcontent(next_page_url), 'html.parser')
            else:
                print_info(f"Thread Enumeration Complete for {thread_url}")
                return 1

            first_page = False

    def save_thread_details(self, thread_url, bs4_content):
        """
        Save thread details to database
        Extract relevant information from the bs4 content
        :param thread_url: URL of the thread
        :param bs4_content: BeautifulSoup object
        :return: None
        """

        # Define the input and output formats
        input_format = "%A %B %d, %Y at %I:%M %p"
        output_format = "%Y-%m-%d %H:%M"

        try:
            t_url = thread_url
            t_title = bs4_content.find('span', class_='thread-info__name').get_text()
            t_desc = bs4_content.find('div', class_='post_whole').get_text()
            t_author = bs4_content.find('div', class_='thread-info__datetime').get_text().split(' ')[1]
            t_published_date = bs4_content.find('div', class_='thread-info__datetime').get_text().split('-')[1]
            t_published_date = t_published_date.replace('\t', '').replace('\r', '').replace('\n', '').strip()
            t_published_date = datetime.datetime.strptime(t_published_date, input_format).strftime(output_format)

            t = Threads(thread_url=t_url, thread_title=t_title, thread_desc=t_desc,
                        thread_author=t_author,
                        thread_published=t_published_date,
                        enumerated=1)

            t.save()
            print_info(f"Saved Thread to Database {thread_url}")
            return t

        except:
            print_error(f"Failed to enumerate thread {thread_url}")
            return -1

    def save_comments(self, thread_url, comments):
        """
        Save comments to the database
        :param thread_url: URL of the thread
        :param comments: List of comments
        :return: None
        """
        # Define the input and output formats
        input_format = "%m-%d-%Y, %I:%M %p"
        output_format = "%Y-%m-%d %H:%M"

        for comm in comments:
            c_text = comm.find('div', class_='post_body').get_text()
            c_author = comm.find('div', class_='post__user-profile').get_text()
            c_author_title = comm.find('div', class_='post__user-title').get_text()
            try:

                c_date = comm.find('span', class_='post_date').get_text()[0:20]
                c_date = datetime.datetime.strptime(c_date, input_format).strftime(output_format)

            except:
                c_date = None
            c = ThreadComments(comment_text=c_text,
                               comment_author=c_author,
                               comment_author_title=c_author_title,
                               comment_date=c_date,
                               thread_url=thread_url)
            c.save()

    def get_thread_links(self, bs4_content):
        """
        Get thread link from web content using BeautifulSoup
        :param bs4_content: web content (BeautifulSoup object)
        :return: List of thread links
        """
        matches = set()
        a_tags = bs4_content.find_all('a')
        for a in a_tags:
            href = a.get('href', '')
            match = re.search(self.thread_link_pattern, href)
            if match:
                matches.add(match.group().replace("Thread-", ""))

        return matches

    def save_thread_link_to_db(self, thread_links):
        """
        Save thread links found in the web content into the database
        :param thread_links: List of thread links found in the web content
        :return: None
        """
        print_info(f"Saving External Thread Links")
        for thread_link in thread_links:
            thread_link = f"{self.thread_base_url}{thread_link}"
            if not Threads.objects.filter(thread_url=thread_link).exists():
                print_info(f"|____ {thread_link}")
                t = Threads(thread_url=thread_link,
                            enumerated=0)
                t.save()
            else:
                print_info(f"Already exit in the database {thread_link}")


def thread_enumerate():
    te = BreachForum()
    while True:
        thread_links = Threads.objects.filter(enumerated=0)

        if not thread_links:
            return 1

        for thread in thread_links:
            te.enumerate(thread.thread_url)

        print_info("========= END ===========")
