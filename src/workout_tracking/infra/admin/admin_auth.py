from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from werkzeug.security import check_password_hash

from workout_tracking.infra.db.database import AsyncSessionLocal
from workout_tracking.infra.repositories.user_repository import DefaultUserRepository
from workout_tracking.infra.repositories.user_repository_types import GetUserByEmailInput


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str, session_factory):
        self._session_factory = session_factory
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        async with self._session_factory() as session:
            user_repo = DefaultUserRepository(session)
            user = await user_repo.get_user_by_email(GetUserByEmailInput(email=email))

        if (
            user
            and check_password_hash(user.hashed_password, password)
            and user.is_superuser
        ):
            request.session.update({"user_id": str(user.id)})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        if not user_id:
            return False
        return True
