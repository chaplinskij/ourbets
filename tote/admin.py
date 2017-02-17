from django.contrib.admin import ModelAdmin, site, StackedInline, TabularInline
from utility.admin import register, ReadOnlyAdminMixin, ReadOnlyAdmin, DefaultModelAdmin
from image_cropping.admin import ImageCroppingMixin
from adminsortable.admin import SortableAdmin

from tote.models import(
   FeaturedMatch,
)


class FeaturedMatchAdmin(SortableAdmin):
   raw_id_fields = ('match',)


register(FeaturedMatch, FeaturedMatchAdmin)
