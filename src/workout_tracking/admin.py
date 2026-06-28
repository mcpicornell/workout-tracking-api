from sqladmin import ModelView
from .infra.db.models import ExerciseModel, UserModel, UserExerciseModel, JobModel
from .settings import get_settings

class JobAdmin(ModelView, model=JobModel):
    name = "Job"
    plural = "Jobs"
    column_list = [JobModel.id, JobModel.name, JobModel.status]

class UserAdmin(ModelView, model=UserModel):
    name = "User"
    plural = "Users"
    column_list = [UserModel.id, UserModel.email]

class ExerciseAdmin(ModelView, model=ExerciseModel):
    name = "Exercise"
    plural = "Exercises"
    column_list = [ExerciseModel.id, ExerciseModel.name]

class UserExerciseAdmin(ModelView, model=UserExerciseModel):
    name = "User Exercise"
    plural = "User Exercises"
    column_list = [
        UserExerciseModel.id, 
        "user", 
        "exercise", 
        "date"
    ]

ADMIN_VIEWS = (
    JobAdmin,
    UserAdmin,
    ExerciseAdmin,
    UserExerciseAdmin,
)

authentication_backend = AdminAuth(secret_key=get_settings().SECRET_AUTH_KEY)
