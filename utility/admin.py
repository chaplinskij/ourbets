from django.contrib.admin import ModelAdmin, site


class DefaultModelAdmin(ModelAdmin):

   def __init__(self, model, admin_site):
      lst = self.list_display
      if not lst or lst == ('__str__',):
         self.list_display = [field.name for field in model._meta.fields \
                              if field.name != "id"]
      super(DefaultModelAdmin, self).__init__(model, admin_site)


class ReadOnlyAdminMixin(object):
   def get_readonly_fields(self, request, obj=None):
      return [f.name for f in self.model._meta.fields]

   def has_add_permission(self, request, obj=None):
      return False

   def has_delete_permission(self, request, obj=None):
      return False

   actions = None


class ReadOnlyAdmin(ReadOnlyAdminMixin, DefaultModelAdmin):
   pass


def register(model, admin_model=DefaultModelAdmin, **options):
   site.register(model, admin_model, **options)


