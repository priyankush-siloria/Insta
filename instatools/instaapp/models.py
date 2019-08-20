from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ForgetPassword(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
	code=models.CharField(max_length=100, blank=True, null=True, verbose_name='Code')

	def __str__(self):
		name = self.user.first_name + self.user.last_name
		return name

class UserPackage(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
	user_account=models.IntegerField(blank=True, null=True, verbose_name='user_account')
	user_package=models.CharField(max_length=100, blank=True, null=True, verbose_name='user_package')
	def __str__(self): 
		return self.user.username

class UserAccounts(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
	email_account=models.CharField(max_length=100, blank=True, null=True, verbose_name='user_account')
	account_password=models.CharField(max_length=100, blank=True, null=True, verbose_name='user_package')
	country=models.CharField(max_length=100, blank=True,null=True)
	def __str__(self):
		return self.email_account

class UserInstaDetail(models.Model):
	insta_user = models.ForeignKey(UserAccounts, blank=True,null=True, on_delete=models.CASCADE, verbose_name='Insta User')
	posts=models.CharField(blank=True, null=True, max_length=100, verbose_name='user_account')
	total_followers=models.CharField(max_length=100, blank=True, null=True, verbose_name='user_package')
	total_follows=models.CharField(max_length=100, blank=True,null=True)
	pending_follow_request=models.CharField(max_length=100,blank=True,null=True)
	def __str__(self):
		return self.insta_user.email_account