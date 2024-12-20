from django.urls import path
from . import views
from django.conf import settings
#from service4me.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
#from django.views.generic.dates import DateDetailView
urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='book/library.html'), name = 'index'),
    ##path('upload/', views.upload, name = 'upload-data'),
    path('getdata/update/<int:book_id>', views.update_book),
    path('getdata/delete/<int:book_id>', views.delete_book),

    path('sumreceived/getdata/update/<int:book_id>', views.sum_update_book),
    path('sumspent/getdata/update/<int:book_id>', views.sum_update_spent),

    path('sumreceived/<int:date>', views.getdata_e),
    path('sumreceived/getdata/<int:date>', views.getdata_e),
    path('sumspent/getdata/<int:date>', views.getdata_s),

    path('getdata/', views.getdata, name = 'get_data'),
    path('sumreceived/', views.sum, name = 'get_sum'),
    path('sumspent/', views.sumspent, name = 'get_sum_spent'),
    ##path('upload_spent/', views.upload_spent, name = 'upload-data-spent'),
    path('getspentdata/', views.getspentdata, name = 'get_data_spent'),
    path('getspentdata/delete/<int:book_id>', views.delete_spent),
    path('getspentdata/update/<int:book_id>', views.update_spent),
    #path('monthreceived/', views.month_received, name = 'month_received'),

    path('register/', views.register, name='register'),
    #path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='book/library.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='book/logout.html'), name= 'logout'),

    path('home/',views.home, name= 'home'),
    path('worktrack/',views.work_track, name= 'worktrack'),
    path('create/', views.Createjob, name='create_job'),
    path('worktrack/update/<int:book_Sno>', views.update_job),
    path('worktrack/delete/<int:book_Sno>', views.delete_job),

    path('marriage/',views.mrg_track, name= 'marriage'),
   # path('createmrg/', views.Createjobmrg, name='create_job_mrg'),
    path('marriage/update/<int:Sno>', views.update_marriage),
    path('marriage/delete/<int:book_Sno>', views.delete_marriage),
    path('marriage/more_details/<int:book_Sno>', views.mrg_more_details),

    ##path('image_upload/', views.hotel_image_view, name = 'image_upload'),
    ##path('success', views.success, name = 'success'),

    path('pie_chart/', views.pie_chart, name='pie-chart'),
    path('pie_chart_spent/', views.pie_chart_spent, name='pie_chart_spent'),

    path('email/', views.email ),
    ##path('email/', views.email ),
    ##path('new_look/', views.new_look, name = 'new_look'),

############################# Ice Cream ############################
    path('ic_product_list/', views.ic_product_list,name='ic_product_list'),
    path('ic_expensive/', views.ic_expensive,name='ic_expensive'),
    path('stock_purchase/', views.stock_purchase,name='stock_purchase'),
    path('IC_Stock_sold_details/', views.IC_Stock_sold_details,name='IC_Stock_sold_details'),
    path('ic_stock_left/', views.ic_stock_left,name='ic_stock_left'),
#########################################################
    path('cloths_bill/', views.cloth_bill_view, name='cloths_bill'),

]
#DataFlair

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

