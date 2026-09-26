from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Min, Max
from .models import Category, Product, ProductReview, Commande, ContactMessage, Newsletter, Wishlist
import json
import urllib.parse

def index(request):
    """Page d'accueil avec bannières, recherche, catégories populaires et produits mis en avant."""
    categories = Category.objects.all()
    products = Product.objects.all()
    featured_products = Product.objects.filter(is_featured=True)[:6]
    recent_products = Product.objects.all().order_by('-date_added')[:8]

    # Wishlist IDs for user
    wishlist_product_ids = get_user_wishlist_ids(request)

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'recent_products': recent_products,
        'wishlist_product_ids': wishlist_product_ids,
    }
    return render(request, 'shop/index.html', context)


def catalogue(request):
    """Page catalogue dédiée avec filtrage multi-critères et pagination."""
    categories = Category.objects.all()
    products = Product.objects.all()

    # Liste des marques disponibles
    brands = Product.objects.exclude(brand__isnull=True).exclude(brand__exact='').values_list('brand', flat=True).distinct()

    # Recherche
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    # Filtrage par catégorie
    category_slug = request.GET.get('category', '').strip()
    active_category = None
    if category_slug:
        active_category = Category.objects.filter(slug=category_slug).first()
        if active_category:
            products = products.filter(category=active_category)

    # Filtrage par marque
    selected_brand = request.GET.get('brand', '').strip()
    if selected_brand:
        products = products.filter(brand__iexact=selected_brand)

    # Filtrage par fourchette de prix
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Filtrage par note minimale
    min_rating = request.GET.get('rating')
    if min_rating:
        try:
            products = products.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    # En stock uniquement
    in_stock_only = request.GET.get('in_stock') == '1'
    if in_stock_only:
        products = products.filter(stock__gt=0)

    # Tri
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'popular':
        products = products.order_by('-is_featured', '-rating')
    else:
        products = products.order_by('-date_added')

    total_results = products.count()

    # Pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    wishlist_product_ids = get_user_wishlist_ids(request)

    context = {
        'products': page_obj,
        'categories': categories,
        'brands': sorted(brands),
        'active_category': active_category,
        'selected_brand': selected_brand,
        'search_query': search_query,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'min_rating': min_rating or '',
        'in_stock_only': in_stock_only,
        'sort_by': sort_by,
        'total_results': total_results,
        'wishlist_product_ids': wishlist_product_ids,
    }
    return render(request, 'shop/catalogue.html', context)


def detail(request, myid):
    """Page détaillée d'un produit avec avis, commande WhatsApp et articles suggérés."""
    product = get_object_or_404(Product, id=myid)
    reviews = product.reviews.all()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    # Message WhatsApp pré-rempli
    whatsapp_phone = "25779000000" # Numéro WhatsApp Janvier-Shop Burundi
    product_url = request.build_absolute_uri()
    whatsapp_text = f"Bonjour Janvier-Shop, je souhaite commander l'article : *{product.title}* au prix de *{int(product.price):,} BIF*.\nLien du produit : {product_url}"
    whatsapp_link = f"https://wa.me/{whatsapp_phone}?text={urllib.parse.quote(whatsapp_text)}"

    # Traitement de l'ajout d'avis client
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        rating_val = request.POST.get('rating', '5')
        comment = request.POST.get('comment', '').strip()

        if name and email and comment:
            try:
                rating = int(rating_val)
            except ValueError:
                rating = 5
            ProductReview.objects.create(
                product=product,
                name=name,
                email=email,
                rating=rating,
                comment=comment
            )
            # Recalcul de la note moyenne
            all_reviews = product.reviews.all()
            if all_reviews.exists():
                avg_rating = sum(r.rating for r in all_reviews) / all_reviews.count()
                product.rating = round(avg_rating, 1)
                product.save()

            messages.success(request, "Merci ! Votre avis a été publié avec succès.")
            return redirect('detail', myid=product.id)
        else:
            messages.error(request, "Veuillez renseigner tous les champs pour soumettre votre avis.")

    wishlist_product_ids = get_user_wishlist_ids(request)
    is_in_wishlist = product.id in wishlist_product_ids

    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'whatsapp_link': whatsapp_link,
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'shop/detail.html', context)


