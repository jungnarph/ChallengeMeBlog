from django.urls import path
from .views import RecipeListView, RecipeDetailView
from . import views

app_name = "blogapp"

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    # path('<int:year>/<int:month>/<int:day>/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='recipe_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]