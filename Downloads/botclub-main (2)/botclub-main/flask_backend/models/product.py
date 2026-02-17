from mongoengine import Document, StringField, FloatField, IntField

class Product(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    description = StringField()
    category = StringField()
    imageUrl = StringField()
    stock = IntField(default=0)
