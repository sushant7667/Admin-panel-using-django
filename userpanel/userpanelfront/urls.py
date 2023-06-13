from django.urls import path,include
from django.contrib import admin
from userpanelfront  import views

urlpatterns = [
    path("EmpAdd", views.EmpAdd, name="EmpAdd"),
    path("getUseremp", views.getUseremp, name="getUseremp"), 
    path("updateUser/<int:id>", views.updateUser, name="updateUser"),
    path("deletedata/<int:id>", views.deletedata, name="deletedata"),  
    
    
    # role front

    
    path("roleadd", views.roleadd, name="roleadd"),
    path("getrolelist", views.getrolelist, name="getrolelist"),
    path("updaterolelist/<int:id>", views.updaterolelist, name="updaterolelist"),
    path("deleteRoledata/<int:id>", views.deleteRoledata, name="deleteRoledata"),
]