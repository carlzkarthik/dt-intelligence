from .utils import *
from ..models import *
from unicodedata import normalize
import threading


def enumerate_website(url):
    """
    Extract all the relevant information from a website and store them in the database
    :param url: URL of the website
    :return: None
    """
    print_info(f"Enumerating === {url}")
    if not EnumeratedWebsites.objects.filter(url=url).exists():
        web_content = get_web_content(url)
        if web_content != -1 and web_content is not None:
            bs4_contents = BeautifulSoup(web_content, 'html.parser')
            url = url
            title = ""

            if bs4_contents.title is not None:
                title = bs4_contents.title.string.strip()

            a_texts = [a_tag.text.strip() for a_tag in bs4_contents.find_all('a') if
                       a_tag.text is not None and a_tag.text.strip() != ""]

            a_href_texts = [a_tag['href'].strip() for a_tag in bs4_contents.find_all('a', href=True) if
                            a_tag['href'].strip() != ""]

            img_src_texts = [img_tag['src'].strip() for img_tag in bs4_contents.find_all('img')]

            img_alt_texts = [img_tag['alt'].strip() for img_tag in bs4_contents.find_all('img', alt=True) if
                             img_tag['alt']]

            h1_texts = [h1_tag.text.strip() for h1_tag in bs4_contents.find_all('h1') if h1_tag.text.strip() != ""]

            h2_texts = [h2_tag.text.strip() for h2_tag in bs4_contents.find_all('h2') if h2_tag.text.strip() != ""]

            h3_texts = [h3_tag.text.strip() for h3_tag in bs4_contents.find_all('h3') if h3_tag.text.strip() != ""]

            h4_texts = [h4_tag.text.strip() for h4_tag in bs4_contents.find_all('h4') if h4_tag.text.strip() != ""]

            h5_texts = [h5_tag.text.strip() for h5_tag in bs4_contents.find_all('h5') if h5_tag.text.strip() != ""]

            h6_texts = [h6_tag.text.strip() for h6_tag in bs4_contents.find_all('h6') if h6_tag.text.strip() != ""]

            div_texts = [normalize('NFKD', div_tag.text.strip().replace('\n', " ")
                                   .replace('\r', '')
                                   .replace('\t', ' ')) for div_tag in bs4_contents.find_all('div') if
                         div_tag.text.strip() != ""]

            p_texts = [normalize('NFKD', p_tag.text.strip().replace('\n', " ")
                                 .replace('\r', '')
                                 .replace('\t', ' ')) for p_tag in bs4_contents.find_all('p') if
                       p_tag.text.strip() != ""]

            span_texts = [span_tag.text.strip() for span_tag in bs4_contents.find_all('span') if
                          span_tag.text.strip() != ""]

            b_texts = [b_tag.text.strip() for b_tag in bs4_contents.find_all('b') if b_tag.text.strip() != ""]

            strong_texts = [strong_tag.text.strip() for strong_tag in bs4_contents.find_all('strong') if
                            strong_tag.text.strip() != ""]

            cite_texts = [cite_tag.text.strip() for cite_tag in bs4_contents.find_all('cite') if
                          cite_tag.text.strip() != ""]

            blockquote_texts = [blockquote_tag.text.strip() for blockquote_tag in bs4_contents.find_all('blockquote') if
                                blockquote_tag.text.strip() != ""]

            ul_texts = [ul_tag.text.strip() for ul_tag in
                        bs4_contents.find_all('ul') if ul_tag.text.strip() != ""]

            ol_texts = [ol_tag.text.strip() for ol_tag in bs4_contents.find_all('ol') if ol_tag.text.strip() != ""]

            li_texts = [li_tag.text.strip() for li_tag in bs4_contents.find_all('li') if li_tag.text.strip() != ""]

            nav_ul_li_texts = [li_tag.text.strip() for li_tag in bs4_contents.select('nav ul li') if
                               li_tag.text.strip() != ""]

            onion_links = get_onion_links(web_content)

            update_onion_link_queue(onion_links)

            emails = get_emails(web_content)

            print_info(f"Title of the page is {colors.LIGHT_YELLOW}{title}{colors.END}")

            # Construct EnumeratedWebsites object using above data
            website = EnumeratedWebsites(
                url=url,
                title=title,
                a_text=a_texts,
                a_href_text=a_href_texts,
                img_src_text=img_src_texts,
                img_alt_text=img_alt_texts,
                h1_text=h1_texts,
                h2_text=h2_texts,
                h3_text=h3_texts,
                h4_text=h4_texts,
                h5_text=h5_texts,
                h6_text=h6_texts,
                div_text=div_texts,
                p_text=p_texts,
                span_text=span_texts,
                b_text=b_texts,
                strong_text=strong_texts,
                cite_text=cite_texts,
                blockquote_text=blockquote_texts,
                ul_text=ul_texts,
                ol_text=ol_texts,
                li_text=li_texts,
                nav_ul_li_text=nav_ul_li_texts,
                last_enumerated=datetime.datetime.utcnow(),
                emails=emails
            )

            print_info(f"Saving website data to database {url}")

            # Save the data to database
            website.save()

            # Set the visited = 1 for url in onion link queue
            data = OnionLinks.objects.get(url=url)
            data.visited = 1
            data.save()

        else:
            print_error(f"Failed to enumerate websites")

    else:
        print_info(f"Website already enumerated  {url}")


def enumerate_unvisited_websites():
    """
    Enumerates unvisited websites
    Uses separate thread to each website url
    """
    olinks = OnionLinks.objects.filter(visited=0)
    link_count = olinks.__len__()
    thread_count = 10
    st = 0
    en = thread_count

    while link_count > 0:
        threads = []
        for i in range(st, en):
            t = threading.Thread(target=enumerate_website, args=(olinks[i].url,))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        st += thread_count
        en += thread_count
        link_count -= thread_count

    print_info("Website enumeration complete")
