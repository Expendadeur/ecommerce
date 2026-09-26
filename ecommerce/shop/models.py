from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom de la catégorie")
    slug = models.SlugField(max_length=200, blank=True, null=True)
    icon = models.CharField(max_length=100, default="fa-tag", blank=True, help_text="Classe FontAwesome")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        ordering = ['name']
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre du produit")
    slug = models.SlugField(max_length=250, blank=True, null=True)
    price = models.FloatField(verbose_name="Prix actuel (BIF)")
    discount_price = models.FloatField(blank=True, null=True, verbose_name="Ancien prix / Promo (BIF)")
    description = models.TextField(verbose_name="Description détaillée")
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Catégorie")
    image = models.CharField(max_length=5000, verbose_name="URL de l'image principale")
    stock = models.PositiveIntegerField(default=25, verbose_name="Quantité en stock")
    rating = models.FloatField(default=4.5, verbose_name="Note moyenne (sur 5)")
    brand = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marque")
    is_featured = models.BooleanField(default=False, verbose_name="Mettre en avant sur la page d'accueil")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        ordering = ['-date_added']
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        if self.discount_price and self.discount_price > self.price:
            diff = self.discount_price - self.price
            return int((diff / self.discount_price) * 100)
        return 0


class ProductReview(models.Model):
    RATING_CHOICES = [
        (1, '1 étoile'),
        (2, '2 étoiles'),
        (3, '3 étoiles'),
        (4, '4 étoiles'),
        (5, '5 étoiles'),
    ]
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name="Produit")
    name = models.CharField(max_length=120, verbose_name="Nom de l'auteur")
    email = models.EmailField(verbose_name="Email")
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name="Note")
    comment = models.TextField(verbose_name="Commentaire")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")

    class Meta:
        ordering = ['-date_added']
        verbose_name = "Avis produit"
        verbose_name_plural = "Avis produits"

    def __str__(self):
        return f"Avis de {self.name} sur {self.product.title}"


class Commande(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('PROCESSING', 'En cours de préparation'),
        ('SHIPPED', 'En cours de livraison'),
        ('DELIVERED', 'Livrée'),
        ('CANCELLED', 'Annulée'),
    ]
    PAYMENT_CHOICES = [
        ('COD', 'Paiement Cash à la livraison (BIF)'),
        ('MOBILE_MONEY', 'EcoCash / Lumicash (Mobile Money)'),
        ('CARD', 'Carte Bancaire (Visa / Mastercard)'),
        ('PAYPAL', 'PayPal'),
    ]

    order_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro de commande")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Client")
    items = models.TextField(verbose_name="Détails du panier (JSON)")
    total = models.CharField(max_length=200, verbose_name="Total payé")
    nom = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, default="", verbose_name="Téléphone")
    address = models.CharField(max_length=200, verbose_name="Adresse")
    ville = models.CharField(max_length=200, verbose_name="Ville")
    pays = models.CharField(max_length=300, verbose_name="Pays")
    zipcode = models.CharField(max_length=300, verbose_name="Code Postal")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='COD', verbose_name="Mode de paiement")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING', verbose_name="Statut")
    date_commande = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")

    class Meta:
        ordering = ['-date_commande']
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return f"{self.order_number or 'Commande'} - {self.nom} ({self.total})"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-date_added']
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"

    def __str__(self):
        return f"{self.product.title} (Favori)"


class ContactMessage(models.Model):
    nom = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    sujet = models.CharField(max_length=250, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    date_envoye = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Message lu")

    class Meta:
        ordering = ['-date_envoye']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.sujet} - {self.nom}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    date_abonne = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")

    class Meta:
        ordering = ['-date_abonne']
        verbose_name = "Abonné Newsletter"
        verbose_name_plural = "Abonnés Newsletter"

    def __str__(self):
        return self.email