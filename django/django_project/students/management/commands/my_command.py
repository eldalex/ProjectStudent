from django.core.management.base import BaseCommand
from PIL import Image
import pika
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        count_try=0
        conn=False
        while not conn:
            count_try+=1
            print(f'I`m DJANGO WORKER. Попытка присоединится №{count_try}')
            conn, channel=self.initial()
            if not conn:
                time.sleep(2)
        print(' [*] I`m DJANGO WORKER and i`m Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def initial(self):
        try:
            hostname = 'rmq'
            port = 5672
            credentials = pika.PlainCredentials(username='admin', password='admin')
            parameters = pika.ConnectionParameters(host=hostname, port=port, credentials=credentials)
            connection = pika.BlockingConnection(parameters=parameters)
            # Создать канал
            channel = connection.channel()
            channel.queue_declare(queue='to_resize')
            channel.queue_declare(queue='from_resize')
            try:
                channel.basic_consume(queue='from_resize',
                                auto_ack=True,
                                on_message_callback=self.callback)
            except Exception as error:
                print(error)
            return True, channel
        except:
            return False, None

    @staticmethod
    def callback(ch, method, properties, body):
        try:
            data = body.split(b'separator')
            image = Image.frombytes("RGB", (int(data[1]), int(data[2])), data[0])
            file_name = data[3].decode('UTF-8')
            image.save('media/photo/' + file_name)
        except Exception as error:
            print(error)
