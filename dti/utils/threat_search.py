from ..models import *


class ThreatData:
    def __init__(self, threads_title_search="", threads_description_search="", threads_comments_search=""):
        self.threads_title = threads_title_search
        self.threads_description = threads_description_search
        self.threads_comment = threads_comments_search


def search_threat(keyword):
    print("inside threat search")
    threads_title_search = Threads.objects.filter(thread_title__icontains=keyword)
    threads_description_search = Threads.objects.filter(thread_desc__icontains=keyword)
    threads_comments_search = ThreadComments.objects.filter(comment_text__icontains=keyword)
    td = ThreatData(threads_title_search, threads_description_search, threads_comments_search)

    return td
