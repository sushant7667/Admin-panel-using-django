from django.shortcuts import render,redirect
from django.http import HttpResponse
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
from django.contrib.auth.models import User
# Create your views here.


#role
getroles = 'http://127.0.0.1:8000/Empmaster/getrole'

#permission
permm = 'http://127.0.0.1:8000/Empmaster/perm'

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
    getuserObject=useremp.objects.filter(isactive=True)
    if getuserObject is not None:
        serializer = userserializer(getuserObject,many=True)
        for i in serializer.data:
            print("i",i['countryId'] ,"j",i['stateId'])
            if i['countryId'] and i['stateId'] is not None:
                countryName = countrymodel.objects.filter(id=i['countryId']).first()
                statename = statemodel.objects.filter(id=i['stateId']).first()
                i['countryId'] = countryName.cname
                i['stateId'] = statename.sname
        # for j in serializer.data:
        #     print("iiiii",j['stateId'])
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
    getuserObject = useremp.objects.filter(id=id,isactive=True).first()
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

    UpdateUserObject = useremp.objects.filter(isactive=True,id=id).first()
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
    UpdateUserObject = role.objects.filter(isactive=True,id=id).first()
    if UpdateUserObject is not None:
        data={}
        data['rolename'] = request.POST.get('rolename')  
        print("data",data)
        serializer = Roleserializer(UpdateUserObject,data=data)
        if serializer.is_valid():
            serializer.save() 
            Response_ = {
                "Roledata":serializer.data,
                "response":{
                    "n":1,
                    "Status":"Success",
                    "msg":"update successfully"

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
def getrole(request):
    getuserobject = role.objects.filter(isactive=True)
    if getuserobject is not None:
        serializer = Roleserializer(getuserobject,many=True)
        Response_ = {
            "GetDatarole":serializer.data,
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
    getuserobject = role.objects.filter(isactive=True,id=id).first()
    if getuserobject is not None:
        serializer = Roleserializer(getuserobject)
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
def DeleteRole(request,id):
    userobject = role.objects.filter(id=id,isactive=True).first()
    if userobject is not None:
        data = {}
        data ['isactive'] = False 
        serializer = Roleserializer(userobject,data=data)
        if serializer.is_valid():
            serializer.save()
            Response_ = {
                "data":serializer.data,
                "response":{
                    "n":1,
                    "msg":"Role deleted successfully",
                    "Status":"Success"

                }
            }
            return Response(Response_)
        else:
            Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "msg":"Error Deleting Role",
                "Status":"Failed"

                }
            }
            return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No Role found",
                "Status":"Failed"

            }
        }
        return Response(Response_)

@api_view(['GET'])
def RoleData(request):
        item=role.objects.all()
        role_serializer=Roleserializer(item,many=True)
        Response_ = {
            "Rolelist":role_serializer.data,
            "response":{
                "n":1,
                "msg":"Data found succefully",
                "Status":"Success"
            }
        }
        return Response(Response_)

# @api_view(['GET'])
# def roleData(request):
#         item=usermaster.objects.all()
#         role_serializer=Roleserializer(item,many=True)
#         Response_ = {
#             "RoleList":role_serializer.data,
#             "response":{
#                 "n":1,
#                 "msg":"Data found succefully",
#                 "Status":"Success"
#             }
#         }
#         return Response(Response_)



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
#    emailvalid=testcrud.objects.filter(isactive=True,email=request.POST.get('email')).first()
    emailval=usermaster.objects.filter(isactive=True,email=request.POST.get('email')).first()
    numberval=usermaster.objects.filter(isactive=True,number=request.POST.get('number')).first()
    print("emailval",emailval)
    print("numberval",numberval)
    if emailval is not None:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"User with this Email id already exists",
                "Status":"Failed"

            }
        }
        return Response(Response_)
    if numberval is not None:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"User with this number already exists",
                "Status":"Failed"

            }
        }
        return Response(Response_)

    serializer=Userserializer(data=data)

    if serializer.is_valid():
        serializer.save()
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "Status":"Success",
                "msg":"user added successfully"

            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":serializer.errors,
            "response":{
                "n":0,
                "Status":"Failed",
                "msg":"Failed to add user"
            }
        }
        return Response(Response_)


