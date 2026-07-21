class NotFoundError(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ProductNotFoundError(NotFoundError):

    def __init__(self, id: int):
        self.message = f"Product with id={id} not found"
        super().__init__(self.message)


class CategoryNotFoundError(NotFoundError):
    
    def __init__(self, id: int):
        self.message = f"Category with id={id} not found"
        super().__init__(self.message)
