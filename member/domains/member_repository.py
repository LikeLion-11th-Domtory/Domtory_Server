from django.shortcuts import get_object_or_404
from member.domains import Member

class MemberRepository:
    def find_member_by_email(self, email: str):
        return get_object_or_404(Member, email=email)
    
    def find_member_by_id(self, member_id: int):
        return get_object_or_404(Member, id=member_id)
    
    def save_member(self, member: Member):
        member.save()