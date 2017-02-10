from django.conf import settings
from datetime import datetime
from django.utils import timezone
import requests, pytz, json

from stats.models import (
   StaticURL, RegionGroup, Region, Competition, Season, Round, Venue, Team,
   MatchState, Match, Outcome, CrowdscoresResponse
)


class Crowdscores(object):
   api_key = settings.CROWDSCORES_API_KEY

   def _get_request(self, path, params=None):
      params = params or dict()
      params['api_key'] = self.api_key
      r = requests.get('https://api.crowdscores.com/v1/' + path, params=params)
      data = r.json()
      del(params['api_key'])
      CrowdscoresResponse.objects.create(
         path=path,
         params=params,
         value=json.dumps(data)
      )
      return data

   def update_competitions(self, data=None):
      path = 'competitions'
      if not data:
         data = self._get_request(path)

      for item in data:
         r_data = item['region']
         r_flag, _ = StaticURL.objects.get_or_create(url_name=r_data['flagUrl'])
         rg_data = r_data['regionGroup']
         rg_flag, _ = StaticURL.objects.get_or_create(url_name=rg_data['flagUrl'])
         reg_group, _ = RegionGroup.objects.update_or_create(
            dbid=rg_data['dbid'],
            defaults={
               'ordering': rg_data['ordering'],
               'name': rg_data['name'],
               'flag': rg_flag
            }
         )
         region, _ = Region.objects.update_or_create(
            dbid=r_data['dbid'],
            defaults={
               'ordering': r_data['ordering'],
               'name': r_data['name'],
               'flag': r_flag,
               'group': reg_group
            }
         )

         flag, _ = StaticURL.objects.get_or_create(url_name=item['flagUrl'])

         Competition.objects.update_or_create(
            dbid=item['dbid'],
            defaults={
               'ordering': item['ordering'],
               'name': item['name'],
               'short_name': item['shortName'],
               'full_name': item['fullName'],
               'show_league': item['showLeagueTables'],
               'show_assists': item['showAssistStats'],
               'show_card': item['showCardStats'],
               'show_goal': item['showGoalStats'],
               'flag': flag,
               'region': region
            }
         )

   def update_seasons(self, data=None):
      path = 'seasons'
      if not data:
         data = self._get_request(path)

      for item in data:
         start = datetime.fromtimestamp(item['start']/1000., tz=pytz.utc)
         end = datetime.fromtimestamp(item['end']/1000., tz=pytz.utc)
         Season.objects.update_or_create(
            dbid=item['dbid'],
            defaults={
               'name': item['name'],
               'date_start': start,
               'date_end': end
            }
         )

   def update_rounds(self, data=None):
      path = 'rounds'
      if not data:
         data = self._get_request(path)

      for item in data:
         season, _ = Season.objects.get_or_create(dbid=item['season']['dbid'])
         competition, _ = Competition.objects.get_or_create(dbid=item['competition']['dbid'])

         Round.objects.update_or_create(
            dbid=item['dbid'],
            defaults={
               'name': item['name'],
               'full_name': item['fullName'],
               'active': item['active'],
               'has_league': item['hasLeagueTable'],
               'has_assists': item['hasAssistStats'],
               'has_card': item['hasCardStats'],
               'has_goal': item['hasGoalStats'],
               'season': season,
               'competition': competition
            }
         )

   def update_teams(self, data=None):
      path = 'teams'
      if not data:
         data = self._get_request(path)

      for item in data:
         venue_data = item['defaultHomeVenue']
         venue = None
         if venue_data:
            venue_geo = venue_data['geolocation']
            geo_lat = venue_geo['latitude'] if venue_geo else None
            geo_lon = venue_geo['longitude'] if venue_geo else None
            venue, _ = Venue.objects.update_or_create(
               dbid=venue_data['dbid'],
               defaults={
                  'capacity': venue_data['capacity'] or 0,
                  'name': venue_data['name'],
                  'geo_lat': geo_lat,
                  'geo_lon': geo_lon
               }
            )

         flag, _ = StaticURL.objects.get_or_create(url_name=item['flagUrl'])
         shirt, _ = StaticURL.objects.get_or_create(url_name=item['shirtUrl'])
         Team.objects.update_or_create(
            dbid=item['dbid'],
            defaults={
               'name': item['name'],
               'short_name': item['shortName'],
               'short_code': item['shortCode'],
               'is_national': item['isNational'],
               'show_league': item['showLeagueTables'],
               'show_assists': item['showAssistStats'],
               'show_card': item['showCardStats'],
               'show_goal': item['showGoalStats'],
               'venue': venue,
               'flag': flag,
               'shirt': shirt
            }
         )

   def update_states(self, data=None):
      path = 'football_states'
      if not data:
         data = self._get_request(path)

      for item in data.values():
         MatchState.objects.update_or_create(
            id=item['stateCode'],
            defaults={
               'label': item['label'],
               'short_name': item['shortName'],
               'medium_name': item['mediumName'],
               'long_name': item['longName'],
               'length': item['length'],
               'offset': item['offset'],
               'min_offset': item.get('minRealOffset'),
               'in_game': item['inGame'],
               'in_play': item['inPlay'],
               'has_score': item['hasScore'],
               'knockout': item['knockout'],
               'void': item['void'],
               'is_break': item['break'],
               'ended': item['ended'],
            }
         )

   def update_matches(self, params=None, data=None):
      path = 'matches'
      if not data:
         data = self._get_request(path, params)

      for item in data:
         home_team, _ = Team.objects.get_or_create(dbid=item['homeTeam']['dbid'])
         away_team, _ = Team.objects.get_or_create(dbid=item['awayTeam']['dbid'])
         season, _ = Season.objects.get_or_create(dbid=item['season']['dbid'])
         competition, _ = Competition.objects.get_or_create(dbid=item['competition']['dbid'])
         try:
            venue, _ = Venue.objects.get_or_create(dbid=item['venue']['dbid'])
         except:
            venue = None
         round, _ = Round.objects.get_or_create(dbid=item['round']['dbid'])
         out_c = item['outcome']
         outcome, _ = Outcome.objects.get_or_create(
            winner=out_c['winner'],
            category=out_c['type'],
            after_extra=out_c['afterExtraTime']
         ) if out_c else (None, None)

         state = MatchState.objects.get(pk=item['currentState'])
         ns = item['nextState']
         next_states = MatchState.objects.get(pk=ns) if ns else None

         start = datetime.fromtimestamp(item['start'] / 1000., tz=pytz.utc)

         cur_date = item['currentStateStart']
         end = datetime.fromtimestamp(cur_date / 1000., tz=pytz.utc) if cur_date else None

         Match.objects.update_or_create(
            dbid=item['dbid'],
            defaults={
               'home_goals': item['homeGoals'],
               'away_goals': item['awayGoals'],
               'home_dismiss': item['dismissals']['home'],
               'away_dismiss': item['dismissals']['away'],
               'start': start,
               'end': end,
               'state': state,
               'next_state': next_states,
               'is_result': item['isResult'],
               'go_extra': item['goToExtraTime'],
               'has_extra': item['extraTimeHasHappened'],
               'home_team': home_team,
               'away_team': away_team,
               'season': season,
               'competition': competition,
               'round': round,
               'venue': venue,
               'outcome': outcome
            }
         )
