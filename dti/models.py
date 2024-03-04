import datetime

from django.db import models
from .utils.print_utils import *


class OnionLinks(models.Model):
    url = models.URLField(primary_key=True)
    source_name = models.CharField(max_length=100)
    source_url = models.URLField()
    visited = models.BooleanField()
    keyword_searched = models.CharField(max_length=20)
    date_searched = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if OnionLinks.objects.filter(url=self.url).exists() and args != "update":
    #         print_info(f"Skipping {self.url} ")
    #     else:
    #         print_info(f"Saving {self.url} to Database")
    #         super().save(*args, **kwargs)


class EnumeratedWebsites(models.Model):
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


class Threads(models.Model):
    thread_url = models.URLField(primary_key=True)
    thread_title = models.TextField(blank=True, null=True)
    thread_desc = models.TextField(blank=True, null=True)
    thread_author = models.TextField(blank=True, null=True)
    thread_published = models.DateTimeField(blank=True, null=True)
    enumerated = models.BooleanField(default=False)


class ThreadComments(models.Model):
    thread_url = models.ForeignKey(Threads, on_delete=models.SET_NULL, null=True)
    comment_text = models.TextField(blank=False, null=False)
    comment_author = models.TextField(blank=False, null=False)
    comment_author_title = models.TextField(blank=False, null=False)
    comment_date = models.DateTimeField(blank=True, null=True)


class DarkwebUsers(models.Model):
    user_name = models.CharField(max_length=100, primary_key=True)
    user_email = models.TextField(blank=True, null=True)
    user_phone = models.TextField(blank=True, null=True)
    user_title = models.TextField(blank=True, null=True)
    last_enumerated = models.DateTimeField(blank=True, null=True, default=None),
    associated_website = models.ForeignKey(EnumeratedWebsites, on_delete=models.CASCADE, blank=True,
                                           null=True)


class CryptocurrencyTransaction(models.Model):
    sender = models.CharField(max_length=100, ),
    receiver = models.CharField(max_length=100, )
    amount_in_crypto = models.FloatField()
    amount_in_usd = models.FloatField()
    transaction_date = models.DateTimeField(blank=True, null=True, default=None)
    associated_website = models.ForeignKey(EnumeratedWebsites, on_delete=models.CASCADE, )


class CryptoAddress(models.Model):
    crypto_address = models.CharField(max_length=100, primary_key=True)
    associated_website = models.ForeignKey(EnumeratedWebsites, on_delete=models.CASCADE, )


class ImageFiles(models.Model):
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
    user_name = models.ForeignKey(DarkwebUsers, on_delete=models.SET_NULL, null=True)
    result_title = models.TextField()
    result_description = models.TextField()
    result_link = models.TextField()
    query_string = models.TextField()
