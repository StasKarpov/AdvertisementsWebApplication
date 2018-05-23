from django.test import TestCase
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token as TokenModel
from advertisements import viewsUser


BLANK_FIELD = 'This field may not be blank.'
USER_EXIST = 'User with given username already exists.'
TOKEN_ALREADY_GEN = 'User alredy logged in.'
UNAUTH_USER = 'Authentification failed.'

class UserCreationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testin', \
            password="testcase123", email="testing123@gmail.com")
        self.user.is_active = True
        self.user.save()


    def setData(self, username, password, email):
        return {'username': username, 'password': password, 'email': email}

    def test_get_request(self):
        response = self.client.get("/user/register/")
        self.assertEqual(response.status_code, 405)

    def test_user_is_created_with_corret_data(self):
        data = self.setData('testuser', 'testing123', \
            'testcase123@gmail.com')

        # create user with valid data
        response = self.client.post('/user/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email']})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.all().filter(username=data['username']).count(), 1)


    def test_fails_user_creation_with_incorrect_email(self):
        data = self.setData('testuser', 'testing123', \
            'testcase123')

        # create user with valid data
        response = self.client.post('/user/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Test User'})
        self.assertEqual(response.status_code, 400)

    def test_fails_user_creation_without_username(self):
        data = self.setData('', 'testing123', \
            'testcase123@gmaik.com')

        # create user without username
        request = self.client.post('/user/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})
        # self.assertTrue(BLANK_FIELD in request.data['username'])

        # and code equal 400
        self.assertEqual(request.status_code, 400)

    def test_fails_user_creation_without_password(self):
        data = self.setData('testuser', '', \
            'testcase123@gmaik.com')

        request = self.client.post('/user/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})
        #self.assertTrue(BLANK_FIELD in request.data['password'])

        # and code equal 400
        self.assertEqual(request.status_code, 400)

    def test_fails_user_creation_without_email(self):
        data = self.setData('testuser', 'testing123', \
            '')

        # create user without username
        request = self.client.post('/user/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email']})
        #self.assertTrue(BLANK_FIELD in request.data['email'])

        # and code equal 400
        self.assertEqual(request.status_code, 400)

    def test_fails_user_creation_without_username(self):
        data = self.setData( '','testing123', \
            'testcase123@gmail.com')

        # create user without username
        request = self.client.post('/user/register/', { \
            'username' : data['username'],
             'password': data['password'], \
                'email': data['email']})
        self.assertEqual(request.status_code, 400)

    def test_fails_with_already_regis_username(self):
        data = self.setData('testin', 'testing123', \
            'testcase123@gmail.com')

        request = self.client.post('/user/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email']})

        #self.assertEqual(self.user.username
        #,request.data['username'])

        # and code equal 400
        self.assertEqual(request.status_code, 400)



class UserLoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testin', \
            password="testcase123", email="testing123@gmail.com")
        self.user.is_active = True
        self.user.save()


    def setData(self, username, password):
        return {'username': username, 'password': password}

    def test_user_login_with_correct_data_gets_token(self):
        data = self.setData(self.user.username, \
            'testcase123')
        # logout before login
        self.client.logout()

        # send request to login
        request = self.client.post('/user/login/', {
            'username': data['username'], 'password': data['password']
        })
        # get current user
        user = auth.get_user(self.client)
        self.assertEqual(user, self.user)

        # check if loged user gets the same token
        token = TokenModel.objects.get(user=user)
        self.assertEqual(request.data['token'], token.key)

        # logout and check if user is anonymous
        self.client.logout()
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

    def test_unauth_user(self):
        request = self.client.post('/user/login/', {
            'username': self.user.username, 'password': '123123'
        })

        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

        self.assertEqual(request.status_code, 401)
        self.assertEqual(UNAUTH_USER, request.data['detail'])




class UserLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testin', \
            password="testcase123", email="testing123@gmail.com")
        self.user.is_active = True
        self.user.save()


    def test_token_deletes_after_loging_out(self):
        self.client.logout()
        # to get token for self.user
        request = self.client.post('/user/login/', {
            'username': self.user.username, 'password': 'testcase123'
        })
        self.client.logout()

        token = TokenModel.objects.get(user=self.user)

        authoriz = 'Token ' + str(token)

        # check token deletes after loging out
        request = self.client.post('/user/logout/', HTTP_AUTHORIZATION="Token {}".format(token))

        # check if not anonymous
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

        # Validation error because token was deleted after logout
        with self.assertRaises(ObjectDoesNotExist):
            token = TokenModel.objects.get(user=self.user)
