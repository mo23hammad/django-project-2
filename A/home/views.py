from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.contrib import messages
from .models import Product,Category
from . import tasks
from .forms import FileUploadForm
from utils import IsUserAdminMixin
from orders.forms import AddCartForm



class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self,request,slug):
        product = get_object_or_404(Product,slug = slug)
        form = AddCartForm()
        return render(request,'home/detail.html',{'product':product,'form':form})
    
class BucketHomeView(IsUserAdminMixin,View):
    template_name = 'home/bucket.html'

    def get(self,request):
        objects = tasks.all_bucket_object_task()
        return render(request,self.template_name,{'objects':objects})

class DeleteBucketObjectView(IsUserAdminMixin,View):

    def get(self,request,key):
        tasks.delete_object_task.delay(key)
        messages.success(request,'Your object will delete very soon.','info')
        return redirect('home:bucket')

class DownloadBucketObjectView(IsUserAdminMixin,View):

    def get(self,request,key):
        tasks.download_object_task.delay(key)
        messages.success(request,'Your object will download very soon.','info')
        return redirect('home:bucket')


class UploadBucketObjectView(IsUserAdminMixin,View):
    form_class = FileUploadForm
    template_name = 'home/upload.html'
    success_url = 'home:bucket'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            tasks.upload_object_task.delay(uploaded_file, uploaded_file.name)
            messages.success(request,'your file will upload soon.','success')
            return redirect(self.success_url)
        messages.error(request,'your file is not valid.','danger')
        return render(request, self.template_name, {'form': form})


    




