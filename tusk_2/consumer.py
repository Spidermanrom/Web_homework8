import sys

import pika
from producer import connect, Contacts


def send_email(contact):
    print(f"Sending email to {contact.email}")


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    def callback(ch, method, properties, body):
        contact_id = body.decode()
        contact = Contacts.objects.get(id=contact_id)
        if contact and not contact.get_message:
            send_email(contact)
            contact.get_message = True
            contact.save()
            print(f" [x] Email sent to {contact.email}\n")

    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C\n')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)