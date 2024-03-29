from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    listings = Listing.objects.filter(is_active = True).all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def closed_auctions(request):
    listings = Listing.objects.filter(is_active = False).all()
    return render(request, "auctions/closed_auctions.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        listing_user = request.user
        listing = Listing (title = title, description = description, \
                           starting_bid = starting_bid, current_price = starting_bid, image_url=image_url,\
                              category= category, listing_user = listing_user,\
                                is_active = True)
        listing.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, "auctions/create.html")

def show_listing(request, listing_id):
    listing = Listing.objects.get(pk= listing_id)
    comments = listing.comments.all()
    if request.user.is_authenticated:
        watch_items = request.user.watchlist.all()
        watchlist = [item.listing for item in watch_items]
    else:
        watchlist =[]
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments": comments
    })

@login_required
def watchlist(request, user_id):
    user = User.objects.get(pk = user_id)
    
    if request.method == "POST":
        action = int(request.POST["action"])
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk = listing_id)
        if action == 0:
            watch_item = Watchitem.objects.get(user = request.user, listing = listing)
            watch_item.delete()
        else:
            watch_item = Watchitem(user = user, listing = listing)
            watch_item.save()
        return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))

    return render(request, "auctions/watchlist.html", {
        "user": user,
        "watchlist": user.watchlist.all()
    })

def place_bid(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk = listing_id)
    bid_amount = int(request.POST["bid_amount"])
    if (listing.bid is None and bid_amount >= listing.starting_bid) or (bid_amount > listing.current_price):
        bid = Bid(listing = listing, bidder = user, amount = bid_amount)
        bid.save()
        listing.current_price = bid_amount
        listing.bid = bid
        listing.save()
        message = "Your bid is successfully placed!"
    else:
        message = "Your bid is too low!"
        
    return render (request, "auctions/listing.html", {
        "listing": listing,
        "message": message
    })

@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    listing.is_active = False
    listing.save()
    bid = listing.bid
    if bid:
        bidder = bid.bidder
        listing.winner = bidder
        listing.save()
    
    return HttpResponseRedirect(reverse('show_listing', args=(listing_id, )))

@login_required
def add_comment(request, listing_id):

    listing = Listing.objects.get(pk = listing_id)
    user = request.user
    comment_content = request.POST["comment_content"]

    comment = Comment.objects.create(user = user, listing = listing, text = comment_content)
    comment.save()

    return HttpResponseRedirect(reverse('show_listing', args=(listing_id, )))

def categories(request):
    listings = Listing.objects.all()
    categories = [item.category for item in listings]

    return render (request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    listings = Listing.objects.filter(category = category, is_active = True)
    return render(request, "auctions/category.html", { 
        "listings": listings,
        "category": category
    })