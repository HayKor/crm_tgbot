import logging

from core.config import AppConfig
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.aiogram import AiogramProvider
from retailcrm import v5 as RetailClient


logger = logging.getLogger(__name__)


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


container = make_async_container(AppProvider(), AiogramProvider())
