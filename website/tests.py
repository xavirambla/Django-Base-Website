from django.test import tag
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your tests here.



def insertUsers():
    resultList = User.objects.all()
    if resultList.count() < 10:  
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'Password123.')
        user.save()

        user = User.objects.create_user('paul', 'mccartney@thebeatles.com', 'Password123.')
        user.save()

        user = User.objects.create_user('george', 'harrison@thebeatles.com', 'Password123.')
        user.save()

        user = User.objects.create_user('ringo', 'starr@thebeatles.com', 'Password123.')
        user.save()

        user = User.objects.create_user('freddie', 'mercury@queen.com', 'Password123.')
        user.save()

        user = User.objects.create_user('brian', 'may@queen.com', 'Password123.')
        user.save()

        user = User.objects.create_user('roger', 'taylor@queen.com', 'Password123.')
        user.save()

        user = User.objects.create_user('johndeacon', 'deacon@queen.com', 'Password123.')
        user.save()

        user = User.objects.create_user('brianjones', 'jones@rollingstones.com', 'Password123.')
        user.save()

        user = User.objects.create_user('mick', 'jagger@rollingstones.com', 'Password123.')
        user.save()

        user = User.objects.create_user('keith', 'richards@rollingstones.com', 'Password123.')
        user.save()

        user = User.objects.create_user('bill', 'wyman@rollingstones.com', 'Password123.')
        user.save()

        user = User.objects.create_user('charlie', 'watts@rollingstones.com', 'Password123.')
        user.save()

        user = User.objects.create_user('ian', 'stewart@rollingstones.com', 'Password123.')
        user.save()



# Authentication 

