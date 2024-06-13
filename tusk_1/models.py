from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import EmbeddedDocumentField, ListField, StringField, DateTimeField, ReferenceField

class Tag(EmbeddedDocument):
    name = StringField()

class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    author = ReferenceField(Author, required=True)
    tags = ListField(EmbeddedDocumentField(Tag))
    quote = StringField()

