class AppError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.status_code}] {self.message}"

    def print_error(self):
        print(self.__str__())