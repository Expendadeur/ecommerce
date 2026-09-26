import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from shop.models import Category, Product, ProductReview, Commande

def run():
    print("Insertion des catégories et des produits de démonstration...")

    # Catégories
    categories_data = [
        {"name": "Smartphones & Tablettes", "icon": "fa-mobile-screen-button", "description": "Derniers smartphones et tablettes haute performance."},
        {"name": "Ordinateurs & PC", "icon": "fa-laptop", "description": "Laptops ultralégers, stations de travail et ordinateurs gamer."},
        {"name": "Audio & Écouteurs", "icon": "fa-headphones", "description": "Casques réducteurs de bruit, enceintes et écouteurs sans fil."},
        {"name": "Montres & Connectés", "icon": "fa-clock", "description": "Smartwatches et bracelets connectés pour votre santé et sport."},
        {"name": "Photo & Caméras", "icon": "fa-camera", "description": "Appareils photos réflexes, hybrides et drones 4K."},
        {"name": "Accessoires High-Tech", "icon": "fa-plug", "description": "Chargeurs rapides, câbles, coques et supports."},
    ]

    category_objs = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"icon": cat_data["icon"], "description": cat_data["description"]}
        )
        category_objs[cat.name] = cat
        print(f"Catégorie: {cat.name} ({'créée' if created else 'existante'})")

    # Produits
    products_data = [
        {
            "title": "iPhone 15 Pro Max (256 Go) - Titane Naturel",
            "category": category_objs["Smartphones & Tablettes"],
            "price": 3850000.0,
            "discount_price": 4200000.0,
            "stock": 15,
            "rating": 4.9,
            "brand": "Apple",
            "is_featured": True,
            "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&auto=format&fit=crop&q=80",
            "description": "L'iPhone 15 Pro Max est forgé dans le titane de qualité aérospatiale avec la puce surpuissante A17 Pro, un bouton Action personnalisable et le système photo iPhone le plus avancé à ce jour.",
        },
        {
            "title": "Samsung Galaxy S24 Ultra AI (512 Go)",
            "category": category_objs["Smartphones & Tablettes"],
            "price": 3400000.0,
            "discount_price": 3900000.0,
            "stock": 20,
            "rating": 4.8,
            "brand": "Samsung",
            "is_featured": True,
            "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=800&auto=format&fit=crop&q=80",
            "description": "Bienvenue dans l'ère de Galaxy AI. Avec son stylet S Pen intégré, son capteur 200 MP et son écran Dynamic AMOLED 2X 120Hz ultra lumineux, surpassez toutes vos attentes.",
        },
        {
            "title": "MacBook Pro 16 M3 Max (36 Go RAM, 1 To SSD)",
            "category": category_objs["Ordinateurs & PC"],
            "price": 7500000.0,
            "discount_price": 8200000.0,
            "stock": 8,
            "rating": 5.0,
            "brand": "Apple",
            "is_featured": True,
            "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80",
            "description": "Le MacBook Pro 16 pouces avec puce M3 Max offre une autonomie record de 22 heures et une puissance graphique exceptionnelle pour les créateurs de contenu et développeurs exigeants.",
        },
        {
            "title": "Dell XPS 15 InfinityEdge OLED Touchscreen",
            "category": category_objs["Ordinateurs & PC"],
            "price": 5200000.0,
            "discount_price": 5800000.0,
            "stock": 12,
            "rating": 4.7,
            "brand": "Dell",
            "is_featured": False,
            "image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80",
            "description": "Design raffiné en aluminium usiné CNC, écran 3.5K OLED tactile à bordures ultra fines et processeur Intel Core i9 de 13e génération pour une polyvalence absolue.",
        },
        {
            "title": "Sony WH-1000XM5 Casque Réducteur de Bruit Sans Fil",
            "category": category_objs["Audio & Écouteurs"],
            "price": 1100000.0,
            "discount_price": 1250000.0,
            "stock": 25,
            "rating": 4.9,
            "brand": "Sony",
            "is_featured": True,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
            "description": "La référence absolue en matière de réduction active du bruit ambiant. Son haute résolution sans fil, 30 heures d'autonomie et appels cristallins grâce aux 8 microphones.",
        },
        {
            "title": "AirPods Pro 2 avec Boîtier MagSafe USB-C",
            "category": category_objs["Audio & Écouteurs"],
            "price": 750000.0,
            "discount_price": 890000.0,
            "stock": 40,
            "rating": 4.8,
            "brand": "Apple",
            "is_featured": False,
            "image": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80",
            "description": "Équipés de la puce H2, les AirPods Pro 2 offrent une réduction de bruit jusqu'à 2x plus efficace, l'audio spatial personnalisé et la détection des conversations.",
        },
        {
            "title": "Apple Watch Ultra 2 Titane GPS + Cellular 49mm",
            "category": category_objs["Montres & Connectés"],
            "price": 2600000.0,
            "discount_price": 2900000.0,
            "stock": 10,
            "rating": 4.9,
            "brand": "Apple",
            "is_featured": True,
            "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80",
            "description": "Conçue pour les athlètes d'endurance, l'exploration et les sports aquatiques. Boîtier en titane ultra-résistant, GPS double fréquence et autonomie jusqu'à 72h.",
        },
        {
            "title": "Sony Alpha 7 IV Appareil Photo Hybride Plein Format",
            "category": category_objs["Photo & Caméras"],
            "price": 6800000.0,
            "discount_price": 7400000.0,
            "stock": 5,
            "rating": 5.0,
            "brand": "Sony",
            "is_featured": False,
            "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop&q=80",
            "description": "Capteur Exmor R 33 MP plein format, vidéo 4K 60p 10-bit 4:2:2, autofocus IA avec suivi en temps réel des yeux humains, oiseaux et animaux.",
        },
        {
            "title": "Station de Charge Sans Fil 3-en-1 MagSafe 15W",
            "category": category_objs["Accessoires High-Tech"],
            "price": 150000.0,
            "discount_price": 210000.0,
            "stock": 60,
            "rating": 4.6,
            "brand": "Anker",
            "is_featured": False,
            "image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&auto=format&fit=crop&q=80",
            "description": "Rechargez simultanément votre iPhone, Apple Watch et vos AirPods avec un seul câble. Design élégant et compact pour votre table de chevet ou bureau.",
        }
    ]

    for p_data in products_data:
        p, created = Product.objects.get_or_create(
            title=p_data["title"],
            defaults=p_data
        )
        # S'il existe déjà, mettre à jour ses prix
        if not created:
            p.price = p_data["price"]
            p.discount_price = p_data["discount_price"]
            p.save()
        print(f"Produit: {p.title} - {p.price} BIF ({'créé' if created else 'mis à jour'})")

        # Ajouter des avis de démonstration
        if created:
            ProductReview.objects.create(
                product=p,
                name="Michel Nkurunziza",
                email="michel.nk@gmail.com",
                rating=5,
                comment="Produit exceptionnel ! Livraison en 24h chrono, emballage soigné et appareil conforme à 100%. Je recommande Janvier-Shop les yeux fermés."
            )
            ProductReview.objects.create(
                product=p,
                name="Aïcha Irakoze",
                email="aicha.ir@yahoo.fr",
                rating=5,
                comment="Superbe qualité de fabrication. Rapport qualité/prix imbattable avec la réduction de bienvenue en BIF !"
            )

    # Commande de démonstration
    cmd, cmd_created = Commande.objects.get_or_create(
        order_number="ORD-DEMO2026",
        defaults={
            "items": '{"1":[1,"iPhone 15 Pro Max (256 Go) - Titane Naturel",3850000.0,"https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800"]}',
            "total": "3 850 000 BIF",
            "nom": "Janvier Ndayisaba",
            "email": "janvier@example.com",
            "phone": "+257 79 12 34 56",
            "address": "Rohero I, Avenue de l'Université, N° 12",
            "ville": "Bujumbura",
            "pays": "Burundi",
            "zipcode": "B.P. 1234",
            "status": "PROCESSING",
            "payment_method": "MOBILE_MONEY"
        }
    )
    print(f"Commande démo: {cmd.order_number} ({'créée' if cmd_created else 'existante'})")
    print("Peuplement de la base de données terminé avec succès !")

if __name__ == '__main__':
    run()
