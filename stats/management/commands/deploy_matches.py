from django.core.management.base import BaseCommand
from stats.services import Crowdscores
from stats.models import CrowdscoresResponse
from datetime import datetime, timedelta

import json


class Command(BaseCommand):

   def add_arguments(self, parser):
      parser.add_argument('-y', '--year', dest='year', type=int)
      parser.add_argument('-d', '--database', dest='database', action='store_true')

   def handle(self, *args, **options):
      year = options['year']
      is_db = options['database']

      if is_db:
         self.upload_from_db()
      else:
         self.upload_from_api(year)

   def upload_from_db(self):
      cs = Crowdscores()
      for response in CrowdscoresResponse.objects.filter(path='matches'):
         data = json.loads(response.value)
         cs.update_matches(params=None, data=data)


   def upload_from_api(self, year):
      _num_days = 7
      date_start = datetime(year, 1, 1)
      date_end = datetime(year+1, 1, 1) if year<datetime.now().year else datetime.now() + timedelta(days=30)

      cs = Crowdscores()
      while date_start<date_end:
         params={'from': datetime.strftime(date_start, '%Y-%m-%d')}
         cs.update_matches(params)
         _to = date_start + timedelta(days=_num_days)
         print 'Matches was uploaded for period %s - %s' % (datetime.strftime(date_start, '%d.%m.%Y'), datetime.strftime(_to, '%d.%m.%Y'))
         date_start = _to

