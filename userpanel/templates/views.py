from django.shortcuts import render
from . import views
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from . import serializer
import requests
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import logout
# from django.views.decorators.csrf import csrf_exemp
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
# Create your views here.

# login logout url
addurl = 'http://127.0.0.1:8000/Empmaster/mainlogin'
logouturl = 'http://127.0.0.1:8000/Empmaster/User_logout'

#countrystate
@api_view(['POST'])
def CountryName(request):
    data={}
    data['cname'] = request.POST.get('cname')            

    serializer=Countryserializer(data=data)
    if serializer.is_valid():
        serializer.save() 
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "Status":"Success",
                "msg":"product found successfully"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "Status":"Failed",
                "msg":"unsucessful"
            }
        }
        return Response(Response_)

@api_view(['POST'])
def StateName(request):
    data={}
    data['sname'] = request.POST.get('sname')      
    data['country_id'] = request.POST.get('country_id')       

    serializer=Stateserializer(data=data)
    if serializer.is_valid():
        serializer.save() 
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "Status":"Success",
                "msg":"product found successfully"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "Status":"Failed",
                "msg":"unsucessful"
            }
        }
        return Response(Response_)


#emp master
@api_view(['POST'])
def UserName(request):
    data={}
    data['Firstname'] = request.POST.get('Firstname')  
    data['Lastname'] = request.POST.get('Lastname')
    data['mobile_no'] = request.POST.get('mobile_no')
    data['gender'] = request.POST.get('gender')
    data['email'] = request.POST.get('email')
    data['countryId'] = request.POST.get('countryId')
    data['stateId'] = request.POST.get('stateId')

    print("data",data)
    serializer=userserializer(data=data)

    if serializer.is_valid():
        serializer.save()
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "Status":"Success"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "Status":"Failed"

            }
        }
        return Response(Response_)

@api_view(['GET'])
def getuserdetails(request):
    getuserObject=useremp.objects.all()
    if getuserObject is not None:
        serializer = userserializer(getuserObject,many=True)
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "msg":"user found successfully",
                "Status":"Success"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No user found",
                "Status":"Failed"

            }
        }
        return Response(Response_)

@api_view(['GET'])
def getuseid(request,id):
    getuserObject = useremp.objects.filter(id=id).first()
    if getuserObject is not None:
        serializer = userserializer(getuserObject)
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "msg":"user found successfully",
                "Status":"Success"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No user found",
                "Status":"Failed"

            }
        }
        return Response(Response_)


@api_view(['POST'])
def updateUserName(request,id):

    UpdateUserObject = useremp.objects.filter(id=id).first()
    if UpdateUserObject is not None:
        data={}
        data['Firstname'] = request.POST.get('Firstname')  
        data['Lastname'] = request.POST.get('Lastname')
        data['mobile_no'] = request.POST.get('mobile_no')
        data['gender'] = request.POST.get('gender')
        data['email'] = request.POST.get('email')
        data['countryId'] = request.POST.get('countryId')
        data['stateId'] = request.POST.get('stateId')

        print("data",data)
        serializer=userserializer(UpdateUserObject,data=data)
        #validation
        validemail = useremp.objects.filter(isactive=True,email = request.POST.get('email')).exclude(id=id).first() 
        validno = useremp.objects.filter(isactive=True,mobile_no = request.POST.get('mobile_no')).exclude(id=id).first()
        validation = [useremp.email,validemail,validno]
        if UpdateUserObject.email == data ['email'] and validemail is not None:
            Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"User with this email Id already exists",
                "Status":"Failed"

            }
            }
            return Response(Response_)
        else:
            if serializer.is_valid():
                serializer.save()
                print("save",serializer.data)
                Response_ = {
                    "data":serializer.data,
                    "response":{
                        "n":1,
                        "msg":"User Data has been Updated successfully",
                        "Status":"Success"

                    }
                }
                return Response(Response_)
            else:
                print("err",serializer.errors)
                Response_ = {
                    "data":serializer.errors,
                    "response":{
                        "n":0,
                        "msg":"Error updating User",
                        "Status":"Success"

                    }
                }
                return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"User not Found",
                "Status":"Failed"

            }
        }
        return Response(Response_)


