from django.urls import path
from .views import *
urlpatterns=[
path('', HomePage.as_view(), name='homepage'),
path('login', Login.as_view(), name='login'),
path('register', Register.as_view(), name='register'),
path('forgot-password', ForgotPasswordView.as_view(), name='forgot_password'),
path('recover-password', ResetPassword.as_view(), name='recover_password'),
path('contact-us', ContactUs.as_view(), name='contact_us'),
path('profile', Profile.as_view(), name='profile'),
path('logout', LogoutView, name="logout" ),
path('about-us', AboutUs, name="about_us" ),
path('select-package', SelectPackage.as_view(), name="select_package" ),
path('buy-plan', BuyPlan.as_view(), name="buy_plan" ),
path('thankyou', Thankyou.as_view(), name="thankyou" ),
]