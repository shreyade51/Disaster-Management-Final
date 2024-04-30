from django.urls import path
from . import views

urlpatterns = [

    path('register/',views.register, name='volunteerregister'),
   
    path('',views.volunteerdashboard,name='volunteerdashboard'),

    path('api/map/',views.sendmapdata,name='apimap'),

    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('admindashboard/volunteers',views.adminvolunteers,name='adminvolunteers'),
    path('admindashboard/newdisaster/',views.newDisaster,name='adminnewdisaster'),
    path('admindashboard/tasks/',views.disastertasks,name='admintasks'),
    path('admindashboard/newtask/',views.addtask,name='adminnewtask'),
    path('admindashboard/edittask/<int:id>/',views.edittask,name='adminedittask'),
    path('admindashboard/editdisaster/<int:id>/',views.editdisaster,name='admineditdisaster'),
    path('admindashboard/addlocation/',views.addlocation,name='adminaddlocation'),
    path('admindashboard/locations/',views.location,name='adminlocation'),
    path('admindashboard/contributors/',views.admincontributors,name='admincontributors'),
    path('admindashboard/resources/',views.adminresources,name='adminresources'),
    path('admindashboard/assign_resources/',views.assignresource,name='assign_resources'),
    path('admindashboard/assigned_resources/',views.resoucealloc,name='assigned_resources'),
    path('admindashboard/map/',views.heatmap,name='adminmap'),


    path('contributor/',views.contributor,name='contributor'),
    path('contributor/resource/',views.getresource,name='contributor_resource'),

    
]