from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='home'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('product/<int:myid>/', views.detail, name='detail'),
    path('<int:myid>/', views.detail, name='detail_legacy'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/', views.confimation, name='confirmation'),
    path('facture/<str:order_number>/', views.order_invoice, name='order_invoice'),
    path('suivi-commande/', views.order_tracking, name='order_tracking'),
    path('favoris/', views.wishlist_view, name='wishlist'),
    path('favoris/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('api/search/', views.live_search_api, name='live_search_api'),
    path('inscription/', views.register_view, name='register'),
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('mon-compte/', views.profile_view, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('a-propos/', views.about, name='about'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
