from push.models import Token

class PushRepository:
    def save_token(self, token: Token):
        token.save()