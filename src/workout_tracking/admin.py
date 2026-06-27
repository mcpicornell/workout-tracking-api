from sqladmin import ModelView
from .infra.db.models import ExerciseModel, UserModel, UserExerciseModel

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
