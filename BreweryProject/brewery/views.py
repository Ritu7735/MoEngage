import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from brewery.forms import BrewerySearchForm
from brewery.models import Brewery, Review


# Create your views here.
def home(request):
    return render(request,'index.html')


def login_page(request):
    return render(request,'login.html',{'data':''})


def login_user(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request,user)
        return render(request,'brewery.html')
    else:
        return render(request,'login.html',{'data': 'failed'})


def signup_page(request):
    return render(request,'signup.html')


def signup_user(request):
    email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    if User.objects.filter(username=username).exists():
        return render(request, 'signup.html',{'user_available':True})
    elif User.objects.filter(email=email).exists():
        return render(request,'signup.html',{'email_avilable':True})
    else:
        user = User.objects.create_user(email=email, password=password, username=username)
        user.save()
        return render(request,'login.html',{'data':''})


def go_to_home(request):
    return render(request,'brewery.html')


def search_breweries(request):
    city = request.GET.get('city', 'default_city')
    url = f"https://api.openbrewerydb.org/breweries?"
    response = requests.post(url)
    data = response.json()
    context = {
        'city': city,
        'data': data,
    }

    return render(request, 'search_breweries.html',context)


def homepage(request):
    form = BrewerySearchForm()
    results = []
    if request.method == 'POST' and 'query' in request.POST:
        form = BrewerySearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_type = form.cleaned_data['search_type']
            results = search_breweries(query, search_type)

    return render(request, 'home.html', {'form': form, 'results': results})


def add_review(request, brewery_id):
    brewery = Brewery.objects.get(api_id=brewery_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        review = Review(user=request.user, brewery=brewery, rating=rating, comment=comment)
        review.save()
        return redirect('home')
    return render(request, 'add_review.html', {'brewery': brewery})


def brewery_detail(request,brewery_id):

    brewery = get_object_or_404(Brewery, api_id=brewery_id)
    reviews = brewery.review_set.all()
    return render(request, 'brewery_detail.html', {'brewery': brewery, 'reviews': reviews})


def search_results(request):
    form = BrewerySearchForm(request.GET)
    breweries = []
    if form.is_valid():
        city = form.cleaned_data['city']
        breweries = search_breweries(city)
        # Save breweries to the database
        for b in breweries:
            brewery, created = Brewery.objects.get_or_create(
                api_id=b['id'],
                defaults={
                    'name': b['name'],
                    'street': b.get('street'),
                    'city': b['city'],
                    'state': b['state'],
                    'postal_code': b.get('postal_code'),
                    'country': b.get('country'),
                    'phone': b.get('phone'),
                    'website_url': b.get('website_url'),
                    'brewery_type': b['brewery_type'],
                }
            )
    return render(request, 'search.html', {'form': form, 'breweries': breweries})
