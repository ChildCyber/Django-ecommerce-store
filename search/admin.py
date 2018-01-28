# -*- coding: utf-8 -*-
from django.contrib import admin

from search.models import SearchTerm


# Register your models here.
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ip_address', 'search_date')
    list_filter = ('ip_address', 'user', 'q')
    exclude = ('user',)


admin.site.register(SearchTerm, SearchTermAdmin)
