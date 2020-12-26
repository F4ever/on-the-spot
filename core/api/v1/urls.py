from django.urls import path

from core.api.v1.views import stats_view, attack_view


urlpatterns = [
    path('stats/', stats_view, name='stats'),
    path('attack/', attack_view, name='attack'),
]
