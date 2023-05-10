from django.shortcuts import render, redirect
from .models import Restaurant, Rating
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .forms import RatingForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import ScrapedRestaurant
from django.db.models.expressions import RawSQL
from .forms import SearchForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SortRestaurantsForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Ajoutez d'autres importations si nécessaire


def index(request):
    
    form = SortRestaurantsForm(request.GET)
    sort_by = request.GET.get('sort_by', '')
    restaurants = ScrapedRestaurant.objects.all()

    if sort_by:
        restaurants = restaurants.order_by(sort_by)

    if form.is_valid():
        sort_by = form.cleaned_data['sort_by'] or '-rating'
    else:
        sort_by = '-rating'
        
    scraped_restaurants = ScrapedRestaurant.objects.order_by(sort_by)
    search_query = request.GET.get('search', '')
    order = request.GET.get('order', 'desc')
    scraped_restaurants = scraped_restaurants.annotate(
        rating_decimal=RawSQL("CAST(rating AS DECIMAL(4, 2))", ())
    )
    if order == 'asc':
        scraped_restaurants = scraped_restaurants.order_by('rating_decimal')
    else:
        scraped_restaurants = scraped_restaurants.order_by('-rating_decimal')
    
    if search_query:
            scraped_restaurants = scraped_restaurants.filter(restaurantname__icontains=search_query)

    form = SearchForm(request.GET)
    context = {'scraped_restaurants': scraped_restaurants, 'form': form}
    return render(request, 'restaurants/index.html', context)


def search(request):
    query = request.GET.get('q', '')
    restaurants = Restaurant.objects.filter(
        Q(restaurantname__icontains=query) | Q(location__icontains=query) 
    )
    return render(request, 'restaurants/search.html', {'restaurants': restaurants})


def user_profile(request, user_id):
    # Logique pour la page de profil utilisateur
    pass

def manage_account(request):
    # Logique pour la page de gestion de compte
    pass

def rate_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.restaurant = restaurant
            rating.save()
            return HttpResponseRedirect(reverse('restaurants:restaurant_detail', args=(restaurant.id,)))
        else:
            form = RatingForm()

        return render(request, 'restaurants/rate_restaurant.html', {'form': form, 'restaurant': restaurant})






def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = 'Identifiants invalides. Veuillez réessayer.'
    else:
        message = ''

    return render(request, 'registration/login.html', {'message': message})



def signup(request):
    if request.method == 'POST':
        # Récupérer les données soumises dans le formulaire
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Vérifier si les deux mots de passe sont identiques
        if password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('sign_up')
        
        # Créer un nouvel utilisateur
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            messages.success(request, "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('login')
        except Exception as e:
            messages.error(request, "Une erreur s'est produite lors de la création de votre compte. Veuillez réessayer.")
            return redirect('sign_up')
    else:
        return render(request, 'registration/sign_up.html')
    
    
def log_out(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def submit_rating(request):
    if request.method == "POST":
        # Get the submitted data
        restaurant_id = request.POST.get("restaurant_id")
        rating = request.POST.get("rating")
        user = request.user

        # Create a new Rating object for the user and restaurant
        user_rating, created = Rating.objects.get_or_create(user=user, restaurant_id=restaurant_id)
        user_rating.rating = rating
        user_rating.save()

        # Update the restaurant's average rating
        restaurant = Restaurant.objects.get(id=restaurant_id)
        average_rating = Rating.objects.filter(restaurant=restaurant).aggregate(Avg('rating'))['rating__avg']
        restaurant.rating = average_rating
        restaurant.save()

        # Get the new number of ratings
        new_num_of_ratings = Rating.objects.filter(restaurant=restaurant).count()

        return JsonResponse({"status": "success", "new_avg_rating": average_rating, "new_num_of_ratings": new_num_of_ratings})

    return JsonResponse({"status": "error"})