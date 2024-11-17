from fastapi.exceptions import HTTPException

class LoginValidateException(HTTPException):
    def __init__(self):
        self.message = "`Username` and `Password` are required!"
        super().__init__(status_code=400, detail=self.message)


class RegisterValidateException(HTTPException):
    def __init__(self):
        self.message = "`Username`, `Email` and `Password` are required!"
        super().__init__(status_code=400, detail=self.message)


class CreateUserException(HTTPException):
    def __init__(self):
        self.message = "can not create user object in database!"
        super().__init__(status_code=500, detail=self.message)



class FieldRequiredException(HTTPException):
    def __init__(self, message):
        self.message = message
        super().__init__(status_code=400, detail=self.message)


class InvalidPasswordException(HTTPException):
    def __init__(self):
        self.message = "Wrong password!"
        super().__init__(status_code=400, detail=self.message)


class InvalidEmailException(HTTPException):
    def __init__(self):
        self.message = "Wrong Email!"
        super().__init__(status_code=400, detail=self.message)


class NotCreatedTokensError(HTTPException):
    def __init__(self):
        self.message = "Can not create tokens for the user!"
        super().__init__(status_code=500, detail=self.message)


class NotAuthorizationException(HTTPException):
    def __init__(self):
        self.message = "User not authorization!"
        super().__init__(status_code=401, detail=self.message)


class InvalidToken(HTTPException):
    def __init__(self):
        self.message = "Invalid token"
        super().__init__(status_code=401, detail=self.message)


class NotUpdateUserError(HTTPException):
    def __init__(self):
        self.message = "can not update user!"
        super().__init__(status_code=500, detail=self.message)


class  NotRefreshToken(HTTPException):
    def __init__(self):
        self.message = "Refresh Token is required!"
        super().__init__(status_code=400, detail=self.message)