@api_view(['GET'])
def DeleteUser(request,id):
    userobject = useremp.objects.filter(id=id,isactive=True).first()
    if userobject is not None:
        data = {}
        data ['isactive'] = False 
        serializer = userserializer(userobject,data=data)
        if serializer.is_valid():
            serializer.save()
            Response_ = {
                "data":serializer.data,
                "response":{
                    "n":1,
                    "msg":"User has been deleted successfully",
                    "Status":"Success"

                }
            }
            return Response(Response_)
        else:
            Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "msg":"Error Deleting Data",
                "Status":"Failed"

                }
            }
            return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No data found",
                "Status":"Failed"

            }
        }
        return Response(Response_)



#role master
@api_view(['POST'])
def RoleName(request):
    data={}
    data['rolename'] = request.POST.get('rolename')            
    serializer=Roleserializer(data=data)
    if serializer.is_valid():
        serializer.save() 
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "Status":"Success",
                "msg":"added successfully"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "Status":"Failed",
                "msg":"unsucessful"
            }
        }
        return Response(Response_)


    
@api_view(['POST'])
def updaterole(request,id):
    UpdateUserObject = role.objects.filter(id=id).first()
    if UpdateUserObject is not None:
        data={}
        data['rolename'] = request.POST.get('rolename')  
        print("data",data)
        serializer = userserializer(UpdateUserObject,data=data)
        if serializer.is_valid():
            serializer.save() 
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "Status":"Success",
                "msg":"update successfully"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "Status":"Failed",
                "msg":"unsucessful"
            }
        }
        return Response(Response_)

@api_view(['GET'])
def getrole(request):
    getuserobject = role.objects.all()
    if getuserobject is not None:
        serializer = Roleserializer(getuserobject,many=True)
        Response_ = {
            "roledata":serializer.data,
            "response":{
                "n":1,
                "msg":"role found successfully",
                "Status":"Success"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No role found",
                "Status":"Failed"

            }
        }
        return Response(Response_)

@api_view(['GET'])
def getroleid (request,id):
    getuserobject = role.objects.filter(id=id).first()
    if getuserobject is not None:
        serializer = Roleserializer(getuserobject)
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "msg":"role found successfully",
                "Status":"Success"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No role found",
                "Status":"Failed"

            }
        }
        return Response(Response_)



#user master
@api_view(['POST'])
def UserMaster(request):
    data={}
    data['Name'] = request.POST.get('Name')  
    data['role_id'] = request.POST.get('role_id')
    data['email'] = request.POST.get('email')
    data['number'] = request.POST.get('number')
    data['password'] = make_password(request.POST.get('password'))

    print("data",data)
    serializer=Userserializer(data=data)

    if serializer.is_valid():
        serializer.save()
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "Status":"Success"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "Status":"Failed"

            }
        }
        return Response(Response_)


@api_view(['GET'])
def getusermaster(request):
    getuserObject=usermaster.objects.all()
    if getuserObject is not None:
        serializer = Userserializer(getuserObject,many=True)
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "msg":"user found successfully",
                "Status":"Success"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No user found",
                "Status":"Failed"

            }
        }
        return Response(Response_)
    
@api_view(['GET'])
def getmasterid(request,id):
    getuserObject = usermaster.objects.filter(id=id).first()
    if getuserObject is not None:
        serializer = userserializer(getuserObject)
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "msg":"user found successfully",
                "Status":"Success"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No user found",
                "Status":"Failed"

            }
        }
        return Response(Response_)


@api_view(['POST'])
def updateUserMaster(request,id):

    UpdateUsermaster = usermaster.objects.filter(id=id).first()
    if UpdateUsermaster is not None:
        data={}
        data['Name'] = request.POST.get('Name')  
        data['role_id'] = request.POST.get('role_id')
        data['email'] = request.POST.get('email')
        data['number'] = request.POST.get('number')
        data['password'] = make_password(request.POST.get('password'))

        print("data",data)
        serializer=Userserializer(UpdateUsermaster,data=data)
        #validation
        validemail = usermaster.objects.filter(isactive=True,email = request.POST.get('email')).exclude(id=id).first() 
        validno = usermaster.objects.filter(isactive=True,number = request.POST.get('number')).exclude(id=id).first()
        validation = [usermaster.email,validemail,validno]
        if UpdateUsermaster.email == data ['email'] and validemail is not None:
            Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"User with this email Id already exists",
                "Status":"Failed"

            }
            }
            return Response(Response_)
        else:
            if serializer.is_valid():
                serializer.save()
                print("save",serializer.data)
                Response_ = {
                    "data":serializer.data,
                    "response":{
                        "n":1,
                        "msg":"User Data has been Updated successfully",
                        "Status":"Success"

                    }
                }
                return Response(Response_)
            else:
                print("err",serializer.errors)
                Response_ = {
                    "data":serializer.errors,
                    "response":{
                        "n":0,
                        "msg":"Error updating User",
                        "Status":"Success"

                    }
                }
                return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"User not Found",
                "Status":"Failed"

            }
        }
        return Response(Response_)

