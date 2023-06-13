from django.urls import path,include
from django.contrib import admin
from Empmaster  import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #countrystate api
    path('CountryName', views.CountryName,name="CountryName"),
    path('StateName', views.StateName,name="StateName"),
    # aminurl api
    path('UserName', views.UserName,name="UserName"),
    path('getuserdetails', views.getuserdetails,name="getuserdetails"),
    path('getuseid/<int:id>', views.getuseid,name="getuseid"),
    path('updateUserName/<int:id>', views.updateUserName,name="updateUserName"),
    path('DeleteUser/<int:id>', views.DeleteUser,name="DeleteUser"),


    #role url
    
    path('RoleName', views.RoleName,name="RoleName"),
    path('updaterole/<int:id>', views.updaterole,name="updaterole"),
    path('getrole', views.getrole,name="getrole"),
    path('getroleid/<int:id>', views.getroleid,name="getroleid"),
    path('DeleteRole/<int:id>', views.DeleteRole,name="DeleteRole"),
    path('RoleData', views.RoleData,name="RoleData"),


#usermaster

    path('UserMaster', views.UserMaster,name="UserMaster"),
    path('getusermaster', views.getusermaster,name="getusermaster"),
    path('getmasterid/<int:id>', views.getmasterid,name="getmasterid"),
    path('updateUserMaster/<int:id>', views.updateUserMaster,name="updateUserMaster"),
    path('DeleteUsermaster/<int:id>', views.DeleteUsermaster,name="DeleteUsermaster"),


#getall countryand state data
    path('countryData', views.countryData,name="countryData"),
    path('getstate', views.getstate,name="getstate"),
    path('getcountry', views.getcountry,name="getcountry"),
    

#login
    path('mainlogin', views.mainlogin,name="mainlogin"),
    path('User_logout', views.User_logout,name="User_logout"),
    path('CheckPasswordView/<int:id>', views.CheckPasswordView,name="CheckPasswordView"),
    path('Logindetails', views.Logindetails,name="Logindetails"),
    path('passwordreset', views.passwordreset,name="passwordreset"),
    path('forgotpassword/<int:id>', views.forgotpassword,name="forgotpassword"),




# menuitemfront

    path('perm', views.perm,name="perm"),

#permissionadd
    
    path('Permissionadd', views.Permissionadd,name="Permissionadd"),
    path('permissiondetails/<int:Role_Id>', views.permissiondetails,name="permissiondetails"),
    path('getrolepermission/<int:id>', views.getrolepermission,name="getrolepermission"),
    path('updaterolepermission/<int:id>', views.updaterolepermission,name="updaterolepermission"),
    path('detailspermission/<int:Role_Id>', views.detailspermission,name="detailspermission"),
]
