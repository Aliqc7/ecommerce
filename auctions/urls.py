from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name = "create_listing"),
    path("listing/<int:listing_id>", views.show_listing, name = "show_listing"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("place_bid/<int:listing_id>", views.place_bid, name = "place_bid")
]
