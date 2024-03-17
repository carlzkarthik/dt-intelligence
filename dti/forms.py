from django import forms


class UrlCollectorForm(forms.Form):
    """
    Onion Link Collector Form
    """
    choices = [
        ('ahmia', 'Ahmia'),
        ('torch', 'Torch'),
        ('all', 'All'),
    ]

    search_engines = forms.MultipleChoiceField(choices=choices,
                                               widget=forms.CheckboxSelectMultiple())
    keyword = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class SiteEnumerationForm(forms.Form):

    """
    Site Enumeration Engine Form
    """
    url = forms.URLField()


class ThreadEnumerationForm(forms.Form):
    """
    Thread Enumeration Form
    """
    thread_url = forms.URLField()


class CryptoTransactionEnumeration(forms.Form):
    """
    Crypto Transaction Enumeration Form
    """
    address = forms.CharField()


class ThreatSearchForm(forms.Form):
    """
    Threat Search Form
    """
    keyword = forms.CharField(max_length=100)

class UserEnumerationForm(forms.Form):
    """
    User Enumeration Form
    """
    pass