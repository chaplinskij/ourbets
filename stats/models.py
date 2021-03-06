from __future__ import unicode_literals
from easy_thumbnails.files import get_thumbnailer
from django.utils.translation import ugettext_lazy as _
from django.templatetags.static import static
from django.db.models import (
   Model, CharField, ForeignKey, PositiveIntegerField, URLField, BooleanField,
   IntegerField, DateTimeField, DecimalField, ManyToManyField, TextField,
   ImageField,
)
from image_cropping.fields import ImageRatioField


class StaticURL(Model):
   url_name = URLField(_('flag URL'))


class RegionGroup(Model):
   dbid = PositiveIntegerField(_('external id'))
   name = CharField(_('name'), max_length=60)
   ordering = IntegerField(_('ordering'))
   flag = ForeignKey(StaticURL, related_name='region_group_flags')

   def __unicode__(self):
      return self.name


class Region(Model):
   dbid = PositiveIntegerField(_('external id'))
   name = CharField(_('name'), max_length=60)
   ordering = IntegerField(_('ordering'))
   flag = ForeignKey(StaticURL, related_name='region_flags')
   group = ForeignKey(RegionGroup, related_name='regions')

   def __unicode__(self):
      return self.name


class Competition(Model):
   dbid = PositiveIntegerField(_('external id'))
   name = CharField(_('name'), max_length=40)
   short_name = CharField(_('short name'), max_length=15)
   full_name = CharField(_('full name'), max_length=60)
   ordering = IntegerField(_('ordering'))
   show_league = BooleanField(_('show league tables'), default=False)
   show_assists = BooleanField(_('show assists stats'), default=False)
   show_card = BooleanField(_('show card stats'), default=False)
   show_goal = BooleanField(_('show goal stats'), default=False)
   region = ForeignKey(Region, related_name='competitions')
   flag = ForeignKey(StaticURL, related_name='competition_flags')

   def flag_url(self):
      return self.flag.url_name

   def __unicode__(self):
      return '%s - %s' % (self.region.name, self.name)


class Season(Model):
   dbid = PositiveIntegerField(_('external id'))
   name = CharField(_('name'), max_length=60)
   date_start = DateTimeField()
   date_end = DateTimeField()

   def __unicode__(self):
      return self.name


class Round(Model):
   dbid = PositiveIntegerField(_('external id'))
   name = CharField(_('name'), max_length=40)
   full_name = CharField(_('full name'), max_length=60)
   active = BooleanField(_('active'), default=False)
   has_league = BooleanField(_('has league tables'), default=False)
   has_assists = BooleanField(_('has assists stats'), default=False)
   has_card = BooleanField(_('has card stats'), default=False)
   has_goal = BooleanField(_('has goal stats'), default=False)
   season = ForeignKey(Season, related_name='seasons')
   competition = ForeignKey(Competition, related_name='rounds')

   def __unicode__(self):
      return self.name


class Venue(Model):
   dbid = PositiveIntegerField(_('external id'))
   name = CharField(_('name'), max_length=60)
   capacity = IntegerField(default=0)
   geo_lat = DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
   geo_lon = DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
   cover = ImageField(_('cover'), upload_to='venues', blank=True, null=True)
   rectangle = ImageRatioField('cover', '1200x300')

   def image_url(self, field):
      if not self.cover:
         return None

      f = self._meta.get_field(field)
      return get_thumbnailer(self.cover).get_thumbnail({
         'size': (f.width, f.height),
         'box': getattr(self, field),
         'crop': True
      }).url

   def cover_url(self):
      return self.image_url('rectangle') if self.cover else self.default_cover()

   def default_cover(self):
      return static('img/arena3.png')


   def __unicode__(self):
      return self.name


class Team(Model):
   dbid = PositiveIntegerField(_('external id'))
   name = CharField(_('name'), max_length=60)
   short_name = CharField(_('short name'), max_length=30)
   short_code = CharField(_('short code'), max_length=10)
   is_national = BooleanField(_('active'), default=False)
   show_league = BooleanField(_('show league tables'), default=False)
   show_assists = BooleanField(_('show assists stats'), default=False)
   show_card = BooleanField(_('show card stats'), default=False)
   show_goal = BooleanField(_('show goal stats'), default=False)
   venue = ForeignKey(Venue, null=True, blank=True)
   flag = ForeignKey(StaticURL, related_name='team_flags', null=True, blank=True)
   shirt = ForeignKey(StaticURL, related_name='team_shirts', null=True, blank=True)
   cover = ImageField(_('cover'), upload_to='teams', blank=True, null=True)

   def cover_url(self):
      return self.cover.url if self.cover else self.default_cover()

   def default_cover(self):
      return static('img/default_cover_team.png')

   def __unicode__(self):
      return self.name


class MatchState(Model):
   id = IntegerField(primary_key=True)
   label = CharField(_('name'), max_length=60)
   short_name = CharField(_('short code'), max_length=10)
   medium_name = CharField(_('medium name'), max_length=30)
   long_name = CharField(_('long name'), max_length=60)
   length = IntegerField(null=True, blank=True)
   offset = IntegerField(null=True, blank=True)
   min_offset = IntegerField(_('min real offset'), null=True, blank=True)
   in_game = BooleanField()
   in_play = BooleanField()
   has_score = BooleanField()
   knockout = BooleanField()
   void = BooleanField()
   is_break = BooleanField()
   ended = BooleanField()

   def __unicode__(self):
      return self.medium_name


class Outcome(Model):
   winner = CharField(max_length=20, null=True, blank=True)
   category = CharField(max_length=20)
   after_extra = BooleanField(_('After extra time'), default=False)

   def __unicode__(self):
      return self.winner


class Match(Model):
   dbid = PositiveIntegerField(_('external id'))
   home_goals = IntegerField(_('home goals'), null=True, blank=True)
   away_goals = IntegerField(_('away goals'), null=True, blank=True)
   home_dismiss = IntegerField(_('home dismissals'), default=0)
   away_dismiss = IntegerField(_('home dismissals'), default=0)
   start = DateTimeField(_('date of start'), null=True, blank=True)
   end = DateTimeField(_('date of current state'), null=True, blank=True)
   state = ForeignKey(MatchState, related_name='matches', null=True, blank=True)
   next_state = ForeignKey(MatchState, related_name='next_matches', null=True, blank=True)
   is_result = BooleanField(_('is result'), default=False)
   go_extra = BooleanField(_('go to extra time'), default=False)
   has_extra = BooleanField(_('extra time has happened'), default=False)
   home_team = ForeignKey(Team, related_name='home_matches')
   away_team = ForeignKey(Team, related_name='away_matches')
   season = ForeignKey(Season, null=True, blank=True)
   competition = ForeignKey(Competition, null=True, blank=True)
   round = ForeignKey(Round, null=True, blank=True)
   venue = ForeignKey(Venue, null=True, blank=True)
   outcome = ForeignKey(Outcome, null=True, blank=True)

   def __unicode__(self):
      return '%s - %s (%s)' % (self.home_team.name, self.away_team.name, self.start)

   def home_goals_display(self):
      return self.home_goals if self.end else '?'

   def away_goals_display(self):
      return self.away_goals if self.end else '?'


class CrowdscoresResponse(Model):
   path = CharField(max_length=50)
   params = TextField(null=True, blank=True)
   date_created = DateTimeField(auto_now_add=True)
   value = TextField()
