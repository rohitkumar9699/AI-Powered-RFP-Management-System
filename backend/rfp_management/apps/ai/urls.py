"""AI app - urls"""
from django.urls import path
from .views import AIViewSet

ai_view = AIViewSet.as_view({
    'post': 'parse_natural_language'
})

urlpatterns = [
    path('parse-natural-language/', AIViewSet.as_view({'post': 'parse_natural_language'})),
    path('parse-proposal/', AIViewSet.as_view({'post': 'parse_proposal'})),
    path('evaluate-proposals/', AIViewSet.as_view({'post': 'evaluate_proposals'})),
]
