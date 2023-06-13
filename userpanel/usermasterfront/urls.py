from django.urls import path,include
from django.contrib import admin
from usermasterfront  import views

urlpatterns = [
    path('UsermasterAdd', views.UsermasterAdd,name="UsermasterAdd"),
    path('getUsermaster', views.getUsermaster,name="getUsermaster"),
    path('updateUsermaster/<int:id>', views.updateUsermaster,name="updateUser"),
    path('deletemasterdata/<int:id>', views.deletemasterdata,name="deletemasterdata"),

    
    # login front
    path('loginAdd', views.loginAdd,name="loginAdd"),
    path('userlogout', views.userlogout,name="userlogout"),

    #permission role
    path('perroleAdd', views.perroleAdd,name="perroleAdd"),
    path('getperrole', views.getperrole,name="getperrole"),

    #permission all data get
    # path('permsi', views.permsi,name="permsi"),

    #give permissi9ons
    path('permissionfront', views.permissionfront,name="permissionfront"),
]