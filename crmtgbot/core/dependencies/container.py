import logging
from typing import AsyncGenerator

from core.config import AppConfig
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.aiogram import AiogramProvider
from redis.asyncio import ConnectionPool, Redis
from retailcrm import v5 as RetailClient


logger = logging.getLogger(__name__)


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_redis_pool(self, config: AppConfig) -> AsyncGenerator[ConnectionPool, None]:
        pool = ConnectionPool.from_url(config.redis.url)
        yield pool
        await pool.aclose()

    @provide(scope=Scope.REQUEST)
    async def provide_redis_conn(self, pool: ConnectionPool) -> AsyncGenerator[Redis, None]:
        conn = Redis(connection_pool=pool)
        try:
            yield conn
        finally:
            await conn.aclose()


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_app_config(self) -> AppConfig:
        return AppConfig.from_env()

    @provide(scope=Scope.APP)
    def provide_retail_client(self, config: AppConfig) -> RetailClient:
        return RetailClient(
            crm_url=config.crm.url,
            api_key=config.crm.token,
        )


container = make_async_container(AppProvider(), AiogramProvider(), RedisProvider())
