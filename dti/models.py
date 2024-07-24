import datetime

from django.db import models
from .utils.print_utils import *
from django.db.models import Max


class OnionLinks(models.Model):
    """
    Database model for onion link queue
    This model is equivalent to Tables in MySql database
    --------------------------------------------------------
    Params
    --------------------------------------------------------
    1. url ---> onion link
    2. source_name ---> name of the source where the link was found
    3. source_url ---> url of the source where the link was found
    4. visited ---> boolean indicating whether the link was visited or not
    5. keyword_searched ---> keyword searched on search engine
    6. date_searched ---> date the link was saved on the database
    """
    url = models.URLField(primary_key=True)
    source_name = models.CharField(max_length=100)
    source_url = models.URLField()
    visited = models.BooleanField()
    keyword_searched = models.CharField(max_length=20, default=None, null=True)
    date_searched = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if OnionLinks.objects.filter(url=self.url).exists() and args != "update":
    #         print_info(f"Skipping {self.url} ")
    #     else:
    #         print_info(f"Saving {self.url} to Database")
    #         super().save(*args, **kwargs)


class EnumeratedWebsites(models.Model):
    """
    Database model for enumerated websites
    This model is equivalent to Tables in MySql database
    """
    website_id = models.IntegerField(unique=True, null=True, blank=False)
    url = models.URLField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    a_text = models.TextField(blank=True, null=True)
    a_href_text = models.TextField(blank=True, null=True)
    img_src_text = models.TextField(blank=True, null=True)
    img_alt_text = models.TextField(blank=True, null=True)
    h1_text = models.TextField(blank=True, null=True)
    h2_text = models.TextField(blank=True, null=True)
    h3_text = models.TextField(blank=True, null=True)
    h4_text = models.TextField(blank=True, null=True)
    h5_text = models.TextField(blank=True, null=True)
    h6_text = models.TextField(blank=True, null=True)
    div_text = models.TextField(blank=True, null=True)
    p_text = models.TextField(blank=True, null=True)
    span_text = models.TextField(blank=True, null=True)
    b_text = models.TextField(blank=True, null=True)
    strong_text = models.TextField(blank=True, null=True)
    cite_text = models.TextField(blank=True, null=True)
    blockquote_text = models.TextField(blank=True, null=True)
    ul_text = models.TextField(blank=True, null=True)
    ol_text = models.TextField(blank=True, null=True)
    li_text = models.TextField(blank=True, null=True)
    nav_ul_li_text = models.TextField(blank=True, null=True)
    last_enumerated = models.DateTimeField(null=False, auto_now_add=True)
    emails = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.website_id is None:  # Only set the value for new records
            max_id = EnumeratedWebsites.objects.aggregate(max_id=Max('website_id'))['max_id']
            self.website_id = (max_id or 0) + 1
        super().save(*args, **kwargs)


class Threads(models.Model):
    """
    Database model for dark web forum threads
    This model is equivalent to Tables in MySql database
    """
    thread_url = models.URLField(primary_key=True)
    thread_title = models.TextField(blank=True, null=True)
    thread_desc = models.TextField(blank=True, null=True)
    thread_author = models.TextField(blank=True, null=True)
    thread_published = models.DateTimeField(blank=True, null=True)
    enumerated = models.BooleanField(default=False)


class ThreadComments(models.Model):
    """
    Database model for dark web forum thread comments
    This model is equivalent to Tables in MySql database
    """
    thread_url = models.ForeignKey(Threads, on_delete=models.SET_NULL, null=True)
    comment_text = models.TextField(blank=False, null=False)
    comment_author = models.TextField(blank=False, null=False)
    comment_author_title = models.TextField(blank=False, null=False)
    comment_date = models.DateTimeField(blank=True, null=True)


class ScraperState(models.Model):
    forum_name = models.CharField(max_length=100, unique=True)
    last_page_number = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.forum_name} - Page {self.last_page_number}"


class DarkwebUsers(models.Model):
    """
    Database model for dark web users
    This model is equivalent to Tables in MySql database
    """
    user_name = models.CharField(max_length=100, primary_key=True)
    user_email = models.TextField(blank=True, null=True)
    user_phone = models.TextField(blank=True, null=True)
    user_title = models.TextField(blank=True, null=True)
    last_enumerated = models.DateTimeField(blank=True, null=True, default=None),
    associated_website = models.ForeignKey(EnumeratedWebsites, on_delete=models.CASCADE, blank=True,
                                           null=True)


class CryptocurrencyTransaction(models.Model):
    """
    Database model for crypto currency transactions
    This model is equivalent to Tables in MySql database
    """
    sender = models.CharField(max_length=100, ),
    receiver = models.CharField(max_length=100, )
    amount_in_crypto = models.FloatField()
    amount_in_usd = models.FloatField()
    transaction_date = models.DateTimeField(blank=True, null=True, default=None)
    associated_website = models.ForeignKey(EnumeratedWebsites, on_delete=models.CASCADE, )


class CryptoAddress(models.Model):
    """
    Database model for crypto address
    This model is equivalent to Tables in MySQL database
    """
    crypto_address = models.CharField(max_length=100, primary_key=True)
    associated_website = models.ForeignKey(EnumeratedWebsites, on_delete=models.CASCADE, )


class ImageFiles(models.Model):
    """
    Database model for image file
    This table holds the EXIF data for image files
    This model is equivalent to Tables in MySql database
    """
    img_name = models.TextField()
    img_path = models.CharField(max_length=1024)
    img_url = models.URLField()
    img_alt_text = models.TextField()
    gps_version_ide = models.TextField()
    latitude_reference = models.CharField(max_length=5)
    latitude = models.CharField(max_length=15)
    longitude_reference = models.CharField(max_length=5)
    longitude = models.CharField(max_length=15)
    altitude_reference = models.CharField(max_length=5)
    altitude = models.CharField(max_length=15)
    datetime = models.DateTimeField()
    cam_make = models.TextField()
    cam_model = models.TextField()
    cam_software = models.TextField()


class UserGoogleDork(models.Model):
    """
    Database model for google dork results
    This model is equivalent to Tables in MySQL
    """
    user_name = models.ForeignKey(DarkwebUsers, on_delete=models.SET_NULL, null=True)
    result_title = models.TextField()
    result_description = models.TextField()
    result_link = models.TextField()
    query_string = models.TextField()
