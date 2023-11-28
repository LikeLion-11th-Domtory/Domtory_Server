from push.models import Token
from django.shortcuts import get_list_or_404

class PushRepository:
    def save_token(self, token: Token):
        token.save()
    
    def find_all_valid_tokens(self):
        return get_list_or_404(Token, is_valid=True)