from django.contrib.admin import ModelAdmin, site, StackedInline, TabularInline
from utility.admin import register, ReadOnlyAdminMixin, ReadOnlyAdmin, DefaultModelAdmin
from image_cropping.admin import ImageCroppingMixin
from adminsortable.admin import SortableAdmin

from tote.models import(
   FeaturedMatch, FeaturedCompetition, Forecast, Tournament, TournamentMatch,
   TournamentTable
)


class FeaturedMatchAdmin(SortableAdmin):
   raw_id_fields = ('match',)


class FeaturedCompetitionAdmin(SortableAdmin):
   raw_id_fields = ('competition',)


class TournamentMatchInline(TabularInline):
   model = TournamentMatch
   extra = 1
   fields = ('match',)
   raw_id_fields = ('match',)


class TournamentAdmin(DefaultModelAdmin):
   inlines = (TournamentMatchInline, )


register(FeaturedMatch, FeaturedMatchAdmin)
register(FeaturedCompetition, FeaturedCompetitionAdmin)
register(Forecast)
register(Tournament, TournamentAdmin)
register(TournamentMatch)
register(TournamentTable)
