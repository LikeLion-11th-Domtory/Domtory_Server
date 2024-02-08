from dependency_injector import containers, providers
from push.services import PushService
from push.domains import PushRepository

class PushContainer(containers.DeclarativeContainer):
    push_repository = providers.Factory(PushRepository)
    push_service = providers.Factory(
        PushService,
        push_repository=push_repository
    )