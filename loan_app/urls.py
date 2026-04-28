from django.urls import path
from django.views.generic import RedirectView
from django.templatetags.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('debug/db/', views.debug_db, name='debug_db'),
    path("test-email/", views.test_email, name="test_email"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path(
        "favicon.ico",
        RedirectView.as_view(url=static("favicon.ico"), permanent=True),
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change.html", success_url="done/"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("farmer/profile/", views.farmer_profile, name="farmer_profile"),
    path(
        "farmer/profile/view/<int:user_id>/",
        views.farmer_profile_view,
        name="farmer_profile_view",
    ),
    path(
        "farmer/profile/create/",
        views.farmer_profile_create,
        name="farmer_profile_create",
    ),
    path(
        "farmer/profile/update/",
        views.farmer_profile_update,
        name="farmer_profile_update",
    ),
    path("farmer/upload/document/", views.upload_document, name="upload_document"),
    path("farmer/upload/nid/", views.upload_nid, name="upload_nid"),
    path("loan/apply/", views.loan_apply, name="loan_apply"),
    path("loan/history/", views.loan_history, name="loan_history"),
    path("loan/<int:pk>/", views.loan_detail, name="loan_detail"),
    path("loan/<int:pk>/pdf/", views.loan_download_pdf, name="loan_download_pdf"),
    path("loan/<int:pk>/approve/", views.approve_loan, name="approve_loan"),
    path("loan/<int:pk>/reject/", views.reject_loan, name="reject_loan"),
    path("loans/", views.loan_list, name="loan_list"),
    path("loan/<int:loan_id>/repayment/", views.make_repayment, name="make_repayment"),
    path("loan/<int:loan_id>/record-repayment/", views.record_repayment_by_officer, name="record_repayment_by_officer"),
    path("repayments/", views.repayment_history, name="repayment_history"),
    path("repayments/pdf/", views.repayment_history_download_pdf, name="repayment_history_download_pdf"),
    path("repayment/<int:pk>/pdf/", views.repayment_download_pdf, name="repayment_download_pdf"),
    path("repayment/pending/", views.repayment_list, name="repayment_list"),
    path("repayment/<int:pk>/approve/", views.approve_repayment, name="approve_repayment"),
    path("repayment/<int:pk>/reject/", views.reject_repayment, name="reject_repayment"),
    path("farmers/", views.farmer_list, name="farmer_list"),
    path("nid/verify/<int:user_id>/", views.verify_nid, name="verify_nid"),
    path(
        "nid/verification/", views.nid_verification_list, name="nid_verification_list"
    ),
]
