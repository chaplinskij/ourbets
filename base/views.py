from datetime import datetime
from itertools import groupby

from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Max, Min
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth

from base.forms import HomePageForm
from stats.models import Match
from tote.models import FeaturedMatch


class HomeView(TemplateView):
   template_name = 'home.html'
   display_matches = 4
   # form_class = HomePageForm


   def get_context_data(self, **kwargs):
      ctx=super(HomeView, self).get_context_data(**kwargs)
      ctx['featured_matches'] = FeaturedMatch.objects.all()[:self.display_matches]
      return ctx


class DateMatchesView(TemplateView):
   template_name = '_matches.html'

   def get_context_data(self, **kwargs):
      ctx=super(DateMatchesView, self).get_context_data(**kwargs)
      rep_date = self.request.GET.get('date')
      rep_date = datetime.strptime(rep_date, "%Y%m%d").date() if rep_date else datetime.now().date()
      matches = Match.objects.filter(
         start__date=rep_date,
         competition__featured_competition__isnull=False
      ).order_by('competition__featured_competition__order', 'start')
      competitions=[]
      for k, group in groupby(matches, lambda x: x.competition):
         k.matches=list(group)
         competitions.append(k)

      ctx['competitions'] = competitions
      ctx['previous_date'] = Match.objects.filter(
         start__date__lt=rep_date,
         competition__featured_competition__isnull=False
      ).aggregate(rep_date=Max('start'))
      ctx['next_date'] = Match.objects.filter(
         start__date__gt=rep_date,
         competition__featured_competition__isnull=False
      ).aggregate(rep_date=Min('start'))
      ctx['current_date'] = rep_date
      return ctx



class LiveScoreView(TemplateView):
   template_name = 'live.html'

class SettingsView(TemplateView):
   template_name = 'profile.html'

   def get_context_data(self, **kwargs):
      ctx = super(SettingsView, self).get_context_data(**kwargs)
      user = self.request.user
      try:
         github_login = user.social_auth.get(provider='github')
      except UserSocialAuth.DoesNotExist:
         github_login = None

      try:
         twitter_login = user.social_auth.get(provider='twitter')
      except UserSocialAuth.DoesNotExist:
         twitter_login = None

      try:
         facebook_login = user.social_auth.get(provider='facebook')
      except UserSocialAuth.DoesNotExist:
         facebook_login = None

      try:
         vk_login = user.social_auth.get(provider='vk-oauth2')
      except UserSocialAuth.DoesNotExist:
         vk_login = None

      try:
         google_login = user.social_auth.get(provider='google-oauth2')
      except UserSocialAuth.DoesNotExist:
         google_login = None

      can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

      ctx['github_login'] = github_login
      ctx['twitter_login'] = twitter_login
      ctx['facebook_login'] = facebook_login
      ctx['vk_login'] = vk_login
      ctx['google_login'] = google_login
      ctx['can_disconnect'] = can_disconnect

      return ctx


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})


class ProfileView(TemplateView):
   template_name = 'profile.html'