from django.shortcuts import render, redirect
from .models import  *
from .forms import *
from django.http import HttpResponse
from django.db.models import Avg, Count, Min, Sum
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count

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

#def index(request):
#    return render(request, 'book/library.html', {})

@login_required
def getdata(request):
    upload = ReceivedCreate()
    data = Received.objects.filter(date=datetime.date.today(), author=request.user)
    return render(request, 'book/out.html', {'upload_form':upload,'data': data})
@login_required
def getdata_e(request,date):
    date_time_obj = datetime.datetime.strptime(str(date), '%Y%m%d')
    data = Received.objects.filter(date=date_time_obj.date(), author=request.user)
    return render(request, 'book/out.html', {'data': data})

@login_required
def getspentdata(request):
    upload = ReceivedCreate()
    data = Spent.objects.filter(date=datetime.date.today(), author=request.user)
    return render(request, 'book/out.html', {'upload_form':upload,'data': data})

@login_required
def sum(request):
    today = datetime.date.today()
    data = Received.objects.filter(author=request.user,date__month=today.month).values('date').order_by('-date').annotate(Sum('amount'))
    data_month=Received.objects.annotate(month=ExtractMonth ('date')).values('month').annotate(Sum('amount'))
    data_day=Received.objects.filter(date=datetime.date.today(), author=request.user)
    data_year=Received.objects.annotate(year=ExtractYear ('date')).values('year').annotate(Sum('amount'))
    return render(request, 'book/agg.html', {'data': data, 'data_month':data_month, 'data_day':data_day, 'data_year':data_year})

#@login_required
#def month_received(request):
#    data=Received.objects.annotate(month=ExtractMonth ('date')).values('month').annotate(Sum('amount'))
#    #shelf1 = Received.objects.filter(author=request.user).values('date').annotate(Sum('amount'))
#    return render(request, 'book/month_sum.html', {'data': data})

@login_required
def sumspent(request):
    data = Spent.objects.filter(author=request.user).values('date').order_by('-date').annotate(Sum('amount'))
    data_month=Spent.objects.annotate(month=ExtractMonth ('date')).values('month').annotate(Sum('amount'))
    return render(request, 'book/agg.html', {'data': data,'data_month':data_month})

@login_required
def upload(request):
    upload = ReceivedCreate()
    if request.method == 'POST':
        upload = ReceivedCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload = upload.save(commit=False)
            upload.author= request.user
            upload.save()
            return redirect('home')
            #return render(request, 'book/upload_form.html', {'upload_form':upload})
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'book/upload_form.html', {'upload_form':upload})


@login_required
def upload_spent(request):
    upload = SpentCreate()
    if request.method == 'POST':
        upload = SpentCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload = upload.save(commit=False)
            upload.author= request.user
            upload.save()
            return redirect('get_data_spent')
            #return render(request, 'book/upload_form.html', {'upload_form':upload})
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'book/upload_form.html', {'upload_form':upload})


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
#def work_track(request):
#    shelf = worktrack.objects.all()
#    return render(request, 'book/work_track.html', {'shelf' : shelf})

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
def hotel_image_view(request):
    form_img = HotelForm()
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    elif request.method == 'GET':
        data = Hotel.objects.all()
        return render(request, 'book/image.html', {'data' : data,'form_img':form_img})
        #return render((request, 'display_hotel_images.html',   {'form' : form}))

    else:
        form = HotelForm()
        return render(request, 'book/image.html', {'form' : form})

@login_required
def success(request):
    return HttpResponse('successfully uploaded')

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

def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['manoj7573@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('home')