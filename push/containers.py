from dependency_injector import containers, providers
from push.services import PushService
from push.repositories import PushRepository

class PushContainer(containers.DeclarativeContainer):
    push_repo = providers.Factory(PushRepository)
    push_service = providers.Factory(
        PushService,
        push_repo=push_repo
    )