from dataclasses import fields
from unittest import result
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView
from .models import Meal
from .forms import DetailForm
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import Avg
from django.http import JsonResponse, HttpResponseServerError


class IndexView(CreateView):
    template_name = 'index.html'
    model = Meal
    fields = ('name', 'description', 'imageUrl',
              'countryOfOrigin', 'typicalMealTime')
    success_url = reverse_lazy('mealsite:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["topRated"] = Meal.objects.annotate(avg_rating=Avg(
            "mealrating__rating")).filter(avg_rating__gte=3.5)[0:3]

        context["recentlyAdded"] = Meal.objects.all().order_by(
            '-dateAdded')[0:3]

        return context


class CategoryListView(ListView):
    template_name: str = 'mealsite/list.html'
    model = Meal

    def get_queryset(self):
        queryset = ''
        
        category = self.kwargs['category']
        hash = {1: 'morning', 2: 'afternoon', 3: 'evening'}

        list_of_key = list(hash.keys())
        list_of_value = list(hash.values())

        if category in list_of_value:
            position = list_of_key[list_of_value.index(category)]
            queryset = Meal.objects.all().filter(typicalMealTime=position)

        elif category == 'toprate':
            queryset = queryset.annotate(avg_rating=Avg(
                "mealrating__rating")).filter(avg_rating__gte=3.5)

        elif category == 'recently':
            queryset = Meal.objects.all().order_by('-dateAdded')

        else:
            raise Http404("Question does not exist")

        # クエリパラメータ取得
        param_value = self.request.GET.get(
            "sort") if self.request.GET.get("sort") else ''

        if param_value == 'rate':
            queryset = queryset.annotate(avg_rating=Avg(
                "mealrating__rating")).order_by('-avg_rating')

        elif param_value == 'country':
            queryset = queryset.order_by('-countryOfOrigin')

        elif param_value == 'data':
            queryset = queryset.order_by('-dateAdded')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['category'].upper()
        context['category'] = self.kwargs['category']
        return context


class MealDetail(DetailView):
    template_name: str = 'mealsite/detail.html'
    model = Meal
    context_object_name = "meal"


def meal_detail_axios(request, pk):
    if request.method == "GET":
        meal = Meal.objects.get(id=pk)
        results = []

        results.append(
            {
                "totalRating": meal.totalRating(),
                "votes": meal.numberOfVotes(),
            }
        )
        return JsonResponse(results, safe=False)

    if request.method == "POST":
        form = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.meal_id = pk
            rating.save()
            form.save_m2m()
            return JsonResponse({"status": 'Success'})
        else:
            return HttpResponseServerError()
