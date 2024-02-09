from dependency_injector import containers, providers
from member.applications import MemberService
from member.domains import MemberRepository

class MembersContainer(containers.DeclarativeContainer):
    member_repository = providers.Factory(MemberRepository)
    member_service = providers.Factory(
        MemberService,
        member_repository=member_repository
    )