from django.shortcuts import redirect, render, get_object_or_404
from .models import Products
from .forms import ProductsForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST


def index(request):
    return render(request, "products/index.html")


def products(request):
    Product = Products.objects.all().order_by("-pk")
    context = {
        "Products": Product,
    }
    return render(request, "products/products.html", context)


# 상품 등록 ------------------------------------------------------------------------------


@login_required
def create(request):
    if request.method == "POST":
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            products = form.save(commit=False)
            products.author = request.user
            products.save()
            return redirect("products:products_detail", products.pk)
    else:
        form = ProductsForm()

    context = {"form": form}
    return render(request, "products/create.html", context)


# 상품 상세 정보 ------------------------------------------------------------------------------

def products_detail(request, pk):
    Product = get_object_or_404(Products, pk=pk)
    comment_form = CommentForm()
    comments = Product.comments.all().order_by("-pk")
    context = {
        "Product": Product,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "products/products_detail.html", context)


# 상품 삭제 및 수정------------------------------------------------------------------------------


@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    Product = get_object_or_404(Products, pk=pk)
    if Product.author == request.user:
        if request.method == "POST":
            form = ProductsForm(request.POST, instance=Product)
            if form.is_valid():
                Product = form.save()
                return redirect("products:products_detail", Product.pk)
        else:
            form = ProductsForm(instance=Product)
    else:
        return redirect("products:products")

    context = {
        "form": form,
        "Product": Product,
    }
    return render(request, "products/update.html", context)


@require_POST
def delete(request, pk):
    Product = get_object_or_404(Products, pk=pk)
    if Product.author == request.user:
        Product.delete()
    return redirect("products:products")


# 찜하기(좋아요)------------------------------------------------------------------------------


@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        Product = get_object_or_404(Products, pk=pk)
        if Product.like_users.filter(pk=request.user.pk).exists():
            Product.like_users.remove(request.user)  # 좋아요 취소
        else:
            Product.like_users.add(request.user)  # 좋아요
        return redirect("products:products")
    return redirect("accounts:login")


