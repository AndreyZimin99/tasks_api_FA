import os
import json
import aio_pika
import asyncio
from fastapi import FastAPI
import uvicorn

app = FastAPI()

RABBITMQ_URL = 'amqp://user:password@rabbitmq/'


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        if data['type'] == 'user_registered':
            email = data['data']['email']
            print(f'Sending welcome email to {email}')


async def consume():
    # connection = await aio_pika.connect_robust(RABBITMQ_URL)
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            break
        except Exception:
            print("RabbitMQ not ready, retrying in 3 seconds...")
            await asyncio.sleep(3)
    channel = await connection.channel()
    queue = await channel.declare_queue('email.notifications')
    await queue.consume(on_message)

@app.on_event('startup')
async def startup_event():
    asyncio.create_task(consume())


if __name__ == '__main__':
    uvicorn.run('email_service.main:app', reload=True)
