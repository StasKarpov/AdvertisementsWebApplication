from advertisements.models import Category as CategoryModel
from advertisements.models import SubCategory as SubCategoryModel
from advertisements.models import Advertisement as AdvertisementModel

from advertisements.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator





class Categories(APIView):
    """
    Get a list of categories and create new category
    """
    def get(self,request,format=None):
        #get list of all catogories
        categories = CategoryModel.objects.all()
        serializer = CategorySerializer(categories, many = True)
        return Response(JSONRenderer().render(serializer.data),
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        #add category
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(JSONRenderer().render(serializer.data),
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategory(APIView):
    """
    add Subcategories
    """
    def get(self,request,pk):
        #returns list of subcategories for given category
        category = get_object_or_404(Category.objects.all(),
                                    pk=pk)
        subcategories = SubCategoryModel.objects.filter(category=category)
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(JSONRenderer().render(serializer.data),
                        status=status.HTTP_200_OK)

    def post(self,request):
        #creates subcategory
        try:
            CategoryModel.objects.get(pk=request.data['category_id'])
        except CategoryModel.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = SubCategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(JSONRenderer().render(serializer.data),
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Advertisement(viewsets.ViewSet):
    """
    Get list of Advertisement and add new advertisement
    """

    #packs advertisements makes pagination and sends response
    def paginatedResponse(self,advertisements,page=1):
        paginator = Paginator(advertisements,10)
        try:
            ads = paginator.page(page)
        except EmptyPage:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdvertisementSerializer(ads,many=True)
        return Response(JSONRenderer().render(serializer.data),
                        status=status.HTTP_200_OK)

    def get(self,request,pk):
        ad = get_object_or_404(AdvertisementModel.objects.all(),pk=pk)
        serializer = AdvertisementSerializer(ad)
        return Response(JSONRenderer().render(serializer.data),
                        status=status.HTTP_200_OK)

    #list all ads in category
    def listAdsForCategory(self,request,pk,page=1):
        category = get_object_or_404(Category.objects.all(),
                                    pk=pk)
        advertisements = AdvertisementModel.objects.filter(category=category)
        return self.paginatedResponse(advertisements=advertisements,page=page)
    #list all ads in  subcategory
    def listAdsForSubCategory(self,request,pk,page=1):
        subcategory = get_object_or_404(SubCategory.objects.all(),
                                    pk=request['subcategory_id'])
        advertisements = AdvertisementModel.objects.filter(subcategory=subcategory)
        return self.paginatedResponse(advertisements=advertisements,page=page)


    def listAllAds(self,request,page=1):
        advertisements = AdvertisementModel.objects.all()
        return self.paginatedResponse(advertisements=advertisements,page=page)


    def listAdsForUser(self,request,userid,page=1):
        #TODO:check if user exist
        advertisements = AdvertisementModel.objects.filter(author_id=userid)
        return self.paginatedResponse(advertisements=advertisements,page=page)

    def post(self,request):
        serializer = AdvertisementSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        ad = get_object_or_404(AdvertisementModel.objects.all(),pk=pk)
        serializer = AdvertisementSerializer(ad,data=request.data,partial=True)
        if serializer.is_valid():
           serializer.save()
           return Response(status=status.HTTP_202_ACCEPTED)
        return Response( status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        ad = get_object_or_404(AdvertisementModel.objects.all(), pk=pk)
        ad.delete()
        return Response(status=status.HTTP_200_OK)
