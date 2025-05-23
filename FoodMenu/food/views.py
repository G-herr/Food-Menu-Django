from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

# Create your views here.

class IndexClassView(ListView):
    model = Item
    template_name = 'food/index.html'
    context_object_name = 'item_list'
    
class FoodDetail(DetailView):
    model = Item
    template_name = 'food/detail.html'
    

def create_item(request):
    form = ItemForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request,'food/item-form.html',{'form':form, 'form_type': 'create'})

class CreateItem(CreateView):
    model = Item
    fields = ['item_name', 'item_desc', 'item_price', 'item_image']
    template_name = 'food/item-form.html'
    
    def form_valid(self,form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

def update_item(request,id):
    item = Item.objects.get(id = id)
    form = ItemForm(request.POST or None, instance= item)
    
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request,'food/item-form.html',{'form':form, 'item':item, 'form_type': 'update'} )
    
def delete_item(request,id):
    item = Item.objects.get(id=id)
    
    if request.method == 'POST':
        item.delete()
        return redirect('index')
    return render(request,'food/item-delete.html',{'item':item})