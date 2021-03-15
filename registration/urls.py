from django.urls import path, include
from registration.forms import CustomUserForm
from django_registration.backends.one_step.views import RegistrationView
from registration import views as registration_views


urlpatterns = [
    path(
        "accounts/register/",
        RegistrationView.as_view(
            form_class=CustomUserForm, success_url="/accounts/login/addcard/"
        ),
        name="django_registration_register",
    ),
    path("accounts/", include("django_registration.backends.one_step.urls")),
    path("accounts/", include("django.contrib.auth.urls"), name="login"),
    path(
        "accounts/login/addcard/",
        registration_views.ProfilePage.as_view(),
        name="profile",
    ),
    path(
        "accounts/login/addcard/logout/",
        registration_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "myplan/",
        registration_views.UserSubscriptionPlan.as_view(),
        name="mysubscriptionplan",
    ),
    path(
        "create-sub", registration_views.CreateSubscription.as_view(), name="createsub"
    ),
    path("complete", registration_views.Complete.as_view(), name="complete"),
    path("cancel", registration_views.CancelSubscription.as_view(), name="cancel"),
]