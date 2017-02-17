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


register(StaticURL)
register(Competition, CompetitionAdmin)
register(Season)
register(Round)
register(Venue, VenueAdmin)
register(Team)
register(Match)
register(Region)
register(RegionGroup)

