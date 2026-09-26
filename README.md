# 🛍️ Janvier-Shop - Plateforme E-Commerce Django & PostgreSQL

Une application e-commerce complète, moderne et responsive développée avec **Django 3.2+**, **PostgreSQL local**, **Bootstrap 5.3**, et **JavaScript Vanilla** (Devise locale : **Franc Burundais - BIF**).

---

## ✨ Nouvelles Fonctionnalités & Améliorations

### 1. 🗄️ Base de données PostgreSQL locale
- Configuration dans `ecommerce/settings.py` via variables d'environnement (avec fallback automatique).
- Driver `psycopg2` / `psycopg2-binary` préconfiguré.
- Script de peuplement automatique `populate_db.py` (produits réalistes, catégories, avis, commandes).

### 2. 📦 Modèles de Données Enrichis (`shop/models.py`)
- **`Category`** : Nom, slug, icône FontAwesome, description, date de création.
- **`Product`** : Titre, slug, prix promo/réduction, stock en temps réel, note moyenne (1-5★), marque, produit vedette (is_featured), image haute résolution, description.
- **`ProductReview`** : Avis et évaluations clients (1 à 5 étoiles) avec calcul automatique de la moyenne.
- **`Commande`** : Numéro de commande unique (`ORD-XXXXXX`), détails complets des articles, mode de paiement (Paiement à la livraison, Orange/MTN Mobile Money, Carte Bancaire, PayPal), suivi de statut (`En attente`, `Confirmée`, `En transit`, `Livrée`).
- **`ContactMessage`** : Formulaire de contact avec historique en base et statut lu/non lu.
- **`Newsletter`** : Gestion des abonnés aux offres par email.

### 3. 🎨 Design Moderne & Expérience Utilisateur (UI/UX)
- **Design System** : Bootstrap 5.3, Google Fonts (*Plus Jakarta Sans*), FontAwesome 6, micro-animations, glassmorphism, badges et alertes flottantes (Toasts).
- **Panier Interactif (Drawer Offcanvas)** : Tiroir latéral dynamique, gestion des quantités (+ / -), suppression d'articles, calcul automatique du sous-total.
- **Codes Promotionnels** : Validation de codes de réduction dans le checkout (`PROMO10` pour -10%, `VIP20` pour -20%).

### 4. 📄 Nouvelles Pages Développées
- **Accueil (`/`)** : Bannière Hero moderne, pills de filtrage par catégorie, barre de recherche multi-critères, tri (prix, notes, nouveautés), produits mis en avant, pagination fluide.
- **Détails Produit (`/product/<id>/`)** : Galerie zoom, sélecteur de quantité, onglets Description et Avis Clients, formulaire d'ajout d'avis en direct, carrousel de produits similaires.
- **Validation de Commande (`/checkout/`)** : Formulaire 2 colonnes, choix du mode de livraison et paiement, récapitulatif détaillé en temps réel.
- **Confirmation & Facture (`/confirmation/`)** : Reçu de commande imprimable (`window.print()`), récapitulatif et raccourci vers le suivi.
- **Suivi de Commande en Temps Réel (`/suivi-commande/`)** : Timeline visuelle en 4 étapes de progression par numéro de commande ou email.
- **À Propos (`/a-propos/`)** : Présentation, statistiques clés et garanties de service.
- **Contact (`/contact/`)** : Formulaire de message, coordonnées directes et accordéon FAQ.

---

## 🚀 Démarrage Rapide

### 1. Activer l'environnement virtuel
```powershell
cd ecommerce
.\env\Scripts\Activate.ps1
```

### 2. Configuration PostgreSQL Local

1. Créez votre base de données PostgreSQL dans pgAdmin ou via le terminal psql :
```sql
CREATE DATABASE ecommerce_db;
```

2. Définissez vos variables d'environnement (ou utilisez les valeurs par défaut dans `settings.py`) :
```powershell
$env:USE_POSTGRESQL="True"
$env:DB_NAME="ecommerce_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="votre_mot_de_passe"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
```

### 3. Appliquer les migrations
```powershell
python manage.py migrate
```

### 4. Charger les données de démonstration
```powershell
python populate_db.py
```

### 5. Créer un compte administrateur (Optionnel)
```powershell
python manage.py createsuperuser
```

### 6. Lancer le serveur de développement
```powershell
python manage.py runserver
```

Rendez-vous sur [http://127.0.0.1:8000/](http://127.0.0.1:8000/) !
