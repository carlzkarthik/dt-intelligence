from django import forms


class UrlCollectorForm(forms.Form):
    choices = [
        ('ahmia', 'Ahmia'),
        ('torch', 'Torch'),
        ('all', 'All'),
    ]

    search_engines = forms.MultipleChoiceField(choices=choices,
                                               widget=forms.CheckboxSelectMultiple())
    keyword = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class SiteEnumerationForm(forms.Form):
    url = forms.URLField()


class ThreadEnumerationForm(forms.Form):
    thread_url = forms.URLField()


class CryptoTransactionEnumeration(forms.Form):
    address = forms.CharField()


class ThreatSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100)

class UserEnumerationForm(forms.Form):
    pass