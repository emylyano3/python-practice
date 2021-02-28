from dependency_injector import providers, containers
from token_manager import TokenManager
from iol_api import IolApi
from credential_manager import CredentialManager


class ApiConfig(containers.DeclarativeContainer):
    api_config = providers.Configuration('api_config')
    api_config.from_yaml('config.yml')


class Managers(containers.DeclarativeContainer):

    credential_manager = providers.Singleton(CredentialManager)
    token_manager = providers.Singleton(
        TokenManager,
        config=ApiConfig.api_config.api_config,
        credential_manager=credential_manager)


class Apis(containers.DeclarativeContainer):
    iol_api = providers.Singleton(
        IolApi,
        config=ApiConfig.api_config.api_config,
        token_manager=Managers.token_manager)
