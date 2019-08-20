from django.shortcuts import render,HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import *
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from random import *
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from .insta import get_data
import json

def LogoutView(request):
	logout(request)
	return HttpResponseRedirect('/')

class HomePage(TemplateView):
	template_name='index.html'
	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,locals())

class Thankyou(TemplateView):
	template_name='thankyou.html'
	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,locals())
		
class Login(TemplateView):
	template_name='login.html'
	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,locals())

	def post(self, request, *args, **kwargs):
		email = request.POST.get('login_email')	
		password = request.POST.get('login_password')
		try:
			user = User.objects.get(email=email)
			userauth = authenticate(username=user.username, password=password)
			if userauth:
				login(request, user, backend='django.contrib.auth.backends.ModelBackend')
				if request.user.is_authenticated:
						return HttpResponseRedirect('select-package')	
				else:
					return HttpResponseRedirect('login')
			else:
				messages.error(request,'Incorrect password  given.')
				return HttpResponseRedirect('login')
		except User.DoesNotExist as e:
			print(e)
			messages.error(request,'Incorrect email address given.')
			return HttpResponseRedirect('login')
		
class Register(TemplateView):
	template_name='register.html'
	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,locals())

	def post(self,request,*args, **kwargs):	
		email = request.POST.get("email")
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		password=request.POST.get('password')
		try:
			user = User.objects.get(email=email)
			messages.info(request,'This email already exists. Use another email.')
			return HttpResponseRedirect('register')
		except User.DoesNotExist:
			user = User.objects.create_user(
				username = email,
				email = email,
				password=password
			)
			user.first_name = first_name
			user.last_name = last_name
			user.is_active = True
			user.save()	
			return HttpResponseRedirect('login')

def mailSend(subject, recipient_list, message="", html_message=""):
	try:
		email_from = settings.EMAIL_HOST_USER
		send_mail( subject, message, email_from, recipient_list, html_message=html_message )
		return True
	except Exception as e:
		print(str(e))
		return False

class ForgotPasswordView(TemplateView):
	template_name='forget.html'
	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,locals())

	def post(self,request):
		email=request.POST.get('forgot_email')
		print(email)
		try:
			user = User.objects.get(email=email)
			code = randint(100000, 999999) 
			fg_pwd = ForgetPassword(user_id=user.id, code=code)
			fg_pwd.save()
			link = settings.BASE_URL+"/recover-password"

			content_html = render_to_string("mail/send_code.html", {'link':link,'code':code})
			recipients = [email]
			subject = "Reset Password"
			send_status = mailSend(subject, recipients, html_message=content_html)
			if send_status:
				messages.success(request,'Your request has been received.Please look for an email from InstaAuto to change password.Thank you.')
			else:
				messages.error(request,'Some error occur. Retry or contact with administrator.')
		except User.DoesNotExist:
			messages.error(request,'This email address is not registred.')
		except Exception as e:
			raise e
			messages.error(request,'Some error occur. Retry or contact with administrator.')
		return HttpResponseRedirect('forgot-password')

class ResetPassword(TemplateView):
	template_name='reset_password.html'
	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,locals())
	def post(self,request,*args,**kwargs):
		code = request.POST.get('code')
		pwd=request.POST.get('password')
		try:
			u = ForgetPassword.objects.get(code=code)			
			u.user.set_password(pwd)
			u.user.save()	
			messages.success(request,"Your password is changed successfully try to login.")	
			return redirect('login')
		except Exception as e:
			print(str(e))
			messages.error(request,"Invaild code.")	
			return HttpResponseRedirect('recover-password')
		

		
class ContactUs(TemplateView):
	template_name='contact.html'
	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,locals())
	def post(self,request):
		contact_email=request.POST.get('contact_email')
		email_subject=request.POST.get('email_subject')
		email_desc=request.POST.get('email_desc')
		content_html = render_to_string("mail/contact_us.html", locals())
		recipients = ['kishanaviox@gmail.com']
		subject = "Contact-Us New Request."
		send_status = mailSend(subject, recipients, html_message=content_html)
		if send_status:
			messages.success(request,'Your request has been received.Thank you.')
		else:
			messages.error(request,'Some error occur. Retry or contact with administrator.')
		return HttpResponseRedirect('contact-us')
class Profile(TemplateView):
	template_name='profile.html'
	def get(self,request,*args,**kwargs):

		return render(request,self.template_name,locals())

class AboutUs(object):
	template_name='about_us.html'
	def get(self,request,*args,**kwargs):
		return render(request, self.template_name,locals())	
		
class SelectPackage(TemplateView):
	template_name='select_package.html'
	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,locals())

class BuyPlan(TemplateView):
	template_name='buy_plan.html'
	def get(self,request,*args,**kwargs):
		price=''
		number_of_account=int(request.GET.get('number_of_account'))
		selected_package=request.GET.get('selected_package')
		if selected_package == 'standard':
			price=15*int(number_of_account)
		if selected_package == 'premium':
			price=20*int(number_of_account)
		try:
			pack_obj=UserPackage(
				user=request.user,
				user_account=number_of_account,
				user_package=selected_package
				)
			pack_obj.save()
		except Exception as e:
			raise e
		host = request.get_host()
		paypal_dict  = {
			"cmd": "_xclick-subscriptions",
			'business': settings.PAYPAL_RECEIVER_EMAIL,
			"a3": price,  # monthly price
			"p3": '1',  # duration of each unit (depends on unit)
			"t3": 'M',  # duration unit ("M for Month")
			"src": "1",  # make payments recur
			"sra": "1",  # reattempt payment on payment error
			"no_note": "1",  # remove extra notes (optional)
			'item_name': 'Content subscription',
			'custom': 1,     # custom data, pass something meaningful here
			'currency_code': 'USD',
			'notify_url': 'http://{}{}'.format(host,
				reverse('profile')),
			'return_url': 'http://{}{}'.format(host,
				reverse('thankyou')),
			'cancel_return': 'http://{}{}'.format(host,
				reverse('login')),
		}

		form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
		selected_package=UserPackage.objects.filter(user=request.user).order_by('-id')[0]
		return render(request,self.template_name,locals())


	def post(self,request,*args,**kwargs):
		response={}
		print("000000000090900000000000")
		print(request.POST)
		try:

			email=request.POST.get('email')
			print(email)
			password=request.POST.get('password')
			print(password)
			country=request.POST.get('country')

			obj=UserAccounts(
				user=request.user,
				email_account=email,
				account_password=password,
				country=country
			)
			obj.save()

			is_data_scraped=get_data(email,password)

			if is_data_scraped:
				print("Scraped data is successfully save in database.")
				response['msg']='Account Testes Successfully.Thanks.'
				response['status']=True
				
			else:
				print("Error in Scraped data or login.")
				response['msg']='There is some error, while testing you account.Please try again later or use another Insta account.Thanks you.'
				response['status']=False

		except Exception as e:
			raise e
			print("----Exception in Scraped data or login.----")
			response['msg']='There is some error, Please contact with administrator.Thanks.'
			response['status']=False
		return HttpResponse(json.dumps(response),content_type="application/json")