from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import BlogCodeRecipe
from .forms import BlogCodeRecipeForm
from datetime import datetime
from django.db.models import OuterRef, Subquery


@staff_member_required
def custom_admin_view(request):
    newsletters = list(
        BlogCodeRecipe.objects.filter(published_date=datetime.today().date()).filter(
            version=Subquery(
                BlogCodeRecipe.objects.filter(
                    user_id=OuterRef("user_id"),
                    published_date=OuterRef("published_date"),
                )
                .values("version")
                .order_by("-version")[:1]
            )
        )
    )
    print(newsletters)
    if request.method == "POST":
        form = BlogCodeRecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_blog_code_recipe_view")
        return redirect("admin_blog_code_recipe_view")
    else:
        forms = []
        for n in newsletters:
            forms.append(BlogCodeRecipeForm(instance=n))

        context = {"forms": forms}
        return render(request, "admin/blog_code_recipe.html", context)
