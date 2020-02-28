from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def user_to_validate(self,data):
        errors={}
        if len(data['form_fname']) < 2:
            errors['fname']='The character must be five characters long'
        if len(data['form_lname']) < 2:
            errors['lname']= 'The character must be five characters long'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['form_email']):
            errors['email'] = "Invalid email address!"
        if len(data['form_email']) < 2:
            errors['email']= 'It should be a valid email'
        if len(data['form_pw']) < 0:
            errors['pw']= 'You cannot register without a valid password'
        useremail = User.objects.filter(email=data['form_email'])
        if len(useremail) != 0:
            print(useremail)
            errors['emailTaken']= 'This email has already been taken'
        return errors

    def LoginValidation(self,data):
        Userlogin = User.objects.filter(email=data['form_email'])
        errors ={}
        if len(Userlogin) == 0:
            errors['noemail'] = 'This email has not been registered'
        else:
            user = Userlogin[0]
            if bcrypt.checkpw(data['form_pw'].encode(),user.password.encode()):
                print(user)
            else:
                errors['password'] = 'The password does not match'
            
        return errors

class GroupManager(models.Manager):
    def orgValidations(self,data):
        errors= {}
        if len(data['orgname']) < 5:
            errors['name'] = 'A valid organization name is required'
        if len(data['desc']) < 10:
            errors['description'] = 'You need to add a description about your organization' 
        return errors
        
# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Group(models.Model):
    orgname = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(User,related_name='creators',on_delete = models.CASCADE)
    member = models.ManyToManyField(User,related_name='members')
    objects = GroupManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

