from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('site-enumeration-engine', views.site_enumeration_engine, name='site-enumeration-engine'),
    path('thread-enumeration-engine', views.thread_enumeration_engine, name='thread-enumeration-engine'),
    path('crypto-transaction-enumeration', views.crypto_transaction_enumeration, name='crypto-transaction-enumeration'),
    path('url-collector', views.url_collector, name="url-collector"),
    path('onion-links', views.onion_links, name="onion-links"),
    path('enumerated-websites', views.enumerated_websites, name="enumerated-websites"),
    path('threat-search', views.threat_search, name="threat-search"),
    path('darkweb-users', views.darkweb_users, name="darkweb-users"),
    path('enumerate_user', views.enumerate_user, name="enumerate_user"),
    path('unvisited-site-enum', views.unvisited_site_enum, name="unvisited-site-enum"),
    path('unvisited-thread-enum', views.unvisited_thread_enum, name="unvisited-thread-enum"),
    path('enumerated-website/details/<int:website_id>', views.website_details, name="details"),
    path('test-page', views.test_page, name="test-page"),
]
