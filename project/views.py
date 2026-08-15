from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from django.core.paginator import Paginator
from slugify import slugify
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

def about(request):
    info = About.get_solo()          # было: About.objects.all()
    return render(request, 'project/about.html', {'info': info})

def header(request):
    return render(request, 'head.html')

def gallery(request, tag_slug):
    category = get_object_or_404(
        GalleryCategory,
        slug=tag_slug,
        is_active=True
    )

    gallery = Gallery.objects.filter(
        category=category,
        is_active=True
    ).prefetch_related('images')

    return render(request, 'project/gallery.html', {
        'category': category,
        'gallery': gallery,
    })

class search(TemplateView):
    template_name = 'project/homePage.html'
    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')
        base = Base.objects.filter(slug__icontains=slugify(query))

        paginator = Paginator(base, 16)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        category = GalleryCategory.objects.all()

        context['categoryGal'] = category
        context['page_obj'] = page_obj
        context['HeroImage'] = 0
        context['case'] = 'search'
        context['is_empty'] = not base.exists()
        context['filter'] = 0
        context['q'] = query

        return context

class save(TemplateView):
    template_name = 'project/homePage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            my_cookie = self.request.COOKIES.get('BOX').split('%2C')
        except:
            my_cookie = []
        base = Base.objects.filter(slug__in=my_cookie)

        paginator = Paginator(base, 16)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        category = GalleryCategory.objects.all()

        context['categoryGal'] = category
        context['page_obj'] = page_obj
        context['HeroImage'] = 0
        context['filter'] = 0
        context['case'] = 'save'
        context['is_empty'] = not base.exists()

        return context

class category(TemplateView):
    template_name = 'project/homePage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')

        info = About.get_solo()

        filter = Filter.objects.all()
        base = Base.objects.filter(category__slugfilter=tag_slug)
        category_obj = get_object_or_404(Filter, slugfilter=tag_slug)
        title = category_obj.title

        paginator = Paginator(base, 16)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        category = GalleryCategory.objects.all()

        context['categoryGal'] = category
        context['page_obj'] = page_obj
        context['filter'] = filter
        context['HeroImage'] = 0
        context['case'] = 'category'
        context['title'] = title
        context['info'] = info
        
        return context


class mainHome(TemplateView):
    template_name = 'project/homePage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = Base.objects.filter(is_published=True)
        info = About.get_solo()      # было: About.objects.all()

        paginator = Paginator(base, 16)
        page_number = self.request.GET.get('page')
        category = GalleryCategory.objects.all()

        context['categoryGal'] = category
        page_obj = paginator.get_page(page_number)
        context['filter'] = Filter.objects.all()
        context['page_obj'] = page_obj
        context['HeroImage'] = 1
        context['case'] = 'catalog'
        context['info'] = info

        return context

class card(TemplateView):
    template_name = 'project/card.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base = Base.objects.filter(slug=self.kwargs['tag_slug'])
        context['base'] = base
        context['filter'] = 0

        return context


@csrf_exempt
def update_model(request):
    if request.method == 'POST':
        new_data = request.POST.get('new_data')
        print('Correct')
        return JsonResponse({'status': 'success', 'message': 'Model updated successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})