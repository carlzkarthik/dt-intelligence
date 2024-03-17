from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse
from .forms import *
from .utils import thread_enumeration
from django.core.paginator import Paginator

import threading

from .utils.url_collector import onion_url_collector
from .utils.site_enumeration_engine import *
from .utils.thread_enumeration import *
from .utils.threat_search import *
from .utils.user_enumeration import *


def enumerate_user(request):
    """
    View Function to enumerate dark web users
    """
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        success = user_enumeration(user_name)
        return JsonResponse({'result': success})

    else:
        print_error("Error in enumerate_user")
        return JsonResponse({'result': False})


def homepage(request):
    """
    View Function to display homepage
    """
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render())


def site_enumeration_engine(request):
    """
    View Function to display site enumeration engine
    """
    if request.method == 'POST':
        form = SiteEnumerationForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            t = threading.Thread(target=enumerate_website, args=(url,))
            t.start()
    else:
        form = SiteEnumerationForm()

    context = {'form': form}
    return render(request, 'site-enumeration-engine.html', context=context)


def unvisited_site_enum(request):
    """
    View Function to run site enumeration engine on unvisited sites
    """
    if request.method == 'POST':
        status = enumerate_unvisited_websites()
        return JsonResponse({'result': status})


def unvisited_thread_enum(request):
    """
    View Function to run thread enumeration engine on unvisited thread
    """
    if request.method == 'POST':
        status = thread_enumerate()
        return JsonResponse({'result': status})


def thread_enumeration_engine(request):
    """
    View Function to display thread enumeration engine
    If the request is GET, it will display the thread enumeration engine
    If the request is POST, it will run the thread enumeration engine dark web forums
    """
    if request.method == 'POST':
        form = ThreadEnumerationForm(request.POST)
        if form.is_valid():
            thread_url = form.cleaned_data['thread_url']
            be = BreachForum()
            t = threading.Thread(target=be.enumerate, args=(thread_url,))
            t.start()
    else:
        form = ThreadEnumerationForm()

    context = {'form': form}
    return render(request, 'thread-enumeration.html', context=context)


def crypto_transaction_enumeration(request):
    """
    View Function to display crypto transaction enumeration engine
    """
    if request.method == 'POST':
        form = CryptoTransactionEnumeration(request.POST)

        if form.is_valid():
            address = form.cleaned_data['address']
            t = threading.Thread(target=enumerate_crypto_address, args=(address,))
            t.start()

    else:
        form = CryptoTransactionEnumeration()

    context = {'form': form}
    return render(request, 'crypto-transaction-enumeration.html', context=context)


def url_collector(request):
    """
    View Function to display url collector page
    """
    if request.method == 'POST':
        form = UrlCollectorForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['search_engines']
            keyword = form.cleaned_data['keyword']
            t = threading.Thread(target=onion_url_collector, args=(keyword, choice))
            t.start()

        # print("Sleeping for 10 secs")
        # sleep(10)

    else:
        form = UrlCollectorForm()

    context = {'form': form}
    return render(request, 'url-collector.html', context=context)


def onion_links(request):
    """
    View Function to display list of collected onion links
    """
    data = OnionLinks.objects.all()
    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'onion-links.html', {'page_obj': page_obj})


def enumerated_websites(request):
    """
    View Function to display list of enumerated websites
    """
    websites = EnumeratedWebsites.objects.all()
    context = {'websites': websites}
    return render(request, 'enumerated-website.html', context=context)


def threat_search(request):
    """
    View Function to display threat searching page
    """
    threat_data = ""
    if request.method == 'POST':
        form = ThreatSearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            threat_data = search_threat(keyword)
    else:
        form = ThreatSearchForm()

    context = {'form': form,
               'threat_data': threat_data, }
    return render(request, 'threat-search.html', context=context)


def darkweb_users(request):
    """
    View Function to display list of darkweb users
    """
    users = DarkwebUsers.objects.all()
    context = {'darkweb_users': users}
    return render(request, 'darkweb-users.html', context=context)


def website_details(request, website_id):
    """
    View Function to display enumerated website details
    """
    website = EnumeratedWebsites.objects.filter(website_id=website_id).first()
    context = {'website': website}
    return render(request, 'website-details.html', context=context)


def test_page(request):
    if request.method == 'POST':
        form = UserEnumerationForm(request.POST)
        enumerate_user()

    else:
        form = UserEnumerationForm()

    context = {'form': form}
    return render(request, 'test-page.html', context=context)
