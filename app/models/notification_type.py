from enum import Enum


class NotificationType(str, Enum):
    REAL_TIME = "real_time"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