def checkout(request):
    """Page de validation de commande avec liaison compte utilisateur."""
    if request.method == "POST":
        items = request.POST.get('items', '')
        total = request.POST.get('total', '')
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        ville = request.POST.get('ville', '').strip()
        pays = request.POST.get('pays', '').strip()
        zipcode = request.POST.get('zipcode', '').strip()
        payment_method = request.POST.get('payment_method', 'COD')

        if not nom or not email or not address:
            messages.error(request, "Veuillez remplir les informations obligatoires (Nom, Email, Adresse).")
            return render(request, 'shop/checkout.html')

        commande = Commande(
            user=request.user if request.user.is_authenticated else None,
            items=items,
            total=total,
            nom=nom,
            email=email,
            phone=phone,
            address=address,
            ville=ville,
            pays=pays,
            zipcode=zipcode,
            payment_method=payment_method
        )
        commande.save()

        request.session['last_order_id'] = commande.id
        return redirect('confirmation')

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'nom': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }

    return render(request, 'shop/checkout.html', {'initial_data': initial_data})


def confimation(request):
    """Page de confirmation avec reçu et suivi."""
    order_id = request.session.get('last_order_id')
    commande = None
    items_list = []
    
    if order_id:
        try:
            commande = Commande.objects.get(id=order_id)
        except Commande.DoesNotExist:
            commande = Commande.objects.first()
    else:
        commande = Commande.objects.first()

    if commande and commande.items:
        try:
            parsed_items = json.loads(commande.items)
            for k, val in parsed_items.items():
                items_list.append({
                    'id': k,
                    'qty': val[0] if len(val) > 0 else 1,
                    'name': val[1] if len(val) > 1 else 'Article',
                    'price': val[2] if len(val) > 2 else 0,
                })
        except Exception:
            pass

    return render(request, 'shop/confirmation.html', {
        'commande': commande,
        'items_list': items_list,
        'name': commande.nom if commande else 'Client'
    })


def order_invoice(request, order_number):
    """Génération d'une facture / reçu proforma imprimable."""
    commande = get_object_or_404(Commande, order_number=order_number)
    items_list = []
    if commande.items:
        try:
            parsed = json.loads(commande.items)
            for k, val in parsed.items():
                items_list.append({
                    'id': k,
                    'qty': val[0] if len(val) > 0 else 1,
                    'name': val[1] if len(val) > 1 else 'Article',
                    'price': val[2] if len(val) > 2 else 0,
                    'total_price': (val[0] if len(val) > 0 else 1) * (val[2] if len(val) > 2 else 0)
                })
        except Exception:
            pass

    return render(request, 'shop/invoice.html', {
        'commande': commande,
        'items_list': items_list,
    })


def order_tracking(request):
    """Page de suivi de commande en temps réel."""
    searched_order = None
    order_query = request.GET.get('order_number', '').strip()
    
    if order_query:
        try:
            searched_order = Commande.objects.filter(
                Q(order_number__iexact=order_query) | Q(email__iexact=order_query)
            ).first()
            if not searched_order:
                messages.warning(request, f"Aucune commande trouvée pour la référence : {order_query}")
        except Exception:
            messages.error(request, "Une erreur est survenue lors de la recherche.")

    return render(request, 'shop/tracking.html', {
        'order': searched_order,
        'order_query': order_query
    })


# --- WISHLIST / FAVORIS ---

def get_user_wishlist_ids(request):
    """Récupère la liste des IDs des produits en favoris pour l'utilisateur ou la session."""
    if request.user.is_authenticated:
        return list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    else:
        if not request.session.session_key:
            request.session.create()
        session_wishlist = request.session.get('wishlist_ids', [])
        return session_wishlist


def wishlist_view(request):
    """Affichage de la page de favoris."""
    wishlist_ids = get_user_wishlist_ids(request)
    products = Product.objects.filter(id__in=wishlist_ids)
    return render(request, 'shop/wishlist.html', {
        'products': products,
        'wishlist_product_ids': wishlist_ids,
    })


