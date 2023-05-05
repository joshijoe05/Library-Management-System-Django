from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import BooksForm
from .models import Book
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect,csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    if request.method=='GET' and 'submit' in request.GET:
        select = request.GET.get('select')
        search = request.GET.get('search')
        print(select)
        if select == 'title':
            book = Book.objects.filter(title__icontains=search)
        elif select == 'author':
            print("author",select)
            book = Book.objects.filter(author__icontains=search)
        elif select == 'category':
            book = Book.objects.filter(category__icontains=search)
        p = Paginator(book,4)
        num = request.GET.get('page', 1)
        try:
            page = p.page(num)
        except EmptyPage:
            page = p.page(1)
        except PageNotAnInteger:
            page = p.page(1)
        context = {'books':page,'search':search,'num':num,'p':p,'bool':True}
    else:
        book = Book.objects.all()
        p = Paginator(book,4)
        num = request.GET.get('page', 1)
        try:
            page = p.page(num)
        except EmptyPage:
            page = p.page(1)
        except PageNotAnInteger:
            page = p.page(1)
        context = {
            'books' : page,
            'num' : num,
            'p':p,
            'bool':False,
        }
    return render(request,'index.html',context=context)

@csrf_protect
def add(request):
    form = BooksForm()
    if request.method=='POST':
        form = BooksForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,'Book added successfully !')
                return redirect('index')
            except ValidationError as e:
                messages.error(request,e.message)
    context = {'form':form}
    return render(request,'add.html',context=context)

@csrf_exempt
def edit(request,id):
    form = Book.objects.get(id=id)
    dic = {
        "form" : form,
        'id' : id,
        'date' : str(form.date)[::-1]
    }
    return render(request,'edit.html',dic)

@csrf_protect
def update(request,id):
    if request.method=='POST':
        form = Book(id=id)
        form.title = request.POST['title']
        form.author = request.POST['author']
        form.publisher = request.POST['publisher']
        form.date = request.POST['date']
        form.isbn = request.POST['isbn']
        form.category = request.POST['category']
        form.save()
        messages.success(request, "Book details updated.")
        return redirect('index')

@csrf_protect
def delete(request,id):
    book = Book(id=id)
    if request.method=='POST':
        book.delete()
        messages.warning(request, "Book details deleted. ")
    return redirect('index')