from enum import Enum


class HistoryAction(Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"

    STATUS_CHANGED = "status_changed"
    RESOLVED = "resolved"
    REOPENED = "reopened"
