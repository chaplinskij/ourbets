from __future__ import unicode_literals
from adminsortable.models import Sortable
from django.utils.translation import ugettext_lazy as _
from django.db.models import (
   BooleanField, CharField, PositiveIntegerField, OneToOneField, ForeignKey,
   DateTimeField, Model
)

from stats.models import Match, Competition


class FeaturedMatch(Sortable):
   class Meta(Sortable.Meta):
      ordering = ['order']
      verbose_name = _('featured match')

   match = OneToOneField(Match, related_name='featured_article')
   date_updated = DateTimeField(_('updated date'), auto_now=True)

   def __unicode__(self):
      return unicode(self.match)


class FeaturedCompetition(Model):

   competition = OneToOneField(Competition, related_name='featured_competition')

   def __unicode__(self):
      return '%s - %s' % (self.competition.region.name, self.competition.name)