from mongoengine import Document, StringField, ListField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField, IntField
from .product import Product

class CartItem(EmbeddedDocument):
    product = ReferenceField(Product)
    quantity = IntField(default=1)

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default="customer")
    wishlist = ListField(ReferenceField(Product))
    cart = ListField(EmbeddedDocumentField(CartItem))
