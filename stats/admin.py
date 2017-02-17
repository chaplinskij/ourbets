from django.contrib.admin import ModelAdmin, site, StackedInline, TabularInline
from utility.admin import register, ReadOnlyAdminMixin, ReadOnlyAdmin, DefaultModelAdmin
from image_cropping.admin import ImageCroppingMixin

from stats.models import(
   StaticURL, Competition, Season, Round, Venue, Team, Match, Region,
   RegionGroup,
)


class CompetitionAdmin(DefaultModelAdmin):
   list_filter = ('region', )


class VenueAdmin(ImageCroppingMixin, ModelAdmin):
   search_fields = ('name',)


class MatchAdmin(DefaultModelAdmin):
   list_display = ('dbid', 'home_team', 'away_team', 'home_goals', 'away_goals', 'state', 'competition', 'round', 'start')
   list_filter = ('season', 'competition')
   search_fields = ('home_team__name', 'away_team__name')
   date_hierarchy = 'start'


register(StaticURL)
register(Competition, CompetitionAdmin)
register(Season)
register(Round)
register(Venue, VenueAdmin)
register(Team)
register(Match, MatchAdmin)
register(Region)
register(RegionGroup)

