from dependency_injector import containers, providers
from push.services import PushService
from push.domains import PushRepository
from board.repositories import BoardRepository

class PushContainer(containers.DeclarativeContainer):
    push_repository = providers.Factory(PushRepository)
    board_repository = providers.Factory(BoardRepository)
    push_service = providers.Factory(
        PushService,
        push_repository=push_repository,
        board_repository=board_repository
    )
    device_service = providers.Factory(
        PushService,
        push_repository=push_repository,
        board_repository=board_repository
    )