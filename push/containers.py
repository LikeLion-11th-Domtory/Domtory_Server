from dependency_injector import containers, providers
from push.services import PushService, DeviceService
from push.domains import PushRepository
from board.repositories import BoardRepository
from member.domains import MemberRepository

class PushContainer(containers.DeclarativeContainer):
    push_repository = providers.Factory(PushRepository)
    board_repository = providers.Factory(BoardRepository)
    member_repository = providers.Factory(MemberRepository)
    push_service = providers.Factory(
        PushService,
        push_repository=push_repository,
        board_repository=board_repository,
        member_repository=member_repository
    )
    device_service = providers.Factory(
        DeviceService,
        push_repository=push_repository,
        board_repository=board_repository
    )