# import pika
# import json
# import threading


# def send_welcome_email(email):
#     print(f'Sending welcome email to {email}')


# def callback(ch, method, properties, body):
#     data = json.loads(body)
#     email = data.get('email')
#     if email:
#         send_welcome_email(email)
#         ch.basic_ack(delivery_tag=method.delivery_tag)


# def start_email_consumer():
#     def run():
#         connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#         with connection:
#             with connection.channel() as channel:

#                 channel.queue_declare(queue='email.notifications', durable=True)

#                 channel.basic_consume(queue='email.notifications', on_message_callback=callback)

#                 print('Waiting for messages. To exit press CTRL+C')
#                 channel.start_consuming()

#     threading.Thread(target=run, daemon=True).start()
