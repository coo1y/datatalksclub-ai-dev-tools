from django.urls import path

from . import views

app_name = 'chores'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('plan/', views.plan_view, name='plan'),
    path('plan/start/', views.start_week_view, name='start_week'),
    path('plan/chores/add/', views.add_chore_view, name='add_chore'),
    path('plan/chores/<int:chore_id>/edit/', views.edit_chore_view, name='edit_chore'),
    path('plan/chores/<int:chore_id>/delete/', views.delete_chore_view, name='delete_chore'),
    path('chores/<int:chore_id>/toggle/', views.toggle_chore_view, name='toggle_chore'),
    path('history/', views.history_view, name='history'),
    path('history/<int:week_id>/', views.week_detail_view, name='week_detail'),
]
