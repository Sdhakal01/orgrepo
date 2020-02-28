from django.urls import path
from . import views

urlpatterns = [
    path('main', views.index),
    path('create',views.create),
    path('login',views.login),
    path('groups',views.allgroups),
    path('logout',views.logout),
    path('orgcreate',views.orgcreate),
    path('groups/<groupId>',views.joingroup),
    path('add/<groupId>',views.add),
    path('leave/<groupId>',views.leave),
    path('delete/<groupId>',views.delete),
    path('dashboard',views.dashboard)


]
