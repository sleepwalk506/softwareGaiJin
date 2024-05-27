from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List

def new_list(request):
    list_user = List.objects.create()
    Item.objects.create(text=request.POST['item_text'],list =list_user)
    # return redirect('/lists/the-new-page/')
    return redirect(f'/lists/{list_user.id}/')


def view_list(request,list_id):
    list_user = List.objects.get(id=list_id)
    # items = Item.objects.all()
    # items = Item.objects.filter(list=list_user)
    # return render(request,'home.html',{'items':items})
    # return render(request,'list.html',{'items':items})
    return render(request,'list.html',{'list':list_user})

def add_item(request,list_id):
    list_user = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'],list=list_user)
    return redirect(f'/lists/{list_user.id}/')


def home_page(request):
    # return HttpResponse('<html><title>To-Do lists</title></html>')
    # return render(request,'home.html')

    # if request.method == 'post':
    #     return HttpResponse(request.POST['item_text'])
    # return render(request,'home.html')

    # item = Item()
    # item.text = request.POST.get('item_text','')
    # item.save()

    # if request.method == 'POST':
    #     new_item_text = request.POST['item_text']
    #     Item.objects.create(text=new_item_text)
    # else:
    #     new_item_text = ''
    # return render(request,'home.html',{'new_item_text':new_item_text})

    # return render(request,'home.html',{'new_item_text':request.POST.get('item_text','')})

    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     # return redirect('/')
    #     return redirect('/lists/the-new-page/')
    
    # items = Item.objects.all()
    # return render(request,'home.html')
    # return render(request,'home.html',{'items':items})

    return render(request,'home.html')
    
# Create your views here.
