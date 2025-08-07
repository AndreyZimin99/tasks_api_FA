import asyncio
import aio_pika
from datetime import datetime, timedelta
import json
import jwt
from passlib.context import CryptContext
import uuid

from src.config import settings

rabbit_connection = None
RABBITMQ_URL = 'amqp://user:password@rabbitmq/'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire
    )
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithms: str = settings.auth_jwt.algorithm
):

    decoded = jwt.decode(token, public_key, algorithms)
    return decoded


def hash_password(
    password: str,
) -> str:
    return pwd_context.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(password.encode(), hashed_password)


async def send_email_event(user_id: str, email: str):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        message = {
            "type": "user_registered",
            "data": {
                "user_id": user_id,
                "email": email,
            }
        }
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key="email.notifications"
        )


# async def get_rabbit_connection():
#     global rabbit_connection
#     if rabbit_connection is None or rabbit_connection.is_closed:
#         rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
#     return rabbit_connection

async def get_rabbit_connection():
    global rabbit_connection
    if rabbit_connection is None or rabbit_connection.is_closed:
        while True:
            try:
                rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
                break
            except Exception:
                print("RabbitMQ not ready, retrying in 3 seconds...")
                await asyncio.sleep(3)
        return rabbit_connection


async def get_task_count(user_id: str):
    connection = await get_rabbit_connection()
    channel = await connection.channel()

    correlation_id = str(uuid.uuid4())

    message = aio_pika.Message(
        body=user_id.encode(),
        correlation_id=correlation_id,
        reply_to='auth_response_queue',
    )

    await channel.default_exchange.publish(
        message,
        routing_key='task_request_queue',
    )

    response = await wait_for_response(correlation_id)

    return response


async def wait_for_response(correlation_id: str):
    connection = await get_rabbit_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue("auth_response_queue")

    async def on_response(message: aio_pika.IncomingMessage):
        async with message.process():
            if message.correlation_id == correlation_id:
                return int(message.body.decode())

    response = None
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            response = await on_response(message)
            if response is not None:
                break

    return response
