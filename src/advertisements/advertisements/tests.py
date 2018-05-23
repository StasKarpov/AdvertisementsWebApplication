from django.test import TestCase
from advertisements import urls
from rest_framework.test import APIClient
from advertisements.models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
from advertisements.serializers import AdvertisementSerializer


class TestAdvertisements(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_category(self,number=10):
        counter = 1
        while counter != number+1 :
            Category.objects.create(title='test' + str(counter))
            counter+=1

    def create_category_and_sub(self,numberOfSubs=3):
        Category.objects.create(title='test')
        counter = 1
        while counter != numberOfSubs+1 :
            SubCategory.objects.create(category=Category.objects.all()[0],
                                        title='testSub' + str(numberOfSubs))
            counter+=1

    def create_adverisements(self,number=10):
        self.create_category_and_sub()
        counter = 1
        while counter != number+1:
            Advertisement.objects.create(category=Category.objects.all()[0],
                                        subcategory=SubCategory.objects.all()[0],
                                        title='test' + str(counter),
                                        price=counter,
                                        author_id=counter)
            counter+=1




    def testCreateCategory(self):
        request = self.client.post('/category/create/',\
                                    {
                                     'title': 'test_category',
                                     'description' : 'dis is test category'
                                     })
        self.assertEqual(request.status_code, 201)
        self.assertEqual(Category.objects.all().count(),1)

    def testGetCategoriesList(self):
        self.create_category(number=10)
        request = self.client.get('/category/list/')
        categories = json.loads(request.data)
        self.assertEqual(len(categories),10)
        self.assertEqual(request.status_code,200)


    def testCreateSubCategory(self):
        self.create_category(number=1)
        parentCategory = Category.objects.all()[0]
        request = self.client.post('/sub_category/create/',
                                    {
                                    'title': 'test_subcategory',
                                    'category_id': parentCategory.id
                                    })
        self.assertEqual(request.status_code,201)
        self.assertEqual(SubCategory.objects.all().count(),1)

    def testCreateSubCategoryToNonExistingCategory(self):
        request = self.client.post('/sub_category/create/',
                                    {
                                    'title': 'test_subcategory',
                                    'category_id': 1
                                    })
        self.assertEqual(request.status_code,400)
        self.assertEqual(SubCategory.objects.all().count(),0)

    def testGetSubCategoriesList(self):
        self.create_category_and_sub(numberOfSubs=3)
        request = self.client.get('/category/' + str(Category.objects.all()[0].id) +'/sub_categories/')
        subcategories = json.loads(request.data)
        self.assertEqual(len(subcategories),3)
        self.assertEqual(request.status_code,200)

    def testCreateAdvertisement(self):
        self.create_category_and_sub()
        category = Category.objects.all()[0]
        subcategory = SubCategory.objects.all()[0]

        request = self.client.post('/advertisement/create/',
                                    {
                                    'category': category.id,
                                    'subcategory': subcategory.id,
                                    'author_id' : 1,
                                    'title' : 'testAd',
                                    'price' : 5
                                    })
        self.assertEqual(request.status_code,201)
        self.assertEqual(Advertisement.objects.all().count(),1)

    def testEditAdvertisement(self):
        self.create_adverisements(number=1)
        ad = Advertisement.objects.all()[0]
        oldprice = ad.price
        request = self.client.put('/advertisement/'+str(ad.id)+'/edit/',
                                    {
                                    'price' : oldprice+1
                                    })
        self.assertEqual(request.status_code,202)
        self.assertEqual(oldprice+1,Advertisement.objects.all()[0].price)

    def testGetAd(self):
        self.create_adverisements(number=1)
        ad = Advertisement.objects.all()[0]
        request = self.client.get('/advertisement/'+ str(ad.id) + '/')
        self.assertEqual(request.status_code,200)
        adJson = json.loads(request.data)
        self.assertEqual(adJson['id'],ad.pk)

    def testListAdvertisementsForCategory(self):
        self.create_adverisements(number=10)
        request = self.client.get('/category/' +
                                str(Category.objects.all()[0].id) + '/1/')
        advertisements = json.loads(request.data)
        self.assertEqual(len(advertisements),10)
        self.assertEqual(request.status_code,200)

    def testListAdvertisementsForSubCategory(self):
        self.create_adverisements(number=10)
        request = self.client.get('/sub_category/' +
                                str(SubCategory.objects.all()[0].id) + '/1/')
        advertisements = json.loads(request.data)
        self.assertEqual(len(advertisements),10)
        self.assertEqual(request.status_code,200)

    def testAllAdvertisements(self):
        self.create_adverisements(number=10)
        request = self.client.get('/advertisements/1/')
        advertisements = json.loads(request.data)
        self.assertEqual(len(advertisements),10)
        self.assertEqual(request.status_code,200)

    def testAdsOfUser(self):
        self.create_adverisements(number=1)
        ad = Advertisement.objects.all()[0]
        request = self.client.get('/user/'+str(ad.author_id)+'/advertisements/')
        self.assertEqual(request.status_code,200)
        advertisements = json.loads(request.data)
        self.assertEqual(advertisements[0]['id'],ad.pk)

    def testPaginationListAdvertisementsForCategory(self):
        self.create_adverisements(number=15)
        request = self.client.get('/category/' +
                                str(Category.objects.all()[0].id) + '/1/')
        firstPage = json.loads(request.data)
        self.assertEqual(len(firstPage),10)
        self.assertEqual(request.status_code,200)
        request = self.client.get('/category/' +
                                str(Category.objects.all()[0].id) + '/2/')
        secondPage = json.loads(request.data)
        self.assertEqual(len(secondPage),5)
        self.assertEqual(request.status_code,200)

    def testPaginationListAdvertisementsForSubCategory(self):
        self.create_adverisements(number=15)
        request = self.client.get('/sub_category/' +
                                str(SubCategory.objects.all()[0].id) + '/1/')
        firstPage = json.loads(request.data)
        self.assertEqual(len(firstPage),10)
        self.assertEqual(request.status_code,200)
        request = self.client.get('/sub_category/' +
                                str(SubCategory.objects.all()[0].id) + '/2/')
        secondPage = json.loads(request.data)
        self.assertEqual(len(secondPage),5)
        self.assertEqual(request.status_code,200)

    def testPaginationAllAdvertisements(self):
        self.create_adverisements(number=15)
        request = self.client.get('/advertisements/1/')
        firstPage = json.loads(request.data)
        self.assertEqual(len(firstPage),10)
        self.assertEqual(request.status_code,200)
        request2 = self.client.get('/advertisements/2/')
        secondPage = json.loads(request2.data)
        self.assertEqual(len(secondPage),5)
        self.assertEqual(request.status_code,200)

    def testPaginationEmptyPage(self):
        request = self.client.get('/advertisements/2/')
        self.assertEqual(request.status_code,404)








        #print "sub cat test"
        #print JSONRenderer().render(request.data)
