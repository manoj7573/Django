from django.shortcuts import render, redirect
from .models import  *
from .forms import *
from django.http import HttpResponse
from django.db.models import Avg, Count, Min, Sum
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count
from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers


#from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models.functions import (ExtractDay, ExtractMonth, ExtractQuarter, ExtractWeek,ExtractWeekDay, ExtractIsoYear, ExtractYear )
from django.views import generic

from django.core.mail import send_mail
from django.conf import settings


#DataFlair

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'book/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'book/profile.html')

@login_required
def home(request):
    upload = ReceivedCreate()
    if 'Received' in request.POST:
        #if request.method == 'POST':
            upload = ReceivedCreate(request.POST, request.FILES)
            if upload.is_valid():
                upload = upload.save(commit=False)
                upload.author= request.user
                upload.save()
                return redirect('home')
                #return render(request, 'book/upload_form.html', {'upload_form':upload})
            else:
                return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    elif 'Spent' in request.POST:
        #if request.method == 'POST':
            upload = SpentCreate(request.POST, request.FILES)
            if upload.is_valid():
                upload = upload.save(commit=False)
                upload.author= request.user
                upload.save()
                return redirect('home')
                #return render(request, 'book/upload_form.html', {'upload_form':upload})
            else:
                return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        data = Received.objects.filter( date=datetime.date.today(), author=request.user).values('date').annotate(Sum('amount'))
        return render(request, 'book/home.html', {'upload_form':upload ,'data':data})


@login_required
def getdata(request):
    upload = ReceivedCreate()
    data = Received.objects.filter(date=datetime.date.today(), author=request.user)
    return render(request, 'book/out.html', {'upload_form':upload,'data': data})

@login_required
def getspentdata(request):
    upload = ReceivedCreate()
    data = Spent.objects.filter(date=datetime.date.today(), author=request.user)
    return render(request, 'book/out.html', {'upload_form':upload,'data': data})

@login_required
def sum(request):
    today = datetime.date.today()
    data = Received.objects.filter(date__year=today.year,author=request.user,date__month=today.month).values('date').order_by('-date').annotate(Sum('amount'))
    #data_month=Received.objects.filter(author=request.user,date__year=today.year).annotate(month=ExtractMonth ('date')).values('month').annotate(Sum('amount'))
    data_day=Received.objects.filter(date__year=today.year,date=datetime.date.today(), author=request.user)
    data_year=Received.objects.annotate(year=ExtractYear ('date')).values('year').annotate(Sum('amount'))
    data_mt=Received.objects.filter(author=request.user,date__year=today.year).annotate(month=ExtractMonth ('date')).values('month').annotate(Sum('amount'))
    return render(request, 'book/agg.html', {'data': data, 'data_month':data_mt, 'data_day':data_day, 'data_year':data_year})


@login_required
def sumspent(request):
    today = datetime.date.today()
    data = Spent.objects.filter(author=request.user,date__month=today.month).values('date').order_by('-date').annotate(Sum('amount'))
    data_month=Spent.objects.annotate(month=ExtractMonth ('date')).values('month').annotate(Sum('amount'))
    data_day = Spent.objects.filter(date=datetime.date.today(), author=request.user)
    data_year = Spent.objects.annotate(year=ExtractYear('date')).values('year').annotate(Sum('amount'))
    data_mt = Spent.objects.filter(author=request.user,date__year=today.year).annotate(month=ExtractMonth ('date')).values('month').annotate(Sum('amount'))
    return render(request, 'book/agg.html', {'data': data,'data_month':data_mt,'data_day':data_day, 'data_year':data_year})