@api_view(['GET'])
def getusermaster(request):
    getuserObject=usermaster.objects.filter(isactive=True)
    if getuserObject is not None:
        serializer = Userserializer(getuserObject,many=True)
        for i in serializer.data:
                print("i",i['role_id'])
                if i['role_id'] is not None:
                    RoleName = role.objects.filter(id=i['role_id']).first()
                    i['role_id'] = RoleName.rolename

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
    getuserObject = usermaster.objects.filter(id=id,isactive=True).first()
    if getuserObject is not None:
        serializer = Userserializer(getuserObject)
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

    UpdateUsermaster = usermaster.objects.filter(id=id,isactive=True).first()
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
        print("validno",validno)
        validation = [usermaster.email,validemail,validno]
        print("validation",validemail)
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
        if validno is not None:
            Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"User with this Number already exists",
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
# @csrf_exempt
# @permission_classes((AllowAny,))
# @api_view(["POST"])
# def mainlogin(request):
#     email = request.POST.get("email")
#     print("emaillllll",email)
#     password = request.POST.get("password")
#     print("password",password)
#     empass = usermaster.objects.filter(email=email).first()
#     names=empass.Name
#     print("names",names)  
#     # print("empasssssss",empass.password)

#     if email is not None:   
#         check = check_password(password,empass.password)  
#         print("check",check)  
#         if check == True:
#             token, _ = Token.objects.get_or_create(user=empass)
#             # return Response({'token': token.key})            
#             return Response({
#                             "token":token.key,
#                             "Status":"Success",
#                             "name":names
#                         })

#         else:
#             return Response({
#                             "Status":"Failed",
#                             "msg":"User Login Failed"
#                         })


@csrf_exempt
@permission_classes((AllowAny,))
@api_view(["POST"])
def mainlogin(request):
    email = request.POST.get("email")
    print("emaillllll", email)
    password = request.POST.get("password")
    print("password", password)
    empass = usermaster.objects.filter(email=email).first()

    if empass is None:
        # Return a response indicating that the email is not found
        return Response({
            "Status": "Failed",
            "msg": "Email not found"
        })

    check = check_password(password, empass.password)
    print("check", check)
    if check:
        token, _ = Token.objects.get_or_create(user=empass)
        return Response({
            "token": token.key,
            "Status": "Success",
            "name":empass.Name,
        })
    else:
        return Response({
            "Status": "Failed",
            "msg": "User Login Failed check Email and Password"
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

@api_view(['GET'])
def Logindetails(request):
    getlogin=usermaster.objects.all()
    if getlogin is not None:    
        serializer = Userserializer(getlogin,many=True)
        Response_ = {
            "data":serializer.data,
            "response":{
                "n":1,
                "msg":"product found successfully",
                "Status":"Success"
            }
        }
        return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"No Product found",
                "Status":"Failed"
        }

        }
        return Response(Response_)

@api_view(['POST'])
def passwordreset(request):
    email = request.POST.get('email')
    print(email)
    currentpassword = request.POST.get('currentpassword')
    print("current_password",currentpassword)
    newpassword = request.POST.get('newpassword')
    print("new_password",newpassword)
    confirmpassword = request.POST.get('confirmpassword')
    print("confirm_password",confirmpassword)
    userObject = usermaster.objects.filter(isactive=True,email=email).first()
    print("objmail",userObject)
    
    # password=make_password(request.POST.get('password'))
    # serializer = CustomUserCreationserializer(password)
    # data= adminuser.objects.filter(id=id).first()
    checkpass = check_password(currentpassword,userObject.password)
    print("curpass",currentpassword)
    print("checkpass",checkpass)
    
    if checkpass == True:
        if newpassword == confirmpassword:
            data = {}
            data['password'] = make_password(confirmpassword)
            serializer = Userserializer(userObject,data=data,partial=True)

            if serializer.is_valid():
                serializer.save()
                print("save",serializer.data)
                Response_ = {
                    "data":serializer.data,
                    "response":{
                        "n":1,
                        "msg":"Updated successfully",
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
                        "msg":"Error updating",
                        "Status":"Success"

                    }
                }
                return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"New password and confirm password does not matched",
                "Status":"Failed"

            }
        }
        return Response(Response_)

