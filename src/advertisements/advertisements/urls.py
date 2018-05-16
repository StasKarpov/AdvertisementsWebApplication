from django.conf.urls import url
from django.contrib import admin

from advertisements.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'sub_category/create/$', SubCategory.as_view()),
    url(r'category/(?P<pk>[0-9]+)/sub_categories/$', SubCategory.as_view()),
    url(r'category/create/$', Categories.as_view()),
    url(r'category/list/$', Categories.as_view()),
    url(r'advertisement/create/$', Advertisement.as_view({'post':'post'})),
    url(r'category/(?P<pk>[0-9]+)/$', Advertisement.as_view({'get':'listAdsForCategory'})),
    url(r'sub_category/(?P<pk>[0-9]+)/$', Advertisement.as_view({'get':'listAdsForSubCategory'})),
    url(r'advertisement/$', Advertisement.as_view({'get':'listAllAds'}))

]