@login_required
def update_book(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Received.objects.get(id = book_id)
    except Received.DoesNotExist:
        return redirect('get_data')
    book_form = ReceivedCreate(request.POST or None, instance = book_sel)
    if book_form.is_valid():
       book_form.save()
       return redirect('get_data')
    return render(request, 'book/upload_form.html', {'upload_form':book_form})


@login_required
def delete_book(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Received.objects.get(id = book_id)
    except Received.DoesNotExist:
        return redirect('home')
    book_sel.delete()
    return redirect('get_data')

@login_required
def update_spent(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Spent.objects.get(id = book_id)
    except Spent.DoesNotExist:
        return redirect('get_data_spent')
    book_form = SpentCreate(request.POST or None, instance = book_sel)
    if book_form.is_valid():
       book_form.save()
       return redirect('get_data_spent')
    return render(request, 'book/upload_form.html', {'upload_form':book_form})

@login_required
def delete_spent(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Spent.objects.get(id = book_id)
    except Spent.DoesNotExist:
        return redirect('get_data_spent')
    book_sel.delete()
    return redirect('get_data_spent')

@login_required
def getdata_e(request,date):
    date_time_obj = datetime.datetime.strptime(str(date), '%Y%m%d')
    #data = Received.objects.filter(date=date_time_obj.date(), author=request.user)
    #return render(request, 'book/out.html', {'data': data})

    today = datetime.date.today()
    data_day = Received.objects.filter(date=date_time_obj.date(), author=request.user)
    data = Received.objects.filter(date__year=today.year,author=request.user,date__month=today.month).values('date').order_by('-date').annotate(Sum('amount'))
    #data_month=Received.objects.filter(author=request.user,date__year=today.year).annotate(month=ExtractMonth ('date')).values('month').annotate(Sum('amount'))
    #data_day=Received.objects.filter(date__year=today.year,date=datetime.date.today(), author=request.user)
    data_year=Received.objects.annotate(year=ExtractYear ('date')).values('year').annotate(Sum('amount'))
    data_mt=Received.objects.filter(author=request.user,date__year=today.year).annotate(month=ExtractMonth ('date')).values('month').annotate(Sum('amount'))
    return render(request, 'book/agg.html', {'data': data, 'data_month':data_mt, 'data_day':data_day, 'data_year':data_year})



@login_required
def getdata_s(request,date):
    date_time_obj = datetime.datetime.strptime(str(date), '%Y%m%d')
    data = Spent.objects.filter(date=date_time_obj.date(), author=request.user)
    return render(request, 'book/out.html', {'data': data})
@login_required
def sum_update_book(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Received.objects.get(id = book_id)
    except Received.DoesNotExist:
        return redirect('get_data')
    book_form = ReceivedCreate(request.POST or None, instance = book_sel)
    if book_form.is_valid():
       book_form.save()
       return redirect('get_sum')
    return render(request, 'book/upload_form.html', {'upload_form':book_form})

@login_required
def sum_update_spent(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Spent.objects.get(id = book_id)
    except Spent.DoesNotExist:
        return redirect('get_data')
    book_form = SpentCreate(request.POST or None, instance = book_sel)
    if book_form.is_valid():
       book_form.save()
       return redirect('get_sum_spent')
    return render(request, 'book/upload_form.html', {'upload_form':book_form})
@login_required
def Createjob(request):
    data = worktrackCreate()
    if request.method == 'POST':
        data = worktrackCreate(request.POST, request.FILES)
        if data.is_valid():
            data = data.save(commit=False)
            data.Owner= request.user
            data.save()
            return redirect('worktrack')

        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        #data = worktrack.objects.all()
        return render(request, 'book/create_job.html', {'data':data})

@login_required
def work_track(request):
    upload = worktrackCreate()
    if 'search' in request.GET and request.GET['search']:

        search_term = request.GET.get('search')
        data = worktrack.objects.filter(Owner=request.user,Sno=search_term).annotate(Balance=F('Total_Amount')-F('Amount_Paid'))
        return render(request, 'book/work_track.html', {'data':data})

    elif 'Submit' in request.POST:
        #if request.method == 'POST':
            upload = worktrackCreate(request.POST, request.FILES)

            if upload.is_valid():
                upload = upload.save(commit=False)
                upload.Owner= request.user
                upload.save()
                return redirect('worktrack')
                #return render(request, 'book/work_track.html', {'upload_form':upload})
            else:
                return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    elif  'get_details' in request.GET :
            book_Sno=2
            book_Sno = int(book_Sno)
            try:
                book_sel = marriage.objects.get(Owner=request.user,Sno = book_Sno)
            except marriage.DoesNotExist:
                return redirect('marriage')
            data = worktrack.objects.filter(Owner=request.user).annotate(Balance=F('Total_Amount')-F('Amount_Paid'))
            return render(request, 'book/work_track.html', {'upload':upload,'book_sel':book_sel,'data':data})

    else:
        data = worktrack.objects.filter(Owner=request.user).annotate(Balance=F('Total_Amount')-F('Amount_Paid'))
        return render(request, 'book/work_track.html',{'upload':upload, 'data':data})


@login_required
def update_job(request, book_Sno):
    book_Sno = int(book_Sno)
    try:
        book_sel = worktrack.objects.get(Sno = book_Sno)
    except worktrack.DoesNotExist:
        return redirect('worktrack')
    data = worktrackCreate(request.POST or None, instance = book_sel)
    if data.is_valid():
       data.save()
       return redirect('worktrack')
    return render(request, 'book/create_job.html', {'data':data})

@login_required
def delete_job(request, book_Sno):
    book_Sno = int(book_Sno)
    try:
        book_sel = worktrack.objects.get(Sno = book_Sno)
    except worktrack.DoesNotExist:
        return redirect('worktrack')
    book_sel.delete()
    return redirect('worktrack')


@login_required
def mrg_track(request):
    upload = mrgtrackCreate()
    if request.method == 'POST':
        data = mrgtrackCreate(request.POST, request.FILES)
        if data.is_valid():
            data = data.save(commit=False)
            data.Owner= request.user
            data.save()
            return redirect('marriage')

        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'marriage'}}">reload</a>""")
    else:
                data = marriage.objects.filter(Owner=request.user)
                return render(request, 'book/Marriage.html', {'upload':upload, 'data':data})



@login_required
def update_marriage(request, Sno):
    book_Sno = int(Sno)
    try:
        book_sel = marriage.objects.get(Sno = book_Sno)
    except marriage.DoesNotExist:
        return redirect('marriage')
    data = mrgtrackCreate(request.POST or None , instance = book_sel)
    if data.is_valid():
       data.save()
       return redirect('marriage')
    return render(request, 'book/create_job.html', {'data':data})

@login_required
def delete_marriage(request, book_Sno):
    book_Sno = int(book_Sno)
    try:
        book_sel = marriage.objects.get(Sno = book_Sno)
    except marriage.DoesNotExist:
        return redirect('marriage')
    book_sel.delete()
    return redirect('marriage')

@login_required
def mrg_more_details(request, book_Sno):

    data = marriage.objects.filter(Owner=request.user, Sno=book_Sno)
    return render(request, 'book/mrge_more_details.html', {'data' : data})



@login_required
def pie_chart(request):
    labels = []
    data = []

    queryset = Received.objects.filter(author=request.user).values('name').annotate(amt=Sum('amount')).order_by('-amt')
    for i in queryset:
        labels.append(i[list(i.keys())[0]])
        data.append(i[list(i.keys())[1]])

    return render(request, 'reports/pie.html', {
        'labels': labels,
        'data': data,
    })
@login_required
def pie_chart_spent(request):
    labels = []
    data = []

    queryset = Spent.objects.filter(author=request.user).values('name').annotate(amt=Sum('amount')).order_by('-amt')
    for i in queryset:
        labels.append(i[list(i.keys())[0]])
        data.append(i[list(i.keys())[1]])

    return render(request, 'reports/pie.html', {
        'labels': labels,
        'data': data,
    })

@login_required
def email(request):
    subject = 'Thank you for registering to our site'
    message = ' Hello james bond  , nice work .. keep it up '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['manoj7573@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('home')

##################################################################
##### ICE CREAM ##################################################
##################################################################

@login_required
def ic_product_list(request):
    upload = IC_Product_create()
    #data = IC_Product.objects.all()
    #return render(request, 'ic/product_info.html', {'upload_form':upload,'data': data})
    #data = worktrackCreate()
    if request.method == 'POST':
        data = IC_Product_create(request.POST, request.FILES)
        if data.is_valid():
            data = data.save(commit=False)
            data.author= request.user
            #upload.author = request.user
            data.save()
            return redirect('ic_product_list')

        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        data = IC_Product.objects.all()
        return render(request, 'ic/product_info.html', {'upload_form':upload,'data':data})


@login_required
def ic_expensive(request):
    upload = IC_Expensive_create()
    #data = IC_Product.objects.all()
    #return render(request, 'ic/product_info.html', {'upload_form':upload,'data': data})
    #data = worktrackCreate()
    if request.method == 'POST':
        data = IC_Expensive_create(request.POST, request.FILES)
        if data.is_valid():
            data = data.save(commit=False)
            data.author= request.user
            data.save()
            return redirect('ic_expensive')

        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        data = IC_Expensive.objects.all()
        return render(request, 'ic/ic_expensive.html', {'upload_form':upload,'data':data})

@login_required
def stock_purchase(request):
    upload = IC_Stock_purchased_create()
    #data = IC_Product.objects.all()
    #return render(request, 'ic/product_info.html', {'upload_form':upload,'data': data})
    #data = worktrackCreate()
    if request.method == 'POST':
        data = IC_Stock_purchased_create(request.POST, request.FILES)
        if data.is_valid():
            data = data.save(commit=False)
            data.author= request.user
            data.save()

            return redirect('stock_purchase')

        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        data = IC_Stock_purchased.objects.all().order_by('-date_purchase')
        prod_info = IC_Product.objects.all()
        return render(request, 'ic/stock_purchase.html', {'upload_form':upload,'data':data,'prod_info':prod_info})



@login_required
def ic_stock_left(request):
    upload = IC_Expensive_create()
    #data = IC_Product.objects.all()
    #return render(request, 'ic/product_info.html', {'upload_form':upload,'data': data})
    #data = worktrackCreate()

    data_bites = IC_Product.objects.values_list('No_items_in_box').filter(Product_name='Bites')
    #data_bar = IC_Product.objects.values_list('No_items_in_box').filter(Product_name='Bites')
    data_bar = IC_Stock_purchased.objects.values_list('quantity').filter(prod_name='1').select_related('data_bites')
    #data_bites = IC_Stock_purchased.objects.values_list('quantity').filter(quantity=5).distinct()
    return render(request, 'ic/stock_left.html', {'upload_form':upload,'data':data_bar,'data_bites':data_bites})

@login_required
def IC_Stock_sold_details(request):
    upload = IC_Stock_sold_create()
    if request.method == 'POST':
        data = IC_Stock_sold_create(request.POST, request.FILES)
        if data.is_valid():
            data = data.save(commit=False)
            data.author= request.user
            data.save()
            return redirect('IC_Stock_sold_details')

        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        data = IC_Stock_sold.objects.all().filter( date_sold=datetime.date.today(),author=request.user).order_by('-date_sold')
        #prod = IC_Product.objects.all()
        #today = datetime.date.today()
        #date_time_obj = datetime.datetime.strptime(str(date), '%Y%m%d')
        #data_day = IC_Stock_sold.objects.filter(date_sold=date_time_obj.date(), author=request.user)
        #a = IC_Stock_sold.objects.filter(prod__prod_name='Bites')
        #psobjs = IC_Product.objects.filter(Product_name='Bites').values('Market_price')
        #print(psobjs.query)
        #queryset = IC_Stock_sold.objects.filter(prod_name__in=psobjs.values('Product_name')).values('prod_name')
        #print(queryset.query)
        #queryset1 = IC_Stock_view.objects.all().values()
        #print(queryset1.query)
        return render(request, 'ic/ic_sales.html', {'upload_form':upload,'data':data})
