from django.shortcuts import render
from Empmaster import views
from Empmaster import *
import requests
from django.shortcuts import redirect

# Create your views here.
#countryurl
addcountryurl = 'http://127.0.0.1:8000/Empmaster/CountryName'
addstateuyrl = 'http://127.0.0.1:8000/Empmaster/StateName'

#empmasterurl
addempurl = 'http://127.0.0.1:8000/Empmaster/UserName'
getempurl = 'http://127.0.0.1:8000/Empmaster/getuserdetails'
getempidurl = 'http://127.0.0.1:8000/Empmaster/getuseid/'
updateempurl ='http://127.0.0.1:8000/Empmaster/updateUserName/'
deleteempurl ='http://127.0.0.1:8000/Empmaster/DeleteUser/'

#rolemasterurl

addroleurl = 'http://127.0.0.1:8000/Empmaster/RoleName'
updateroleurl = 'http://127.0.0.1:8000/Empmaster/updaterole/'
getrole = 'http://127.0.0.1:8000/Empmaster/getrole'
getroleidurl = 'http://127.0.0.1:8000/Empmaster/getroleid/'
deleteRoleurl ='http://127.0.0.1:8000/Empmaster/DeleteRole/'

#country
countryUrl = 'http://127.0.0.1:8000/Empmaster/countryData'




def EmpAdd(request):
        if request.method == "POST":
                data={}
                data['Firstname'] = request.POST.get('Firstname')  
                data['Lastname'] = request.POST.get('Lastname')
                data['mobile_no'] = request.POST.get('mobile_no')
                data['gender'] = request.POST.get('gender')
                data['email'] = request.POST.get('email')
                data['countryId'] = request.POST.get('countryId')
                data['stateId'] = request.POST.get('stateId')
                print("daatassssssssssssssssss",data)
                responseUrl = requests.post(addempurl,data=data)
                result = responseUrl.json()
                print ("result",result)
                # return redirect('userpanelfront:getUseremp')
                # return redirect('Empmaster:loginAdd')
                if result['response']['n'] == 1:
                        # messages.success(request, result['response']['msg'])
                        return redirect('userpanelfront:getUseremp')
                else:
                        # messages.error(request, result['response']['msg'])
                        return redirect('userpanelfront:getUseremp') 
        else:
            
                countryresponse = requests.get(countryUrl)
                countryData = countryresponse.json()

                return render(request,'admin_theme/register.html',{'countryList':countryData['countryList'],'stateList':countryData['stateList']})



def getUseremp(request):
        response = requests.get(getempurl)
        geodata = response.json()
        return render(request,'adminuserpanel/list.html',{'GetData':geodata['data']})


def updateUser(request,id):
        if request.method == "GET":
                getUser = getempidurl + str(id)
                response = requests.get(getUser)
                geodata = response.json()
                countryresponse = requests.get(countryUrl)
                countryData = countryresponse.json()
                return render(request,'adminuserpanel/update.html',{'GetData':geodata['data'],'countryList':countryData['countryList'],'stateList':countryData['stateList']})
        else:
                data={}
                data['Firstname'] = request.POST.get('Firstname')  
                data['Lastname'] = request.POST.get('Lastname')
                data['mobile_no'] = request.POST.get('mobile_no')
                data['gender'] = request.POST.get('gender')
                data['email'] = request.POST.get('email')
                data['countryId'] = request.POST.get('countryId')
                data['stateId'] = request.POST.get('stateId')
                print("daata",data)
                updateUser = updateempurl + str(id)
                responseUrl = requests.post(updateUser,data=data)
                result = responseUrl.json()
                if result['response']['n'] == 1:
                        # messages.success(request, result['response']['msg'])
                        return redirect('userpanelfront:getUseremp')
                else:
                        # messages.error(request, result['response']['msg'])
                        return redirect('userpanelfront:getUseremp')

def deletedata(request,id):
        deleteSubdata=deleteempurl + str(id)
        delete_UserUrl = requests.get(deleteSubdata)
        result = delete_UserUrl.json()
        print ("result",result)
        # return redirect('deleted successfully')
        if result['response']['n'] == 1:
                # messages.success(request, result['response']['msg'])
                return redirect('userpanelfront:getUseremp')
        else:
                # messages.error(request, result['response']['msg'])
                return redirect('userpanelfront:getUseremp')


def roleadd(request):
    
        if request.method == "POST":
                data={}
                data['rolename'] = request.POST.get('rolename')
                print ("dsa",data)
                responseUrl = requests.post(addroleurl,data=data)
                result = responseUrl.json()
                print ("result",result)
                return redirect('userpanelfront:getrolelist')
                # return redirect('Empmaster:loginAdd')
                # if result['response']['n'] == 1:
                        # messages.success(request, result['response']['msg'])
                #         return redirect('userpanelfront:getUseremp')
                # else:
                        # messages.error(request, result['response']['msg'])
                #         return redirect('userpanelfront:getUseremp') 
              
        return render(request,'rolename/add-rolename.html')
                    

def getrolelist(request):
        response = requests.get(getrole)
        geodata = response.json()
        print("geodataaaaa",geodata)
        return render(request,'rolename/list-role.html',{'GetDatarole':geodata['GetDatarole']})

        

def updaterolelist(request,id):
        if request.method == "GET":
                getUser = getroleidurl + str(id)
                response = requests.get(getUser)
                print("response",response)
                geodata = response.json()
                print("geooodattta",geodata)
                return render(request,'rolename/update-role.html',{'GetDatarole':geodata['roledata']})
        else:
                data={}
                data['rolename'] = request.POST.get('rolename')
                print("daata",data)
                updateUser = updateroleurl + str(id)
                responseUrl = requests.post(updateUser,data=data)
                result = responseUrl.json()
                if result['response']['n'] == 1:
                        # messages.success(request, result['response']['msg'])
                        return redirect('userpanelfront:getrolelist')
                else:
                        # messages.error(request, result['response']['msg'])
                        return redirect('userpanelfront:getrolelist')

def deleteRoledata(request,id):
        deleteRoledata=deleteRoleurl + str(id)
        delete_UserUrl = requests.get(deleteRoledata)
        result = delete_UserUrl.json()
        print ("result",result)
        # return redirect('deleted successfully')
        if result['response']['n'] == 1:
                # messages.success(request, result['response']['msg'])
                return redirect('userpanelfront:getrolelist')
        else:
                # messages.error(request, result['response']['msg'])
                return redirect('userpanelfront:getrolelist')


# def EmpAdd(request):
#         if request.method == "POST":
#                 data={}
#                 data['Firstname'] = request.POST.get('Firstname')  
#                 data['Lastname'] = request.POST.get('Lastname')
#                 print ("dsa",data)
#                 responseUrl = requests.post(addempurl,data=data)
#                 result = responseUrl.json()
#                 print ("result",result)
#                 return redirect('Empmaster:loginAdd')
#                 if result['response']['n'] == 1:
#                         # messages.success(request, result['response']['msg'])
#                         return redirect('userpanelfront:getUseremp')
#                 else:
#                         # messages.error(request, result['response']['msg'])
#                         return redirect('userpanelfront:getUseremp') 
#         else:
            
#                 countryresponse = requests.get(countryUrl)
#                 countryData = countryresponse.json()

#                 return render(request,'admin_theme/register.html',{'countryList':countryData['countryList'],'stateList':countryData['stateList']})