@tag('authentication','view')
class athentication_ViewsTest(TestCase):

    @classmethod         
    def setUp(self):
        insertUsers()

    @tag('index')
    def test_index_view(self):
        url = reverse("index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
     
        self.assertTrue("container_main" in response.content.decode())
        self.assertTrue("/accounts/login/" in response.content.decode())
        self.assertTrue("/register" in response.content.decode())

    @tag('private_index')      
    def test_index_view_authentified(self):
        self.client.login(username='john', password='Password123.')
        response = self.client.get(reverse('index'),follow=True)   #página que requiere autorización para entrar

        self.assertEqual(response.status_code, 200)
        self.assertTrue("/accounts/logout/" in response.content.decode())
        self.assertTrue("/accounts/password_change/" in response.content.decode())


    @tag('bad_password')      
    def test_index_view_badpassword(self):
        self.client.login(username='john', password='aaaa')
        response = self.client.get(reverse('index'),follow=True)   #página que requiere autorización para entrar

        self.assertEqual(response.status_code, 200)
        self.assertTrue("/accounts/login/" in response.content.decode())
        self.assertTrue("/register" in response.content.decode())



    @tag('register')               
    def test_register_view(self):
        url = reverse("register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTrue("/accounts/login/" in response.content.decode())   # check no estamos autenticados

        #comprobamos que le solicitado los datos del cliente
        self.assertTrue("username" in response.content.decode())   
        self.assertTrue("first_name" in response.content.decode())  
        self.assertTrue("last_name" in response.content.decode())   
        self.assertTrue("/register" in response.content.decode()) 



#--------------------------------------------------------
    @tag( 'forms', 'usuario','register' )
    def test_register(self):
        form_data = {  'username'   : 'testForm' , 
                       'first_name' :'firstNameForm',  
                       'last_name'  : 'lastNameForm', 
                       'email'      : 'emailform@email.com', 
                       'password'   : 'passworD1.' }

        url = reverse("register")        
        count = User.objects.all().count()
        response = self.client.post(url, form_data)

        self.assertEqual( User.objects.all().count() ,  count + 1 )                 
        self.assertEqual(response.status_code, 200)                 
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "alert-info")
        self.assertTrue("Usuario creado." in message.message)


    @tag( 'forms', 'usuario','register_bad_password' )
    def test_register_badPassword(self):
        form_data = {  'username'   : 'testForm' , 
                       'first_name' :'firstNameForm',  
                       'last_name'  : 'lastNameForm', 
                       'email'      : 'emailform@email.com', 
                       'password'   : '' }

        url = reverse("register")    
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 200)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "alert-danger")
        self.assertTrue("This password is too short. It must contain at least 8 characters" in message.message)



    @tag('forms', 'usuario', 'register' , 'register_duplicated' )
    def test_register_duplicated(self):
        self.user = User.objects.create_user('john1', 'lennon1@thebeatles.com', 'Johnpa.s12sword')        
        form_data = {  'username'   : 'john1' , 
                       'first_name' :'firstNameForm',  
                       'last_name'  : 'lastNameForm', 
                       'email'      : 'emailform@email.com', 
                       'password'   : 'pas1rd!a2.' }

        url = reverse("register")        
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
          
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "alert-danger")
        self.assertTrue("Usuario ya existe, escoja otro nombre de usuario." in message.message)
    

    @tag('forms', 'usuario', 'login' )
    def test_login(self):
        self.user = User.objects.create_user('john1', 'lennon1@thebeatles.com', 'johnpassword')  
              
        form_data = {  'username'   : 'john1' , 
                       'password'   : 'johnpassword' }

        url = reverse("login")        
        response = self.client.post(url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        #formulario de registro
        self.assertTrue("/accounts/logout/" in response.content.decode()) 
        self.assertTrue("/accounts/password_change/" in response.content.decode()) 

    @tag( 'forms', 'usuario','login' ,'login_registrado' )
    def test_login_registrado(self):
        self.user = User.objects.create_user('john1', 'lennon1@thebeatles.com', 'johnpassword')        
        form_data = {  'username'   : 'john1' , 
                       'password'   : 'johnpassword' }

        url = reverse("login")        
        response = self.client.post(url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # dentro de la intranet
        self.assertTrue("/accounts/logout/" in response.content.decode()) 
        self.assertTrue("/accounts/password_change/" in response.content.decode()) 

    @tag( 'forms', 'usuario','login' ,'login_notFound' )
    def test_login_notFound(self):
        form_data = {  'username'   : 'testForm' , 
                       'password'   : 'password' }

        url = reverse("login")        
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 200)
        print (f"ZAAAZZZ : {response.content.decode()}")  
        self.assertTrue(_("Your username and password didn't match. Please try again.") in response.content.decode()) 




    @tag('passwordReset')
    def test_passwordReset_view(self):
        url = reverse("password_reset")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("/accounts/login/" in response.content.decode())   # check no estamos autenticados
        self.assertTrue("Reset password" in response.content.decode())  


    @tag( 'forms', 'passwordReset' )
    def test_passwordReset_form(self):
        form_data = {  'email'   : 'harrison@thebeatles.com' , }

        url = reverse("password_reset")        
        response = self.client.post(url, form_data , follow=True)

        self.assertEqual(response.status_code, 200)
  #      self.assertTrue("Email enviado." in response.content.decode())         
        self.assertTrue("We've emailed you instructions for setting your password. If they haven't arrived in a few minutes, check your spam folder." in response.content.decode()) 

    @tag( 'forms', 'passwordReset' )
    def test_passwordReset_form_notUser(self):
        form_data = {  'email'   : 'test@hotmail.com' , }

        url = reverse("password_reset")        
        response = self.client.post(url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        #sistema automáticamente dice siempre que l oenvía , tanto si existe cómo si no el email
#        self.assertTrue("Email no registrado." in response.content.decode())         
        self.assertTrue("We've emailed you instructions for setting your password. If they haven't arrived in a few minutes, check your spam folder." in response.content.decode()) 
        self.assertTrue("Reset password" in response.content.decode()) 



    @tag('my_account')      
    def test_index_view_myaccount(self):
        self.client.login(username='john', password='Password123.')
        response = self.client.get(reverse('my_account'))   #página que requiere autorización para entrar

        self.assertEqual(response.status_code, 200)
        self.assertTrue("/accounts/logout/" in response.content.decode())
        self.assertTrue("/accounts/password_change/" in response.content.decode())
        self.assertTrue("/accounts/details/" in response.content.decode())
        self.assertTrue(f'name="username" value="john"' in response.content.decode())


    @tag( 'forms', 'my_account' )
    def test_index_view_myaccount_form(self):
        self.client.login(username='john', password='Password123.')
        user =  User.objects.filter(username = 'john')[0]
        
        form_data ={'username' : user.username , 'first_name' : user.first_name, 'last_name' : user.last_name , 'email' :user.email}
        url = reverse("my_account")        
        response = self.client.post(url, form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        #sistema automáticamente dice siempre que l oenvía , tanto si existe cómo si no el email
#        self.assertTrue("Email no registrado." in response.content.decode())         
        self.assertTrue("Datos modificados." in response.content.decode()) 

    @tag( 'forms', 'my_account' )
    def test_index_view_myaccount_form_usernameNotValid(self):
        self.client.login(username='john', password='Password123.')
        user =  User.objects.filter(username = 'john')[0]
        
        form_data ={'username' : 'a' , 'first_name' : user.first_name, 'last_name' : user.last_name , 'email' :user.email}
        url = reverse("my_account")        
        response = self.client.post(url, form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        #sistema automáticamente dice siempre que l oenvía , tanto si existe cómo si no el email
#        self.assertTrue("Email no registrado." in response.content.decode())         
        self.assertTrue("Please correct the error below." in response.content.decode()) 
        self.assertTrue('<ul class="errorlist"><li>Invalid username - field too short </li></ul>' in response.content.decode()) 

    @tag( 'forms', 'my_account', 'myaccount_form_usernameEmpty' )
    def test_index_view_myaccount_form_usernameEmpty(self):
        self.client.login(username='john', password='Password123.')
        user =  User.objects.filter(username = 'john')[0]
        
        form_data ={'username' : '' , 'first_name' : user.first_name, 'last_name' : user.last_name , 'email' :user.email}
        url = reverse("my_account")        
        response = self.client.post(url, form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        #sistema automáticamente dice siempre que l oenvía , tanto si existe cómo si no el email
#        self.assertTrue("Email no registrado." in response.content.decode())         
        self.assertTrue("This field is required." in response.content.decode()) 



    @tag( 'forms', 'my_account', 'myaccount_form_emailInvalid' )
    def test_index_view_myaccount_form_emailInvalid(self):
        self.client.login(username='john', password='Password123.')
        user =  User.objects.filter(username = 'john')[0]
        
        form_data ={'username' : user.username , 'first_name' : user.first_name, 'last_name' : user.last_name , 'email' :'aaa'}
        url = reverse("my_account")        
        response = self.client.post(url, form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        #sistema automáticamente dice siempre que l oenvía , tanto si existe cómo si no el email
#        self.assertTrue("Email no registrado." in response.content.decode())         
        self.assertTrue("Enter a valid email address." in response.content.decode()) 




#        print (f"ZZZZ : {response.content.decode()}")  




