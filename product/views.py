from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from taggit.models import Tag

from product.forms import UserForm, ProductCreationForm, CategoryCreationForm
from product.models import Product


@login_required(login_url='login')
def index(request):
    products = Product.objects.all()

    template = 'product/index.html'
    context = {
        "products": products,
        'common_tags': Product.tags.most_common()[:5]
    }
    return render(request, template, context)


def tag_filter(request, slug):
    context = {'products': Product.objects.filter(tags__slug=slug), 'current_tag': slug}
    return render(request, 'product/index.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'product/signup.html', {'form': form})


def loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.error(request, f'username or password is incorrect.')

    if request.user.is_authenticated:
        return redirect('todo:todo-list')
    form = AuthenticationForm()
    return render(request, 'product/login.html', {'form': form, })


def LogoutView(request):
    logout(request)
    return redirect('index')


def create_product(request):
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully")
            return redirect('/')
        else:
            return render(request, 'product/create_product.html', {'form': form})
    form = ProductCreationForm()
    tags = Tag.objects.all()
    return render(request, 'product/create_product.html', {'form': form, 'tags': tags})


def create_category(request):
    if request.method == 'POST':
        form = CategoryCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully')
            return redirect('/')
    else:
        form = CategoryCreationForm()
        return render(request, 'product/create_category.html', {'form': form})


def view_data(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(id=pk).values()
        product_data = Product.objects.get(id=pk)
        tags = [str(tag) for tag in product_data.tags.all()]
        img = product_data.image.url
        category = product_data.category.name
        return JsonResponse({'status': True, 'data': list(product), 'tags': tags, 'image': img, 'category': category})
    return JsonResponse({'status': False})


def delete_product(request, pk):
    if request.is_ajax():
        Product.objects.get(id=pk).delete()
        count = Product.objects.count()
        return JsonResponse({'status': True, 'id': pk, 'count': count})
    return JsonResponse({'status': False, 'id': pk})


def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            data = form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('/')

    else:
        form = ProductCreationForm(instance=product)
    return render(request, 'product/create_product.html', {'form': form})
