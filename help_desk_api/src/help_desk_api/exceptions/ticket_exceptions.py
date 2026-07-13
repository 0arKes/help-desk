from fastapi import HTTPException, status


class TicketNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found."
        )


class InvalidUserRole(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized action."
        )


class TicketHasBeenAssigned(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="This ticket already has an assignee and cannot be modified.",
        )


class TicketDoesNotBelongToUser(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This ticket does not belong to you.",
        )


class InvalidTicketStatus(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="This ticket has been resolved.",
        )
