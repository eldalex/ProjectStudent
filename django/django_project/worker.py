import pika
from PIL import Image
import io
import time


def initial():
    try:
        hostname = 'rmq'
        port = 5672
        credentials = pika.PlainCredentials(username='admin', password='admin')
        parameters = pika.ConnectionParameters(host=hostname, port=port, credentials=credentials)
        connection = pika.BlockingConnection(parameters=parameters)
        # Создать канал
        channel = connection.channel()
        # На всякий случай создаём очереди
        channel.queue_declare(queue='to_resize')
        channel.queue_declare(queue='from_resize')
        channel.basic_consume(queue='to_resize',
                      auto_ack=True,
                      on_message_callback=callback)

        return True, channel
    except:
        return False, None

def callback(ch, method, properties, body):
    try:
        data = body.split(b'separator')
        file_name = b'separator' + data[1]
        fixed_height = 300
        image = Image.open(io.BytesIO(data[0]))
        height_percent = (fixed_height / float(image.size[1]))
        width_size = int((float(image.size[0]) * float(height_percent)))
        new = image.resize((width_size, fixed_height))
        img_width = bytes(f'separator{new.width}', 'utf-8')
        img_height = bytes(f'separator{new.height}', 'utf-8')
        tobyte = new.tobytes() + img_width + img_height + file_name
        return_resize_image(tobyte)
    except Exception as error:
        print(error)


def return_resize_image(data):
    channel.basic_publish(exchange='',
                          routing_key='from_resize',
                          body=data)


if __name__ == '__main__':
    count_try=0
    conn=False
    while not conn:
        count_try+=1
        print(f'I`m WORKER. Попытка присоединится №{count_try}')
        conn, channel=initial()  
        if not conn:
            time.sleep(2)  
    print(' [*] I`m WORKER and i`m Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

