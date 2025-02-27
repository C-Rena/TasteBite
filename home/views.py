from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User_Recipe
from .forms import RecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home_page(request):
    return render(request,"home.html")


def about_page(request):
    return render(request,"about.html")


def profile_page(request):
    user = request.user 
    return render(request, 'profile.html', {'user': user})


@login_required(login_url="account:login")
def recipes_page(request):
    keyword = request.GET.get("keyword")  # GET ile alınıyor
    if keyword:
        try:
            # Recipe'yi ada göre bul ve detay sayfasına yönlendir
            recipe = User_Recipe.objects.get(recipe_name__iexact=keyword)  # Tam eşleşme arama
            return redirect('recipe_detail', id=recipe.id)
        except User_Recipe.DoesNotExist:
            # Recipe bulunamazsa tüm tarifleri listele
            recipes = User_Recipe.objects.all()
            return render(request, "recipes.html", {"recipes": recipes})

    # Eğer arama yapılmadıysa tüm tarifleri listele
    recipes = User_Recipe.objects.all()
    return render(request, "recipes.html", {"recipes": recipes})


@login_required(login_url="account:login")
def my_recipes_page(request):
    recipes = User_Recipe.objects.filter(recipe_owner=request.user)
    return render(request, "my_recipes.html", {"recipes": recipes})



def add_recipe_page(request):
    form=RecipeForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        recipe=form.save(commit=False)
        recipe.recipe_owner=request.user
        recipe.save()
        messages.success(request,"Your recipe has been added with luck...")
        return redirect("my_recipes")

    context={"form":form}
    return render(request,"add_recipe.html",context)


def recipe_detail_page(request, id):
    recipe=get_object_or_404(User_Recipe,id=id)
    context = {"recipe": recipe}
    return render(request, "recipe_detail.html", context)


def update_recipe_page(request,id):
    recipe=get_object_or_404(User_Recipe,id=id)
    form=RecipeForm(request.POST or None,request.FILES or None,instance=recipe)
    if form.is_valid():
        recipe=form.save(commit=False)
        recipe.recipe_owner=request.user
        recipe.save()
        messages.success(request,"Your article has been successfully updated...")
        return redirect("my_recipes")

    context={"form":form}
    return render(request,"update.html",context)


def delete_recipe_page(request,id):
    recipe=get_object_or_404(User_Recipe,id=id)
    recipe.delete()
    messages.success(request,"Your recipe has been delete with luck...")
    return redirect("my_recipes")
    
