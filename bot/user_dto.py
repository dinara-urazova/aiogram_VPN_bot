from typing import NamedTuple, Optional
from datetime import datetime


class UserDTO(NamedTuple):
    telegram_id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    created_at: Optional[datetime] = (
        None  # None тк не передается с остальными параметрами в add_user, а создается в ней
    )
    updated_at: Optional[datetime] = None  # same here as above
