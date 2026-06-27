import asyncio
from workout_tracking.dependencies import get_dependencies
from workout_tracking.infra.db.models import UserModel
from werkzeug.security import generate_password_hash

async def create_superuser():
    deps = await get_dependencies()
    session = deps.infra_dependencies.user_repository.session
    
    email = input("Email: ")
    password = input("Password: ")
    
    hashed_password = generate_password_hash(password)
    
    user = UserModel(
        email=email,
        hashed_password=hashed_password,
        is_superuser=True
    )
    
    async with session.begin():
        session.add(user)
    
    print(f"Superuser {email} created successfully.")

if __name__ == "__main__":
    asyncio.run(create_superuser())
