from django.shortcuts import render
from django.http import HttpResponse
from lists.models import Item

def home_page(request):
    # return HttpResponse('<html><title>To-Do lists</title></html>')
    # return render(request,'home.html')

    # if request.method == 'post':
    #     return HttpResponse(request.POST['item_text'])
    # return render(request,'home.html')

    item = Item()
    item.text = request.POST.get('item_text','')
    item.save()

    return render(request,'home.html',{'new_item_text':request.POST.get('item_text','')})
# Create your views here.
