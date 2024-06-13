from tusk_1.models import Author, Quote
from tusk_1.connect_mongo import connect


def search_quotes(query):
    if query.startswith('name:'):
        author_name = query.split(':')[1].strip()
        author = Author.objects(fullname__icontains=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes
        else:
            return "Author not found."
    elif query.startswith('tag:'):
        tag_name = query.split(':')[1].strip()
        quotes = Quote.objects(tags__name=tag_name)
        return quotes
    elif query.startswith('tags:'):
        tag_names = query.split(':')[1].strip().split(',')
        quotes = Quote.objects(tags__name__in=tag_names)
        return quotes
    elif query == 'exit':
        return None
    else:
        return "Invalid query format."

if __name__ == "__main__":
    while True:
        user_input = input("Enter your query: ")
        result = search_quotes(user_input)
        if result is None:
            print("Exiting...")
            break
        else:
            for quote in result:
                try:
                    print(quote.quote)
                except AttributeError:
                    pass