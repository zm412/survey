
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("add_question/", views.add_question, name="add_question"),
    path("delete_question/<int:quest_id>", views.delete_question, name="delete_question"),
    path("update_question/<int:quest_id>", views.update_question, name="update_question"),

    path("delete_opt/<int:opt_id>", views.delete_opt, name="delete_opt"),
    path("add_opt/<int:quest_id>", views.add_opt, name="add_opt"),




    path("add_survey/", views.add_survey, name="add_survey"),
    path("add_on_list/<int:surv_id>", views.add_on_list, name="add_on_list"),
    path("delete_survey/<int:surv_id>", views.delete_survey, name="delete_survey"),
    path("del_from_list/<int:surv_id>/<int:quest_id>", views.del_from_list, name="del_from_list"),
    path("update_survey/<int:surv_id>", views.update_survey, name="update_survey"),


    path("start_surv/<int:surv_id>", views.start_surv, name="start_surv"),
    path("add_interv/<int:surv_id>", views.add_interv, name="add_interv"),

]
