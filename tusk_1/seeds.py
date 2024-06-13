import json
from tusk_1.models import Author, Quote, Tag
from mongoengine.errors import DoesNotExist
from tusk_1.connect_mongo import connect
from datetime import datetime
# from dateutil import parser
connect

def load_authors_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            born_date = None
            if author_data.get('born_date'):
                try:
                    format_date_string = "%B %d, %Y"
                    born_date = datetime.strptime(author_data['born_date'], format_date_string).date()

                    # born_date = parser.parse(author_data['born_date'])
                except ValueError:
                    print(f"Invalid date format for author: {author_data['fullname']} - {author_data['born_date']}")
            author = Author(fullname=author_data['fullname'],
                            born_date=born_date,
                            born_location=author_data.get('born_location'),
                            description=author_data.get('description'))
            author.save()

def load_quotes_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            try:
                author = Author.objects.get(fullname=author_name)
                tags = [Tag(name=tag) for tag in quote_data.get('tags', [])]
                quote = Quote(author=author,
                              quote=quote_data.get('quote'),
                              tags=tags)
                quote.save()
            except DoesNotExist:
                print(f"Author {author_name} not found.")


if __name__ == "__main__":
    load_authors_from_json("authors.json")
    load_quotes_from_json("qoutes.json")