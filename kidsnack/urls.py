# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^register/$', 'member.views.register'),
                       url(r'^login/$', 'member.views.login'),
                       url(r'^user/del/$', 'member.views.user_delete'),

                       url(r'^snack/$', 'food.views.snack_list'),
                       url(r'^snack/detail/$', 'food.views.snack_detail'),
                       url(r'^snack/search/$', 'food.views.snack_search'),
                       url(r'^snack/name/auto/complete/$', 'food.views.snack_name_auto_complete'),
                       url(r'^snack/compare/$', 'food.views.snack_compare'),

                       url(r'^snack/like/list/$', 'food.views.snack_like_list'),
                       url(r'^snack/hate/list/$', 'food.views.snack_hate_list'),

                       url(r'^snack/like/$', 'food.views.snack_like'),
                       url(r'^snack/hate/$', 'food.views.snack_hate'),

                       url(r'^snack/like/del/$', 'food.views.snack_like_del'),
                       url(r'^snack/hate/del/$', 'food.views.snack_hate_del'),

                       url(r'^snacks/like/del/all/$', 'food.views.snack_like_del_all'),
                       url(r'^snacks/hate/del/all/$', 'food.views.snack_hate_del_all'),
                       
                       url(r'^snack/require/$', 'food.views.snack_require'),                       
                       )

