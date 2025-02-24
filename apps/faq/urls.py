from django.urls import path
from .views import FAQListView

app_name = 'faq'


urlpatterns = [
    path('<int:id>/', FAQListView.as_view(), name='faq_detail'),
]
