from passlib.apps import custom_app_context

class PasswordHax:
    @staticmethod
    def create_password_hash(password: str) -> str:
        return custom_app_context.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return custom_app_context.verify(password, password_hash)