@api_view(['POST'])
def forgotpassword(request,id):
    newpassword=request.POST.get('newpassword')
    confirmpassword=request.POST.get('confirmpassword')
    objectpass=usermaster.objects.filter(id=id).first()

    if newpassword == confirmpassword:
        data={}
        data ['password']=make_password(request.POST.get('password'))
        serializer=Userserializer(objectpass,data=data,partial = True)
        if serializer.is_valid():
            serializer.save() 
            Response_ = {
                "data":serializer.data,
                "response":{
                    "n":1,
                    "Status":"Success",
                    "msg":"password change successfully"

                }
            }
            return Response(Response_)
        else:
            Response_ = {
                "data":serializer.errors,
                "response":{
                    "n":0,
                    "Status":"unsucessful",
                    "msg":"Failed to change password"
                }
            }
            return Response(Response_)
    else:
            Response_ = {
                "data":serializer.errors,
                "response":{
                    "n":0,
                    "Status":"unsucessful",
                    "msg":"password dose not match"
                }
            }
            return Response(Response_)



#login logout front

# def loginAdd(request):
#         if request.method == "POST":
#             # token = request.session.get('')
#             data={}
#             data['email'] = request.POST.get('email')
#             data['password'] = request.POST.get('password')
#             # data['username'] = request.POST.get('Name')

#             print("sushant",data)

#             responseUrl = requests.post(addurl,data=data)
#             result = responseUrl.json()
#             print("result",result)
#             request.session['email'] = request.POST.get('email')
#             request.session['token'] = result['token']
#             # request.session['namess'] = result['names'] 
#             print(result['name'])
#             namevar = result['name']
#             request.session['name'] = namevar
#             nammmee=request.session.get('name')
#             # print("userrrrrr",request.session['names'])
#             print("asfsdbdgf",request.session['token'])
#             if result['Status'] == 'Success':
#                 return render (request,'admin_theme/index.html' ,{'data':result,"nammmee":nammmee})

#             else:
#                 return HttpResponse("unsuccsessful")
#         return render (request,'admin_theme/login.html')

# def loginAdd(request):
#     if request.method == "POST":
#         data = {
#             'email': request.POST.get('email'),
#             'password': request.POST.get('password')
#         }
#         print("sushant", data)

#         responseUrl = requests.post(addurl, data=data)
#         result = responseUrl.json()
#         print("result", result)

#         if result['Status'] == 'Success':
#             request.session['email'] = request.POST.get('email')
#             request.session['token'] = result['token']
#             request.session['name'] = result.get('name')  # Set the name in the session

#             nammmee = request.session.get('name')
#             print("asfsdbdgf", request.session['token'])

#             return render(request, 'admin_theme/index.html', {'data': result, "nammmee": nammmee})
#         else:
#             return HttpResponse("Login unsuccessful. Enter Wrong Email And Password")
    
#     return render(request, 'admin_theme/login.html')

# def userlogout(request):
#     data = {}
#     data ['email'] = request.session.get('email')
#     # emailobject = request.session.get('email' )
#     token = request.session.get('token')
#     print ("token",token)
#     t = 'Token {}'.format(token)
#     headers = {'Authorization': t}
#     responseUrl = requests.post(logouturl,headers=headers,data=data)
#     result = responseUrl.json()
#     print ("result",result)
    
#     return redirect('Empmaster:loginAdd')


#permission

