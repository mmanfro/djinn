from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.timezone import now


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(now)
        )
account_activation_token = TokenGenerator()
