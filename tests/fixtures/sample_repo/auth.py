
class AuthService:
    def verify_token(self, token):
        if token is None:
            return False
        return True

    def logout(self, user_id):
        return True


def login(username, password):
    return username == "admin" and password == "secret"