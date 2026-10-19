from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "signup/",
        views.signup_user,
        name="signup_user"
    ),

    path(
        "signup/business/",
        views.signup_business,
        name="signup_business"
    ),

    path(
        "login/",
        views.login_user,
        name="login"
    ),

    path(
        "logout/",
        views.logout_user,
        name="logout"
    ),


    # USER

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "food/<int:food_id>/",
        views.food_detail,
        name="food_detail"
    ),

    path(
        "food/<int:food_id>/reserve/",
        views.reserve_food,
        name="reserve_food"
    ),

    path(
        "reservations/",
        views.my_reservations,
        name="my_reservations"
    ),

    path(
        "reservations/<int:reservation_id>/cancel/",
        views.cancel_reservation,
        name="cancel_reservation"
    ),


    # BUSINESS

    path(
        "business/dashboard/",
        views.business_dashboard,
        name="business_dashboard"
    ),

    path(
        "business/food/<int:food_id>/edit/",
        views.business_food_edit,
        name="business_food_edit"
    ),

    path(
        "business/food/<int:food_id>/toggle/",
        views.business_food_toggle,
        name="business_food_toggle"
    ),

    path(
        "business/food/<int:food_id>/delete/",
        views.business_food_delete,
        name="business_food_delete"
    ),

    path(
        "business/reservations/<int:reservation_id>/verify/",
        views.business_verify_pickup_code,
        name="business_verify_pickup_code"
    ),

    path(
        "business/reservations/<int:reservation_id>/<str:action>/",
        views.business_reservation_update,
        name="business_reservation_update"
    ),


    # ACCOUNT

    path(
        "account/",
        views.account,
        name="account"
    ),

    path(
        "account/profile/",
        views.update_profile,
        name="update_profile"
    ),

    path(
        "account/password/",
        views.change_password,
        name="change_password"
    ),
]