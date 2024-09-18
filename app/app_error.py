class AppError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return {'message': self.message}

    def print_error(self):
        print(self.__str__())