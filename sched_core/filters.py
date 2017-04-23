from datetime import date

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sched_core.config import local_time_now

now = local_time_now()
this_year = now.year
last_year = now.replace(year=now.year - 1).year
next_year = now.replace(year=now.year + 1).year
this_year_str = str(this_year)
last_year_str = str(last_year)
next_year_str = str(next_year)
this_year_str = str(this_year)
last_year_str = str(last_year)
next_year_str = str(next_year)

class AdminYearFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('year')

#   parameter_name = 'date_time'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (last_year_str, _(last_year_str)),
            (this_year_str, _(this_year_str)),
            (next_year_str, _(next_year_str))
        )

class AdminDateYearFilter(AdminYearFilter):
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'date'

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == last_year_str:
            return queryset.filter(date__year=last_year)
        if self.value() == this_year_str:
            return queryset.filter(date__year=this_year)
        if self.value() == next_year_str:
            return queryset.filter(date__year=next_year)

class AdminDateTimeYearFilter(AdminYearFilter):
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'date_time'

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == last_year_str:
            return queryset.filter(date_time__year=last_year)
        if self.value() == this_year_str:
            return queryset.filter(date_time__year=this_year)
        if self.value() == next_year_str:
            return queryset.filter(date_time__year=next_year)
