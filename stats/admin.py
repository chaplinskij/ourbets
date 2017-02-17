from django.contrib.admin import ModelAdmin, site, StackedInline, TabularInline
from utility.admin import register, ReadOnlyAdminMixin, ReadOnlyAdmin, DefaultModelAdmin

from stats.models import(
   StaticURL, Competition, Season, Round, Venue, Team, Match, Region,
   RegionGroup,
)


class CompetitionAdmin(DefaultModelAdmin):
   list_filter = ('region', )




register(StaticURL)
register(Competition, CompetitionAdmin)
register(Season)
register(Round)
register(Venue)
register(Team)
register(Match)
register(Region)
register(RegionGroup)

