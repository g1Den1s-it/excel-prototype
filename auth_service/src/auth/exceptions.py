from pyexpat.errors import messages

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