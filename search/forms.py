# -*- coding: utf-8 -*-
from django import forms

from search.models import SearchTerm


class SearchForm(forms.ModelForm):
    """
    form class for accepting search terms
    """

    class Meta:
        model = SearchTerm
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        default_text = 'Search'
        self.fields['q'].widget.attrs['value'] = default_text
        self.fields['q'].widget.attrs['onfocus'] = "if (this.value=='" + default_text + "')this.value = ''"

    include = ('q',)