from __future__ import unicode_literals
from adminsortable.models import Sortable
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import (
   BooleanField, CharField, IntegerField, OneToOneField, ForeignKey,
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


class FeaturedCompetition(Sortable):
   class Meta(Sortable.Meta):
      ordering = ['order']

   competition = OneToOneField(Competition, related_name='featured_competition')

   def __unicode__(self):
      return '%s - %s' % (self.competition.region.name, self.competition.name)


class Tournament(Model):
   name = CharField(_('name'), max_length=60)
   creator = ForeignKey(User)
   date_created = DateTimeField(auto_now_add=True)

   def __unicode__(self):
      return self.name


class TournamentMatch(Model):
   tournament = ForeignKey(Tournament, related_name='matches')
   match = ForeignKey(Match, related_name='tournaments_matches')
   date_created = DateTimeField(auto_now_add=True)

   def __unicode__(self):
      return '%s: %s' % (self.tournament, unicode(self.match))

   def save(self, *args, **kwargs):
      if self.pk is None and self.match.state.has_score==False:
         super(TournamentMatch, self).save(*args, **kwargs)
         users = TournamentTable.objects.filter(tournament=self.tournament)
         for user in users:
            Forecast.objects.get_or_create(
               t_match=self,
               user=user
            )
      else:
         super(TournamentMatch, self).save(*args, **kwargs)


class Forecast(Model):
   t_match = ForeignKey(TournamentMatch, related_name='forecasts')
   user = ForeignKey(User, related_name='forecasts')
   home_goals = IntegerField(_('forecast home goals'), null=True, blank=True)
   away_goals = IntegerField(_('forecast away goals'), null=True, blank=True)
   date_updated = DateTimeField(auto_now=True)
   score = IntegerField(_('score'), default=0)


class TournamentTable(Model):
   tournament = ForeignKey(Tournament)
   user = ForeignKey(User, related_name='tournaments')
   total_score = IntegerField(_('total score'), default=0)
   date_created = DateTimeField(auto_now_add=True)

   def save(self, *args, **kwargs):
      if self.pk is None:
         super(TournamentTable, self).save(*args, **kwargs)
         t_matches = TournamentMatch.objects.filter(tournament=self.tournament)
         for t_match in t_matches:
            if t_match.match.state.has_score==False:
               Forecast.objects.get_or_create(
                  t_match=t_match,
                  user=self.user
               )
      else:
         super(TournamentTable, self).save(*args, **kwargs)
