from django.forms import (CharField, ModelForm, EmailField, HiddenInput,
   BooleanField, ValidationError, CheckboxSelectMultiple, Textarea, Form,
   ModelChoiceField, ModelMultipleChoiceField, IntegerField, ChoiceField, Select, RadioSelect,
   CheckboxInput, TextInput, URLField, URLInput, Textarea)


class HomePageForm(ModelForm):
   pass
#    class Meta:
#       model = Profile
#       exclude = (
#          'position', 'misc', 'exported', 'is_active', 'from_landing', 'paid'
#       )