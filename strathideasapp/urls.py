from django.urls import path
from .views import profile, IdeaListView, IdeaDetailView, IdeaCreateView, \
    IdeaUpdateView, IdeaDeleteView, IdeaLikeToggle, HomeView

app_name = 'strathideasapp'
urlpatterns = [
	path('', HomeView.as_view(), name='home'),
    path('idea', IdeaListView.as_view(), name='idea_list'),
    path('idea/<int:pk>/', IdeaDetailView.as_view(), name='idea_detail'),
    path('idea/<int:pk>/like', IdeaLikeToggle.as_view(), name='idea_like'),
    path('idea/new', IdeaCreateView.as_view(template_name='strathideasapp/ideas_form.html', success_url='/'), name='idea_create'),
    path('idea/<int:pk>/update/', IdeaUpdateView.as_view(success_url='/'), name='idea_update'),
    path('idea/<int:pk>/delete/', IdeaDeleteView.as_view(success_url='/'), name='idea_delete'),
    path('profile/', profile, name='profile'),  # to be removed after login and sign up is set up.

]