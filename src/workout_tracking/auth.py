from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from .dependencies import get_dependencies
from werkzeug.security import check_password_hash

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        
        deps = await get_dependencies()
        user_repo = deps.infra_dependencies.user_repository
        
        user = await user_repo.get_by_email(email)
        
        if user and check_password_hash(user.hashed_password, password) and user.is_superuser:
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
