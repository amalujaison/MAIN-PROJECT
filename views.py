import io
from _sha256 import sha256
from io import BytesIO

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from elearnapp.models import Account, Category, Course, CartItem, Reviews, Reg_Mentor, Quiz, payment, Mentor, \
    what_you_learn, requirements
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont
import os
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from cart.cart import Cart
#from hashlib import sha256
#
# from django.contrib import messages
# from django.shortcuts import render, redirect
#
#
# from elearnapp.models import user_reg, user_log, freecourses, paidcourses, pyintro, pyadva, javaintro, javaadva
#
#
# # Create your views here.
#
#
def demo(request):
    course = Course.objects.all()
    categories = Category.objects.all()
    review = Reviews.objects.all()
    return render(request, "index.html", {'course': course, 'categories': categories, 'review': review})


def home1(request):
    return render(request,"index.html")


def Home_mentor(request):
    course = Course.objects.all()
    categories = Category.objects.all()
    review = Reviews.objects.all()
    return render(request, "Home-mentor.html", {'course': course, 'categories': categories, 'review': review})



def LOGIN(request):
    return render(request,"LOGIN.html")


def base(request):
    return render(request,"base.html")
#
#
def REGISTRATION(request):
    return render(request, "REGISTRATION.html")
#
#


def Home(request):
    course = Course.objects.all()
    categories = Category.objects.all()
    review = Reviews.objects.all()
    return render(request, "Home.html", {'course': course, 'categories': categories, 'review':review})

#
# def register(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         email = request.POST['email']
#         password = request.POST['password']
#         phone = request.POST['phone']
#         address = request.POST['address']
#         state = request.POST['state']
#         country = request.POST['country']
#         paswd = sha256(password.encode()).hexdigest()
#         user = user_reg(name=name,email=email,password=paswd,phone=phone,address=address,state=state,country=country)
#         log = user_log(email=email,password=paswd)
#         user.save()
#         log.save()
#         messages.info(request, 'Your account has been successfully created..!!')
#         return redirect('LOGIN')
#     return render(request, 'REGISTRATION.html')
#
# # Login Function
#
#
# def login(request):
#     request.session.flush()
#     if 'email' in request.session:
#         return redirect(home)
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = sha256(password.encode()).hexdigest()
#         user = user_log.objects.filter(email=email,password=password2)
#         if user:
#             user_details = user_log.objects.get(email=email,password=password2)
#             email = user_details.email
#             request.session['email'] = email
#             return redirect('home')
#         else:
#             print("Invalid")
#     return render(request,'LOGIN.html')
#
#
def home(request):
    if 'email' in request.session:
        email = request.session['email']
        return render(request,'Home.html',{'email':email})
    return redirect(login)
#
#
def about1(request):
    return render(request,"about-1.html")


def about2(request):
    return render(request,"about-2.html")


def userprofile(request):
    return render(request,"user-profile.html")

def reports(request):
    return render(request,"Reports.html")


def activity(request):
    return render(request,"list-view-calendar.html")


def Messages(request):
    return render(request,"mailbox.html")


def course(request):
    return render(request,"paid courses.html")

def checkout(request,slug):
    course = Course.objects.get(slug=slug)
    return render(request,"check out1.html")




def category(request):
    obj=category.objects.all()
    return render(request,"courses-details.html",{'result':obj})

def course_detail(request):
    obj=Course.objects.all()
    return render(request,"courses-details.html",{'result':obj})


# def error(request):
#     # category = Category.objects.filter(Category)
#     return render(request, "error-404.html", {'category': category})


# def javaadv(request):
#     obj=course.objects.all()
#     return render(request,"java1.html",{'result':obj})



# Create your views here.


