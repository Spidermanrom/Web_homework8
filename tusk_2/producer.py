from faker import Faker
from mongoengine import connect
from models import Contacts
import pika

URI = "mongodb+srv://krom4rd:t6abZEUNgL1uhHVu@oleg.qq4u8pu.mongodb.net/?retryWrites=true&w=majority&appName=Oleg"

connect(host=URI,db='test')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
    )
)
chanel = connection.channel()
chanel.queue_declare(queue='email_queue')

Faker.seed(1)
fake = Faker()


def main():
    for _ in range(10):
        name = fake.name()
        email = fake.email()
        phone = '+380'
        phone += str(fake.random_number(digits=9, fix_len=True))
        adress = fake.address()

        contact = Contacts(
            full_name=name,
            email=email,
            phone=phone,
            address=adress
        ).save()

        chanel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id).encode())
        print(f'[x] Sent {contact.id}')

    connection.close()


if __name__ == '__main__':
    main() 