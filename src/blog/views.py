from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import BlogPostModelForm
from .models import BlogPost



# def blog_post_detail_page(request, slug):
	# print("DJANGO SAYS", request.method, request.path, request.user)
	# queryset = BlogPost.objects.filter(slug=slug)
	# if queryset.count() == 0:
	#	raise Http404
	# obj = queryset.first()
	# obj = get_object_or_404(BlogPost, slug=slug)
	# template_name = 'blog_post_detail.html'
	# context = {"object": obj}
	# return render(request, template_name, context)


def blog_post_list_view(request):
	# list out objects
	# could be search
	# now = timezone.now()
	qs = BlogPost.objects.all().published()
	if request.user.is_authenticated:
		my_qs = BlogPost.objects.filter(user=request.user)
		qs = (qs | my_qs).distinct()
	#qs = BlogPost.objects.all()  # queryset -> list of pyhton objects
	# qs = BlogPost.objects.filter(publish_date__lte=now)
	# qs = BlogPost.objects.filter(title__icontains='title') 
	template_name = 'blog/list.html'
	context = {"object_list": qs}
	return render(request, template_name, context)


@staff_member_required
# @login_required(login_url = '/login')
def blog_post_create_view(request):
	# request.user -> return something
	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		# print(form.cleaned_data)
		# title = form.cleaned_data['title']
		# obj = BlogPost.objects.create(**form.cleaned_data)
		# obj  = BlogPost.objects.create(title=title) sends it to a specific model (db)
		# obj2 = OtherModel.objects.create(title=title)
		# form.save()
		  obj = form.save(commit=False)
		  obj.user = request.user
		# obj.title = form.cleaned_data.get('title') + "0"
		  obj.save()
		  form = BlogPostModelForm()
	template_name = 'form.html'
	context = {'form': form}
	return render(request, template_name, context)


def blog_post_detail_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = 'blog/detail.html'
	context = {"object": obj}
	return render(request, template_name, context)


@staff_member_required
def blog_post_update_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	form = BlogPostModelForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
	template_name = 'form.html'
	context = {"title": f"Update {obj.title}", 'form': form}
	return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = 'blog/delete.html'
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	context = {"object": obj}
	return render(request, template_name, context)