# def demo(request):
#     return render(request,"index.html")
#
#
# def LOGIN(request):
#     return render(request,"LOGIN.html")
#
# def REGISTRATION(request):
#     return render(request, "REGISTRATION.html")
#
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = auth.authenticate(email=email, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            # save email in session
            request.session['email'] = email

            if user.is_active:
                return redirect('Home')

            else:
                return redirect('REGISTRATION')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('LOGIN')
    return render(request, 'LOGIN.html')


def user_reg(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = email.split('@')[0]
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        if Account.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('user_reg')
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, state=state, country=country,
                                           password=password)
        user.is_user = True
        user.save()
        messages.info(request, 'Thank you for registering with us. Please Login')
        return redirect('LOGIN')
    return render(request, 'REGISTRATION.html')


def logout(request):
    auth.logout(request)
    return redirect('demo')

@login_required
def changepassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        success = user.check_password(current_password)
        if success:
            user.set_password(new_password)
            user.save()
            messages.info(request, 'Password updated successfully.')
            return redirect('LOGIN')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('changepassword')
    return render(request, 'Change_Password.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email

            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'learnmateedu@gmail.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('LOGIN')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'Forgot_Password.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('LOGIN')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('LOGIN')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')


def courses(request):
    obj = Course.objects.all()
    return render(request,"paid courses.html",{'result':obj})


def courses_mentor(request):
    obj = Course.objects.all()
    return render(request,"paid courses-mentor.html",{'result':obj})

def course_details(request,course_slug):
    single = Course.objects.get(slug=course_slug)
    point = what_you_learn.objects.all()
    req = requirements.objects.all()
    context = {
        'result': single,
        'results':point,
        'res':req,

    }
    return render(request, "course-single-v4.html",context)



# Cart functions
@login_required
def add_cart(request, id):
    if 'email' in request.session:
        item=Course.objects.get(id=id)
        user=request.session['email']
        if CartItem.objects.filter(user_id=user, cart_id=item).exists():

            return redirect('view_cart')
        else:
            price= item.price
            new_cart=CartItem(user_id=user, cart_id=item, price=price)
            new_cart.save()

            return redirect('view_cart')
    messages.success(request, "Product is added in your cart.")
    return render(LOGIN)

#
# Cart Quentity Plus Settings
# Cart View page
@login_required
def view_cart(request):
    if 'email' in request.session:
        email = request.session['email']
        # price = item.price
        # item = Course.objects.filter()
        #
        # price= item.price
        user = request.user
        cart = CartItem.objects.filter(user_id=email)
        amount = 0.0
        cart_product = [p for p in CartItem.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                subtotal = p.price+amount
            messages.warning(request, "This product is added to your cart")
            return render(request, 'Cart/cart1.html', {'cart': cart,'subtotal': subtotal})
        else:
            return render(request, 'Cart/cart1.html')


# Remove Items From Cart
def de_cart(request, id):
    email = request.session['email']
    cart = CartItem.objects.filter(user_id=email)
    if cart.exists():
        CartItem.objects.get(id=id).delete()
        messages.warning(request, "This product is removed form your cart")
        # messages.info(request, "You don't have an active order")
        return redirect('view_cart')
    # if ObjectDoesNotExist():
    #     messages.info(request, "You don't have an active order")
    #     return redirect("Home")


def profile(request):
    return render(request, "user-profile.html")

# def review(request):
#     return render(request,"mailbox-compose.html")


def update_profile(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        user_email = request.user.email

        user = Account.objects.get(email=user_email)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.address = address
        user.state = state
        user.country = country
        print(user_email)
        # if password != None and password != "":
        #     user.set_password(password)
        user.save()
        messages.success(request, 'Profile Is Successfully Updated. ')
        return redirect('profile')


def search_course(request):
    query = request.GET['query']
    course = Course.objects.filter(course_name__icontains=query)
    context = {
        'course': course,
    }
    return render(request,'search.html',context)


# def usercertificate(request):
#     if request.method == "POST":
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         user = Account.objects.filter()
#         course = Course.objects.filter().first()
#         context = {
#             'course': course,
#             'user': user,
#             'first_name': first_name,
#             'last_name': last_name,
#         }
#         return render(request,"certificate.html",context)
#
#
# # def render_to_pdf(template_src, context_dict={}):
# #     template = get_template(template_src)
# #     html  = template.render(context_dict)
# #     result = BytesIO()
# #     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
# #     if not pdf.err:
# #         return HttpResponse(result.getvalue(), content_type='application/pdf')
# #     return None
#
#
# # def usercertificate(request, course_slug):
# #     posts = Course.objects.filter(slug=course_slug).first()
# #     # category = Category.objects.filter(slug=slug)
# #     carts = CartItem.objects.filter(user=request.user, purchase=False)
# #
# #     if carts.exists():
# #         return render_to_pdf('certificate.html',{'customerName':request.user.first_name,'customerNamelast':request.user.last_name,
# #         'customerEmail':request.user.email,'carts':carts,'posts':posts})
# #
# #     return render_to_pdf('certificate.html', {'posts':posts})


# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = io.BytesIO()
#     pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return


def usercertificate(request):
    posts = Course.objects.filter().first()

    carts = CartItem.objects.filter(user=request.user, purchase=False)

    if carts.exists():

        return render_to_pdf('certificate.html',
                             {'customerName': request.user.first_name, 'customerNamelast': request.user.last_name,
                              'customerEmail': request.user.email, 'carts': carts,'posts': posts})

    return render_to_pdf('certificate.html', {'posts': posts})


def certificate(request):
    course= Course.objects.all()
    return render(request,'certificate.html',
                         {'customerName': request.user.first_name, 'customerNamelast': request.user.last_name,
                          'customerEmail': request.user.email})

def test(request):
    return render(request,"TEST.html")


def payments(request):
    if request.method == "POST":
        Cardholdername = request.POST.get('name')
        AccountNo = request.POST.get('number')
        Expiry_date = request.POST.get('exp')
        cvv = request.POST.get('cvv')
        Amount = request.POST.get('amount')
        user_email = request.user.email
        users = Account.objects.get(email=user_email)
        user = payment(Cardholdername=Cardholdername,AccountNo=AccountNo,Expiry_date=Expiry_date,cvv=cvv,Amount=Amount,user=users)
        user.save()
        messages.info(request, 'Your payment has been successfully send..!!')
        return redirect('payments')
    return render(request,"payment.html")

def Review(request):
    if request.method == "POST":
        stars = request.POST.get('stars')
        review= request.POST.get('review')
        user_email = request.user.email

        users = Account.objects.get(email=user_email)
        user = Reviews(stars=stars,review=review,user=users)
        user.save()
        messages.info(request, 'Your review has been successfully send..!!')
        return redirect('Review')
    return render(request, 'mailbox-compose.html')


# def mentor_reg(request):
#     if request.method == "POST":
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         state = request.POST.get('state')
#         country = request.POST.get('country')
#         paswd = sha256(password.encode()).hexdigest()
#         mentor = mentor_reg(first_name=first_name,last_name=last_name,email=email,password=paswd,phone=phone,address=address,state=state,country=country)
#         # log = user_log(email=email,password=paswd)
#         mentor.save()
#         # log.save()
#         messages.info(request, 'Your account has been successfully created..!!')
#         return redirect('mentor_login')
#     return render(request, 'REGISTRATION-Mentor.html')


# def mentor_login(request):
#     if request.method == 'POST':
#         email = request.POST('email')
#         password = request.POST('password')
#         print(email, password)
#         user = auth.authenticate(email=email, password=password)
#         print(user)
#
#         if user is not None:
#             auth.login(request, user)
#             # save email in session
#             request.session['email'] = email
#
#             if user.is_active:
#                 return redirect('Home')
#
#             else:
#                 return redirect('mentor_reg')
#         else:
#             messages.error(request, 'Invalid Credentials')
#             return redirect('mentor_login')
#     return render(request, 'LOGIN-Mentor.html')

def mentor_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = email.split('@')[0]
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        # if mentor_reg.objects.filter(email=email).exists():
        #     messages.error(request, 'Email already exists')
        #     return redirect('user_reg')
        user = Reg_Mentor.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, state=state, country=country,
                                           password=password)
        user.is_staff = True
        user.save()
        messages.info(request, 'Thank you for registering with us. Please Login')
        return redirect('LOGIN')
    return render(request, 'REGISTRATION-Mentor.html')

def mentor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = auth.authenticate(email=email, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            # save email in session
            request.session['email'] = email

            if user.is_user:
                return redirect('Home_mentor')

            else:
                return redirect('mentor_registration')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('mentor_login')
    return render(request, 'LOGIN-Mentor.html')

def update_profilementor(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        user_email = request.user.email

        user = Reg_Mentor.objects.get(email=user_email)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.address = address
        user.state = state
        user.country = country
        print(user_email)
        # if password != None and password != "":
        #     user.set_password(password)
        user.save()
        messages.success(request, 'Profile Is Successfully Updated. ')
        return redirect('profile')


def quiz(request):
    if request.method == 'POST':
        # print(request.POST)
        questions = Quiz.objects.filter()
        score = 0

        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            # print(total)
            print(q.Question)
            print(q.Corrans)
            print(request.POST.get(q.Corrans))

            print()
            if q.Corrans == request.POST.get(q.Corrans):
                score += 10
                correct += 1
            else:
                wrong += 1
                print(wrong)
        percent = score / (total * 10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'result.html', context)
    else:
        questions = Quiz.objects.all()
        context = {
            'questions': questions
        }
        return render(request, 'Quiz.html', context)


def quize(request,id):
    single = Quiz.objects.get(id=id)

    context = {
        'result': single,

    }
    return render(request, "Quiz.html", context)


def company_registration(request):
    if request.method == 'POST':
        company_regno = request.POST.get('first_name')
        company_name = request.POST.get('last_name')
        company_email = request.POST.get('email')
        company_phone = request.POST.get('phone')
        company_password = request.POST.get('password')
        company_address = request.POST.get('address')
        company_country = request.POST.get('country')
        # if mentor_reg.objects.filter(email=email).exists():
        #     messages.error(request, 'Email already exists')
        #     return redirect('user_reg')
        user = Reg_Mentor.objects.create_user(company_regno=company_regno, company_name=company_name, company_email=company_email, company_phone=company_phone,company_address=company_address, company_country=company_country,
                                           company_password=company_password)
        user.is_staff = True
        user.save()
        messages.info(request, 'Thank you for registering with us. Please Login')
        return redirect('LOGIN')
    return render(request, 'REGISTRATION-Mentor.html')

def company_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = auth.authenticate(email=email, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            # save email in session
            request.session['email'] = email

            if user.is_user:
                return redirect('Home_mentor')

            else:
                return redirect('mentor_registration')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('mentor_login')
    return render(request, 'LOGIN-Mentor.html')
