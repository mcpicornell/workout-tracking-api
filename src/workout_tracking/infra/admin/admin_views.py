from sqladmin import ModelView

from workout_tracking.infra.db.models import (
    ExerciseModel,
    JobModel,
    UserExerciseModel,
    UserModel,
)


class JobAdmin(ModelView, model=JobModel):
    name = "Job"
    plural = "Jobs"
    column_list = [JobModel.id, JobModel.description, JobModel.status]


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
    column_list = [UserExerciseModel.id, "user", "exercise", "date"]


ADMIN_VIEWS = (
    JobAdmin,
    UserAdmin,
    ExerciseAdmin,
    UserExerciseAdmin,
)
