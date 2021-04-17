from django.urls import include, path
from .views import departement_views, cmail_views, cmail_views_for_jquery, departement_views_for_jquery


app_name = 'rcmails'


urlpatterns = [

    ####################### urls for 'departements' curd operations #######################
    path('departement/', departement_views.DepartementList.as_view(), name='departement_list'),
    path('departement/add/', departement_views.DepartementCreate.as_view(), name='departement_add'),
    path('departement/<int:pk>/detail/', departement_views.DepartementDetail.as_view(), name='departement_detail'),
    path('departement/<int:pk>/update/', departement_views.DepartementUpdate.as_view(), name='departement_update'),
    path('departement/<int:pk>/delete/', departement_views.DepartementDelete.as_view(), name='departement_delete'),

    ####################### urls for 'departements' curd operations using JQuery #######################
    path('i/departement/', departement_views_for_jquery.departement_list, name='departement_list'),
    path('i/departement/add/', departement_views_for_jquery.departement_create, name='departement_add_for_jquery'),
    path('i/departement/<int:pk>/detail/', departement_views_for_jquery.departement_detail, name='departement_detail_for_jquery'),
    path('i/departement/<int:pk>/update/', departement_views_for_jquery.departement_update, name='departement_update_for_jquery'),
    path('i/departement/<int:pk>/delete/', departement_views_for_jquery.departement_delete, name='departement_delete_for_jquery'),


    ####################### urls for 'cmails' curd operations #######################
    path('cmail/', cmail_views.CmailList.as_view(), name='cmail_list'),
    path('cmail/add/', cmail_views.CmailCreate.as_view(), name='cmail_add'),
    path('cmail/<int:pk>/detail/', cmail_views.CmailDetail.as_view(), name='cmail_detail'),
    path('cmail/<int:pk>/update/', cmail_views.CmailUpdate.as_view(), name='cmail_update'),
    path('cmail/<int:pk>/delete/', cmail_views.CmailDelete.as_view(), name='cmail_delete'),


    ####################### urls for 'cmails' curd operations using JQuery #######################
    # path('i/cmail/', cmail_views_for_jquery.CmailList.as_view(), name='cmail_list'),
    # path('i/cmail/add/', cmail_views_for_jquery.CmailCreate.as_view(), name='cmail_add_for_jquery'),
    # path('i/cmail/<int:pk>/detail/', cmail_views_for_jquery.CmailDetail.as_view(), name='cmail_detail_for_jquery'),
    # path('i/cmail/<int:pk>/update/', cmail_views_for_jquery.CmailUpdate.as_view(), name='cmail_update_for_jquery'),
    # path('i/cmail/<int:pk>/delete/', cmail_views_for_jquery.CmailDelete.as_view(), name='cmail_delete_for_jquery'),


]