def toggle_wishlist(request, product_id):
    """Ajouter ou retirer un produit des favoris (AJAX/POST)."""
    product = get_object_or_404(Product, id=product_id)
    added = False

    if request.user.is_authenticated:
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        if wishlist_item:
            wishlist_item.delete()
            added = False
        else:
            Wishlist.objects.create(user=request.user, product=product)
            added = True
        total_count = Wishlist.objects.filter(user=request.user).count()
    else:
        if not request.session.session_key:
            request.session.create()
        session_wishlist = request.session.get('wishlist_ids', [])
        if product_id in session_wishlist:
            session_wishlist.remove(product_id)
            added = False
        else:
            session_wishlist.append(product_id)
            added = True
        request.session['wishlist_ids'] = session_wishlist
        total_count = len(session_wishlist)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'success': True,
            'added': added,
            'total_count': total_count,
            'message': f"Produit {'ajouté aux' if added else 'retiré des'} favoris !"
        })

    messages.info(request, f"Produit {'ajouté aux' if added else 'retiré des'} favoris !")
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# --- LIVE SEARCH AUTOCOMPLETE API ---

def live_search_api(request):
    """API instantanée pour l'autocomplétion de recherche."""
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(brand__icontains=query) | Q(category__name__icontains=query)
        )[:6]
        for p in products:
            results.append({
                'id': p.id,
                'title': p.title,
                'price': f"{int(p.price):,} BIF".replace(',', ' '),
                'image': p.image,
                'category': p.category.name,
                'url': f"/product/{p.id}/"
            })
    return JsonResponse({'results': results})


# --- ESPACE CLIENT / AUTHENTIFICATION ---

def register_view(request):
    """Inscription client."""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        nom_complet = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        if not email or not password:
            messages.error(request, "Veuillez renseigner un email et un mot de passe.")
        elif password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse email est déjà enregistrée.")
        else:
            names = nom_complet.split(' ', 1)
            first_name = names[0]
            last_name = names[1] if len(names) > 1 else ''
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, f"Bienvenue sur Janvier-Shop, {user.first_name or user.username} !")
            return redirect('home')

    return render(request, 'shop/auth_register.html')


def login_view(request):
    """Connexion client."""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Ravi de vous revoir, {user.first_name or user.username} !")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Email ou mot de passe incorrect.")

    return render(request, 'shop/auth_login.html')


def logout_view(request):
    """Déconnexion client."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')


@login_required(login_url='login')
def profile_view(request):
    """Tableau de bord et historique des commandes du client."""
    user = request.user
    # Commandes associées directement ou par email
    orders = Commande.objects.filter(Q(user=user) | Q(email=user.email)).order_by('-date_commande')
    wishlist_count = Wishlist.objects.filter(user=user).count()

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.last_name = request.POST.get('last_name', user.last_name).strip()
        user.save()
        messages.success(request, "Vos informations de profil ont été mises à jour avec succès.")
        return redirect('profile')

    return render(request, 'shop/profile.html', {
        'orders': orders,
        'wishlist_count': wishlist_count,
    })


def contact(request):
    """Page de contact avec formulaire interactif."""
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        sujet = request.POST.get('sujet', '').strip()
        message = request.POST.get('message', '').strip()

        if nom and email and message:
            ContactMessage.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message
            )
            messages.success(request, "Votre message a été envoyé avec succès ! Notre équipe vous répondra dans les plus brefs délais.")
            return redirect('contact')
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")

    return render(request, 'shop/contact.html')


def about(request):
    """Page À propos de Janvier-Shop."""
    total_products = Product.objects.count()
    total_orders = Commande.objects.count()
    return render(request, 'shop/about.html', {
        'total_products': total_products,
        'total_orders': total_orders
    })


def newsletter_subscribe(request):
    """Inscription à la newsletter."""
    if request.method == 'POST':
        email = request.POST.get('newsletter_email', '').strip()
        if email:
            obj, created = Newsletter.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Merci pour votre inscription à notre newsletter !")
            else:
                messages.info(request, "Vous êtes déjà inscrit à notre newsletter.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))