@api_view(['GET'])
def perm(request):
    item = MenuItem.objects.all()
    serializer = MenuIdserializer(item,many=True)
    Response_ = {
        "GetData":serializer.data,
        "response":{
            "n":1,
            "msg":"Data found succefully",
            "Status":"Success"
        }
    }
    return Response(Response_)



   
#give permissions
@api_view(['POST'])
def Permissionadd(request):
    data={}
    data['Role_Id'] = request.POST.get('Role_Id')      
    data['checkbox_id'] = request.POST.getlist('checkbox_id')
    permissionobj = Permission.objects.filter(Role_Id=data['Role_Id']).first()
    if  permissionobj is not None:
        # userializer = Permissionserializer(permissionobj, data=data)
        # if userializer.is_valid():
        #     userializer.save() 
        # print ("datassss",data)
        serializer=Permissionserializer(permissionobj,data=data)
        if serializer.is_valid():
            serializer.save() 
            Response_ = {
                "data":serializer.data,
                "response":{
                    "n":1,
                    "Status":"Success",
                    "msg":"permission saved successfully"

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
    else:
        serializer=Permissionserializer(data=data)
        if serializer.is_valid():
            serializer.save() 
            Response_ = {
                "data":serializer.data,
                "response":{
                    "n":1,
                    "Status":"Success",
                    "msg":"permission saved successfully"

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
def permissiondetails(request,Role_Id):
    item = Permission.objects.filter(Role_Id=Role_Id)
    serializer = Permissionserializer(item,many=True)
    Response_ = {
        "Getpermission":serializer.data,
        "response":{
            "n":1,
            "msg":"Data found succefully",
            "Status":"Success"
        }
    }
    return Response(Response_)

@api_view(['GET'])
def getrolepermission (request,id):
    getuserobject = Permission.objects.filter(Role_Id=id).first()

    if getuserobject is not None:
        serializer = Permissionserializer(getuserobject,many=True)
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
            "roledata":{},
            "response":{
                "n":0,
                "msg":"No role found",
                "Status":"Failed"

            }
        }
        return Response(Response_)



    
@api_view(['POST'])
def updaterolepermission(request,id):
    UpdateUserObject = Permission.objects.filter(id=id).first()
    if UpdateUserObject is not None:
        data={}
        data['Role_Id'] = request.POST.get('Role_Id')      
        data['checkbox_id'] = request.POST.getlist('checkbox_id')    
        print("data",data)
        # serializer = Permissionserializer(UpdateUserObject,data=data)
        perobj = Permission.objects.filter(Role_Id = data['Role_Id']).first() 
        serializer = Permissionserializer(perobj,data=data)
        if perobj is not None:
    
            if serializer.is_valid():
                serializer.save()
                print("save",serializer.data)
                Response_ = {
                    "data":serializer.data,
                    "response":{
                        "n":1,
                        "msg":"Role_Id   has been Updated successfully",
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
                        "msg":"Error updating Role_Id",
                        "Status":"Success"

                    }
                }
                return Response(Response_)
    else:
        Response_ = {
            "data":{},
            "response":{
                "n":0,
                "msg":"Role_Id not Found",
                "Status":"Failed"

            }
        }
        return Response(Response_)


@api_view(['GET'])
def getpermission(request,id):
    getuserobject = Permission.objects.filter(id=id)
    if getuserobject is not None:
        serializer = Roleserializer(getuserobject,many=True)
        Response_ = {
            "GetDatarole":serializer.data,
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
def detailspermission (request,Role_Id):
    item = Permission.objects.filter(Role_Id=Role_Id)
    serializer = Permissionserializer(item,many=True)
    menuObject = MenuItem.objects.all()
    menuSerializer = MenuIdserializer(menuObject,many=True) 
    # return Response(serializer.data)
    Response_ = {
        "PermissionList":serializer.data,
        "MenuIdList":menuSerializer.data,
        "response":{
            "n":1,
            "msg":"Data found succefully",
            "Status":"Success"
        }
        }
    return Response(Response_)




    
