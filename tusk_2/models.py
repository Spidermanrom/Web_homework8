from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class Contacts(Document):
    full_name = StringField()
    email = StringField()
    phone = StringField()
    address = StringField()
    get_message = BooleanField(default=False)