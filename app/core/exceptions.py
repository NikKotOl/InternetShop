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


class UserNotFoundError(NotFoundError):

    def __init__(self, id_or_username: str | int):
        if isinstance(id_or_username, str):
            self.message = f"User with username '{id_or_username}' not found"
            super().__init__(self.message)
        else:
            self.message = f"User with id={id_or_username} not found"
            super().__init__(self.message)


class AlreadyExistsError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserAlreadyExistsError(AlreadyExistsError):
    def __init__(self, id_or_username):
        if isinstance(id_or_username, str):
            self.message = f"User with username '{id_or_username}' already exists"
            super().__init__(self.message)
        else:
            self.message = f"User with id={id_or_username} already exists"
            super().__init__(self.message)


class InvalidCredentialsError(Exception):
    def __init__(self):
        self.message = f"Invalid credentials"
        super().__init__(self.message)


class InvalidQuantityError(ValueError):
    def __init__(self, quantity: int):
        self.quantity = quantity
        super().__init__(f"Invalid quantity: {quantity}")


class CartNotFoundError(NotFoundError):
    def __init__(self, id: int):
        self.message = f"Cart with id={id} not found"
        super().__init__(self.message)


class CartAccessDeniedError(Exception):
    def __init__(self, cart_id: int):
        self.cart_id = cart_id
        super().__init__(f"Access denied to cart item {cart_id}")
