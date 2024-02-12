from django.shortcuts import get_object_or_404
from board.models import Comment

class BoardRepository:

    def find_comment_by_comment_id_with_post_and_parent(self, comment_id: int) -> Comment:
        """
        comment_id에 맞는 comment를 comment의 post의 멤버와 parent의 member를 조인해서 불러옴
        """
        return get_object_or_404(Comment.objects.select_related('post', 'parent'), id=comment_id)
    
    def find_comments_by_parent_with_member(self, parent) -> Comment:
        """
        부모가 같은 코멘트들을 member와 조인해서 얻어옴
        """
        return Comment.objects.filter(parent=parent).select_related('member')