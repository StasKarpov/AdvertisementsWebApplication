from django.conf.urls import url

from advertisements.views_advertisements import *
from advertisements.views_user import *
urlpatterns = [
    #create subcategory
    url(r'sub_category/create/$', SubCategory.as_view()),
    #get subcategories for category.pk
    url(r'category/(?P<pk>[0-9]+)/sub_categories/$', SubCategory.as_view()),
    #create category
    url(r'category/create/$', Categories.as_view()),
    #get categories
    url(r'category/list/$', Categories.as_view()),
    #create advertisement
    url(r'advertisement/create/$', Advertisement.as_view({'post':'post'})),
    #edit advertisement
    url(r'advertisement/(?P<pk>[0-9]+)/edit/$', Advertisement.as_view({'put':'put'})),
    #get ads for category.pk
    url(r'category/(?P<pk>[0-9]+)/(?P<page>[0-9]+)/$', Advertisement.as_view({'get':'listAdsForCategory'})),
    #get ads for subcategory.pk
    url(r'sub_category/(?P<pk>[0-9]+)/(?P<page>[0-9]+)/$', Advertisement.as_view({'get':'listAdsForSubCategory'})),
    #get single ad
    url(r'advertisement/(?P<pk>[0-9]+)/$', Advertisement.as_view({'get':'get'})),
    #get all advertizements
    url(r'advertisements/(?P<page>[0-9]+|)/$', Advertisement.as_view({'get':'listAllAds'})),
    #get ads for user.id
    url(r'user/(?P<userid>[0-9]+)/advertisements/$', Advertisement.as_view({'get':'listAdsForUser'})),


    #auth
    url(r'user/register/$', UserCreationView.as_view()),
    url(r'user/login/$', UserLoginView.as_view()),
    url(r'user/logout/$', UserLogoutView.as_view()),
]
