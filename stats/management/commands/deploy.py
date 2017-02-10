from django.core.management.base import BaseCommand
from stats.services import Crowdscores
from stats.models import CrowdscoresResponse

import json


class Command(BaseCommand):

   def add_arguments(self, parser):
      parser.add_argument('-d', '--database', dest='database', action='store_true')

   def handle(self, *args, **options):
      cs = Crowdscores()
      FUNCTIONS = dict(
         competitions=cs.update_competitions,
         seasons=cs.update_seasons,
         rounds=cs.update_rounds,
         teams=cs.update_teams,
         football_states=cs.update_states,
      )
      path = ['competitions', 'seasons', 'rounds', 'teams', 'football_states']

      if options['database']:
         for response in CrowdscoresResponse.objects.filter(path__in=path):
            data = json.loads(response.value)
            FUNCTIONS[response.path](data)
            print '%s was upload' % response.path
      else:
         cs.update_competitions()
         cs.update_seasons()
         cs.update_rounds()
         cs.update_teams()
         cs.update_states()

