from django.shortcuts import render,redirect
from . import views
from rest_framework.decorators import api_view
from .models import *
import requests
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.contrib import messages



# Create your views here.

#master
addmasterurl = 'http://127.0.0.1:8000/Empmaster/UserMaster'
getmasterurl = 'http://127.0.0.1:8000/Empmaster/getusermaster'
getmasteridurl = 'http://127.0.0.1:8000/Empmaster/getmasterid/'
updatemasterurl = 'http://127.0.0.1:8000/Empmaster/updateUserMaster/'
deletemasterurl = 'http://127.0.0.1:8000/Empmaster/DeleteUsermaster/'


# login front
addurl = 'http://127.0.0.1:8000/Empmaster/mainlogin'
logouturl = 'http://127.0.0.1:8000/Empmaster/User_logout'
resetpasurl= 'http://127.0.0.1:8000/Empmaster/passwordreset'
forgoturl = 'http://127.0.0.1:8000/Empmaster/forgotpassword/'


 #rolemasterurl
addroleurl = 'http://127.0.0.1:8000/Empmaster/RoleName'
updateroleurl = 'http://127.0.0.1:8000/Empmaster/updaterole/'
getrolesurl = 'http://127.0.0.1:8000/Empmaster/getrole'
deleteroleurl = 'http://127.0.0.1:8000/Empmaster/DeleteRole/'
roledataurl = 'http://127.0.0.1:8000/Empmaster/RoleData'

#permission
permm = 'http://127.0.0.1:8000/Empmaster/perm'

#give permissions
Permissionaddurl = 'http://127.0.0.1:8000/Empmaster/Permissionadd'
updaterolepermissionurl = 'http://127.0.0.1:8000/Empmaster/updaterolepermission'



def UsermasterAdd(request):
        if request.method == "POST":
                print("POST")
                data={}
                data['Name'] = request.POST.get('Name')  
                data['role_id'] = request.POST.get('role_id')
                data['email'] = request.POST.get('email')
                data['number'] = request.POST.get('number')
                data['password'] = request.POST.get('password')
                print("data dfx",data)
                responseUrl = requests.post(addmasterurl,data=data)
                result = responseUrl.json()
                print ("result",result)
                # return redirect('Empmaster:loginAdd')
                if result['response']['n'] == 1:
                        messages.success(request, result['response']['msg'])
                        return redirect('usermasterfront:getUsermaster')
                else:
                        messages.error(request, result['response']['msg'])
                        return redirect('usermasterfront:getUsermaster') 

        # print("ELSE")  
        roleresponse = requests.get(getrolesurl)
        roleData = roleresponse.json()
        print ("roleData sdfgsdgs",roleData)
        return render(request,'admin_theme/usermaster.html',{'GetDatarole':roleData['GetDatarole']})

def getUsermaster(request):
        response = requests.get(getmasterurl)
        geodata = response.json()
        return render(request,'masterfront/viewusermaster.html',{'GetData':geodata['data']})

def getusermasterid(request):
        getUser = getmasteridurl + str(id)
        response = requests.get(getUser)
        geodata = response.json()
        Roleresponse = requests.get(roledataurl)
        roledata = Roleresponse.json()
    

def updateUsermaster(request,id):
        if request.method == "GET":
                getUser = getmasteridurl + str(id)
                response = requests.get(getUser)
                geodata = response.json()
                Roleresponse = requests.get(roledataurl)
                roledata = Roleresponse.json()
                print("roledataaaaA",roledata)
                return render(request,'masterfront/updateusermaster.html',{'GetDatarole':geodata['data'],'Rolelist':roledata['Rolelist']})
                
        else:
                data={}
                data['Name'] = request.POST.get('Name')  
                data['role_id'] = request.POST.get('role_id')
                data['email'] = request.POST.get('email')
                data['number'] = request.POST.get('number')
                data['password'] = make_password(request.POST.get('password'))
                print("daata",data)
                updateUser = updatemasterurl + str(id)
                responseUrl = requests.post(updateUser,data=data)
                result = responseUrl.json()
                if result['response']['n'] == 1:
                        # messages.success(request, result['response']['msg'])
                        return redirect('usermasterfront:getUsermaster')
                else:
                        # messages.error(request, result['response']['msg'])
                        return redirect('usermasterfront:getUsermaster')


def deletemasterdata(request,id):
        deletemasdata=deletemasterurl + str(id)
        delete_UserUrl = requests.get(deletemasdata)
        result = delete_UserUrl.json()
        print ("result",result)
        # return redirect('deleted successfully')
        if result['response']['n'] == 1:
                # messages.success(request, result['response']['msg'])
                return redirect('usermasterfront:getUsermaster')
        else:
                # messages.error(request, result['response']['msg'])
                return redirect('usermasterfront:getUsermaster')