@api_view(['GET'])
def DeleteUsermaster(request,id):
    userobject = usermaster.objects.filter(id=id,isactive=True).first()
    if userobject is not None:
        data = {}
        data ['isactive'] = False 
        serializer = Userserializer(userobject,data=data)
        if serializer.is_valid():
            serializer.save()
            Response_ = {
                "data":serializer.data,
                "response":{
                    "n":1,
                    "msg":"User has been deleted successfully",
                    "Status":"Success"

                }
            }
            return Response(Response_)
        else:
            Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "msg":"Error Deleting Data",
                "Status":"Failed"

                }
            }
            return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No data found",
                "Status":"Failed"

            }
        }
        return Response(Response_)


#for country and state list
@api_view(['GET'])
def countryData(request):
        item=countrymodel.objects.all()
        country_serializer=Countryserializer(item,many=True)
        stateitem=statemodel.objects.all()
        state_serializer=Stateserializer(stateitem,many=True)
        Response_ = {
            "countryList":country_serializer.data,
            "stateList":state_serializer.data,
            "response":{
                "n":1,
                "msg":"Data found succefully",
                "Status":"Success"
            }
        }
        return Response(Response_)

@api_view(['POST'])
def getstate(request):
        getdata=request.POST.get('countryId')
        print(getdata)
        item=statemodel.objects.filter(country_id=getdata) 
        serializer=Stateserializer(item,many=True)
        print(serializer.data)
        return Response(serializer.data)

def getcountry(request):
        item=countrymodel.objects.all()
        country_serializer=Countryserializer(item,many=True)
        stateitem=statemodel.objects.all()
        state_serializer=Stateserializer(stateitem,many=True)
        # print(serializer.data)
        return render(request,'drop.html',{'states':state_serializer.data,'country':country_serializer.data})

#check password
@api_view(['POST'])
def CheckPasswordView(request,id):
        object= usermaster.objects.filter(id=id).first()
        print("object",object.password)
        currentpassword = request.POST.get('currentpassword')
        print("currentpassword",currentpassword)
        checkpass = check_password(currentpassword,object.password)
        print("checkpass",checkpass)
        if checkpass == True:
            Response_ = {
                "data":{},
                "response":{
                    "n":1,
                    "msg":"password match",
                    "Status":"Success"

                }
            }
            return Response(Response_)
        else:
            Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"password dose not match",
                "Status":"Failed"
            }
        }
        return Response(Response_)

#login
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(["POST"])
def mainlogin(request):
    email = request.POST.get("email")
    print("emaillllll",email)
    password = request.POST.get("password")
    empass = usermaster.objects.filter(email=email).first()
    print("empasssssss",empass)

    if email is not None:    
        check = check_password(password,empass.password)    
        if check == True:
            token, _ = Token.objects.get_or_create(user=empass)
            # return Response({'token': token.key})            
            return Response({
                            "token":token.key,
                            "Status":"Success"
                        })

        else:
            return Response({
                            "Status":"Failed"
                        })

@api_view(["POST"])
def User_logout(request):
    email = request.POST.get("email")
    userId = usermaster.objects.filter(isactive=True,email=email).first()
    tokenObject = Token.objects.filter(user=userId.id).first()
    print("aksuygdfauy",userId)
    # logout(request)
    print("logout",tokenObject)
    if tokenObject is not None:
        tokendelete = tokenObject.delete()
        print("tokendelete",tokendelete)
        return Response('User Logged out successfully')
    return Response('User Logged out Failed')



#login logout front

def loginAdd(request):
        if request.method == "POST":
            # token = request.session.get('')
            data={}
            data['email'] = request.POST.get('email')
            data['password'] = request.POST.get('password')
            print("data",data)

            responseUrl = requests.post(addurl,data=data)
            result = responseUrl.json()
            print("result",result)
            request.session['email'] = request.POST.get('email')
            request.session['token'] = result['token']

            print("asfsdbdgf",request.session['token'])
            if result['Status'] == 'Success':
                return render (request,'admin_theme/index.html')

            # else:
            #     return HttpResponse("unsuccsessful")
        return render (request,'admin_theme/login.html')


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
    
    return render (request,'admin/login.html')