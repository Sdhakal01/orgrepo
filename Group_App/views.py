from django.shortcuts import render,redirect
from Group_App.models import User, Group
import bcrypt
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request,'index.html')

def create(request):
    errors = User.objects.user_to_validate(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
           messages.error(request,value)
      return redirect('/main')
    
    else:
        password = request.POST['form_pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()     
        print(pw_hash)  
        newuser = User.objects.create(firstname=request.POST['form_fname'],lastname = request.POST['form_lname'],email=request.POST['form_email'],password=pw_hash)
        request.session['UserId']= newuser.id
    return redirect('/groups')

def login(request):
    errors = User.objects.LoginValidation(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
           messages.error(request,value)
      return redirect('/main')
    else:
        loggeduser = User.objects.filter(email = request.POST['form_email'])
        loggeduser = loggeduser[0]
        request.session['UserId'] = loggeduser.id
    return redirect('/groups')

# this_book = Book.objects.get(id=4)	# retrieve an instance of a book
# this_publisher = Publisher.objects.get(id=2)	# retrieve an instance of a publisher
    
# # 2 options that do the same thing:
# this_publisher.books.add(this_book)		# add the book to this publisher's list of books
# # OR
# this_book.publishers.add(this_publisher)	# add the publisher to this book's list of publishers

def allgroups(request):
  loggedinuser = User.objects.get(id = request.session['UserId'] )
  allorg = Group.objects.all()
  
  context={ 
    'loggedinuser' : loggedinuser,
    'allorg' : allorg,
   }
  return render(request,'group.html',context)

def orgcreate(request):
  errors = Group.objects.orgValidations(request.POST)
  loggedinuser = User.objects.get(id = request.session['UserId'])
  if len(errors) > 0:
      for key, value in errors.items():
          messages.error(request,value)
      return redirect('/groups')
  else:
    neworg = Group.objects.create(orgname=request.POST['orgname'],description=request.POST['desc'],creator = loggedinuser )
    
  return redirect('/groups')

def joingroup(request,groupId):
  loggedinuser = User.objects.get(id=request.session['UserId'])  
  grouptoshow = Group.objects.get(id=groupId)
  allmembers = Group.objects.all()
  context ={
    'grouptoshow' : grouptoshow,
    'loggedinuser' : loggedinuser,
    'allmembers' : allmembers,
    
  }
  return render(request,'join.html',context)

def add(request,groupId):
  grouptoadd = Group.objects.get(id=groupId)
  loggedinuser = User.objects.get(id=request.session['UserId'])
  grouptoadd.member.add(loggedinuser)
  return redirect(f'/groups/{groupId}')

def leave(request,groupId):
  grouptoleave = Group.objects.get(id=groupId)
  loggedinuser = User.objects.get(id=request.session['UserId'])
  grouptoleave.member.remove(loggedinuser)
  return redirect(f'/groups/{groupId}')

def dashboard(request):
  return redirect('/groups')
  
def delete(request,groupId):
  grouptodelete = Group.objects.get(id=groupId)
  grouptodelete.delete()
  return redirect('/groups')

def logout(request):
  request.session.clear()
  return redirect('/main')