# log in front
def loginAdd(request):
    if request.method == "POST":
        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password')
        }
        print("sushant", data)

        responseUrl = requests.post(addurl, data=data)
        result = responseUrl.json()
        print("result", result)

        if result['Status'] == 'Success':
            request.session['email'] = request.POST.get('email')
            request.session['token'] = result['token']
            request.session['name'] = result.get('name')  # Set the name in the session

            nammmee = request.session.get('name')
            print("asfsdbdgf", request.session['token'])

            return render(request, 'admin_theme/index.html', {'data': result, "nammmee": nammmee})
        else:
            return HttpResponse("Login unsuccessful. Enter Wrong Email And Password")
    
    return render(request, 'admin_theme/login.html')

def userlogout(request):
    data = {}
    data ['email'] = request.session.get('email')
    # emailobject = request.session.get('email' )
    token = request.session.get('token')
    print ("token",token)
    t = 'Token {}'.format(token)
    headers = {'Authorization': t}
    responseUrl = requests.post(logouturl,headers=headers,data=data)
    result = responseUrl.json()
    print ("result",result)
    
    return redirect('usermasterfront:loginAdd')

def userpasswordchange(request):
        if request.method == "POST":
                data={}
                data['email'] = request.POST.get('email')
                data['newpassword'] = request.POST.get('newpassword')  
                data['confirmpassword'] = request.POST.get('confirmpassword')
                data['password'] = request.POST.get('password')
                responseUrl = requests.post(resetpasurl,data=data)
                result = responseUrl.json()
                print ("result",result)
                if result['response']['n'] == 1:
                    messages.success(request, result['response']['msg'])
                    return redirect('usermasterfront:getUsermaster')
                else:
                        messages.error(request, result['response']['msg'])
                        return redirect('usermasterfront:getUsermaster') 

def userforgotpassword(request,id):
        if request.method == "POST":
                
                data={}
                data['newpassword'] = request.POST.get('newpassword')  
                data['confirmpassword'] = request.POST.get('confirmpassword')
                data['password'] = request.POST.get('password')
                print("forgotdata",data)
                responseUrl = requests.post(forgoturl,data=data)
                result = responseUrl.json()
                print ("result",result)
    

#permission rolefront

def perroleAdd(request):
        if request.method == "POST":
                print("POST")
                data={}
                data['role_id'] = request.POST.get('role_id')
                print("dtaasfasf",data)
                
        # print("ELSE")  
        roleresponse = requests.get(getrolesurl)
        roleData = roleresponse.json()
        print ("roleData sdfgsdgs",roleData)

        return render(request,'rolename/empitem.html',{'GetDatarole':roleData['GetDatarole']})


def getperrole(request):
        response = requests.get(getrolesurl)
        geodata = response.json()
        return render(request,'masterfront/viewusermaster.html',{'GetDatarole':geodata['GetDatarole']})


# def permsi(request):
#         if request.method == "POST":
#                 data={}
#                 data['Role_Id'] = request.POST.get('Role_Id')      
#                 data['checkbox_id'] = request.POST.getlist('checkbox_id')
#                 print ("datasssssdafadfadfgadfaef",data)   
#         per_request=requests.get(permm)
#         per_response = per_request.json()
#         # print ("permission",per_response)
#         response = requests.get(getroles)
#         geodata = response.json()
#         # print ("roleDataoeitrgjioertjg0 ",geodata)
#         return render(request,'rolename/empitem.html',{'GetDatarole':geodata['GetDatarole'],'GetData':per_response['GetData']})

#give permissions

def permissionfront(request):
        if request.method == "POST":
                data={}
                data['Role_Id'] = request.POST.get('Role_Id')      
                data['checkbox_id'] = request.POST.getlist('checkbox_id')   
                print ("dsa",data)
                responseUrl = requests.post(Permissionaddurl,data=data)
                result = responseUrl.json()
                print("resultawfaf",result)
                if result['response']['n'] == 1:
                    # messages.success(request, result['response']['msg'])
                        return redirect('userpanelfront:getrolelist')
                else:
                # messages.error(request, result['response']['msg'])
                        return redirect('userpanelfront:getrolelist')
        per_request=requests.get(permm)
        per_response = per_request.json()
        print ("permission",per_response)
        roleresponse = requests.get(getrolesurl)
        roleData = roleresponse.json()
        # print("roledata",roleData)
        
        return render(request,'rolename/empitem.html',{'GetDatarole':roleData['GetDatarole'],'GetData':per_response['GetData']})





# def updateUser(request,id):
#         if request.method == "GET":
#                 getUser = getmasteridurl + str(id)
#                 response = requests.get(getUser)
#                 geodata = response.json()
#                 return render(request,'adminuserpanel/update.html',{'data':roleData['data']})
#         else:
#                 data={}
#                 data['Role_Id'] = request.POST.get('Role_Id')      
#                 data['checkbox_id'] = request.POST.getlist('checkbox_id') 
#                 print("daata",data)
#                 updateUser = updaterolepermissionurl + str(id)
#                 responseUrl = requests.post(updateUser,data=data)
#                 result = responseUrl.json()
#                 print("result",result)
                # if result['response']['n'] == 1:
                #         # messages.success(request, result['response']['msg'])
                #         return redirect('usermasterfront:getUsermaster')
                # else:
                #         # messages.error(request, result['response']['msg'])
                #         return redirect('usermasterfront:getUsermaster')