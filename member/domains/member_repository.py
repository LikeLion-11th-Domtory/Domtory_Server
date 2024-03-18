from django.shortcuts import get_object_or_404
from member.domains import Member

class MemberRepository:
    def find_member_by_username(self, username: str):
        return get_object_or_404(Member, username=username)
    
    def find_member_by_id(self, member_id: int):
        return get_object_or_404(Member, id=member_id)
    
    def find_member_with_notification_detail_by_id(self, member_id: int):
        return get_object_or_404(Member.objects.select_related('notificationdetail'), id=member_id)
    
    def save_member(self, member: Member):
        member.save()