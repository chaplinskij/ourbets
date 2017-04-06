from django.contrib.admin import ModelAdmin, site, StackedInline, TabularInline
from utility.admin import register, ReadOnlyAdminMixin, ReadOnlyAdmin, DefaultModelAdmin
from image_cropping.admin import ImageCroppingMixin
from adminsortable.admin import SortableAdmin

from tote.models import(
   FeaturedMatch, FeaturedCompetition
)


class FeaturedMatchAdmin(SortableAdmin):
   raw_id_fields = ('match',)


class FeaturedCompetitionAdmin(DefaultModelAdmin):
   raw_id_fields = ('competition',)

register(FeaturedMatch, FeaturedMatchAdmin)
register(FeaturedCompetition, FeaturedCompetitionAdmin)
