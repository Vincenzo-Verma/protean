from enum import Enum

from protean import Domain
from protean.fields import Identifier, String

domain = Domain(name="Authentication")


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


@domain.event(part_of="User")
class UserActivated:
    user_id = Identifier(required=True)


@domain.event(part_of="User")
class UserRenamed:
    user_id = Identifier(required=True)
    name = String(required=True, max_length=50)


@domain.aggregate
class User:
    name = String(max_length=50, required=True)
    email = String(required=True)
    status = String(choices=UserStatus)

    def activate(self) -> None:
        self.status = UserStatus.ACTIVE.value
        self.raise_(UserActivated(user_id=self.id))

    def change_name(self, name: str) -> None:
        self.name = name
        self.raise_(UserRenamed(user_id=self.id, name=name))
