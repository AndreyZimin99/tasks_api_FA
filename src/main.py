import uvicorn
from fastapi import FastAPI
import asyncio
import aio_pika

from api.v1.routers.task import router as task_router

app = FastAPI()
app.include_router(task_router, prefix='/tasks')


RABBITMQ_URL = 'amqp://guest:guest@rabbitmq/'


rabbit_connection = None


async def wait_for_rabbitmq():
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            return connection
        except Exception as e:
            print(f"Waiting for RabbitMQ to be ready... {e}")
            await asyncio.sleep(5)


async def get_rabbit_connection():
    global rabbit_connection
    if rabbit_connection is None or rabbit_connection.is_closed:
        rabbit_connection = await wait_for_rabbitmq()
        return rabbit_connection


@app.on_event('startup')
async def startup_event():
    async with await get_rabbit_connection():
        asyncio.create_task(consume_messages())


@app.on_event('shutdown')
async def shutdown_event():
    global rabbit_connection
    if rabbit_connection:
        await rabbit_connection.close()


async def on_request(message: aio_pika.IncomingMessage):
    async with message.process():
        user_id = message.body.decode()
        print(f"Received request for user ID: {user_id}")

        task_count = get_task_count_for_user(user_id)

        response_message = str(task_count).encode()
        await message.reply(response_message, correlation_id=message.correlation_id)


def get_task_count_for_user(user_id):
    return 3


async def consume_messages():
    connection = get_rabbit_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("task_request_queue")
    await queue.consume(on_request)


if __name__ == '__main__':
    uvicorn.run('src.main:app', reload=True)
