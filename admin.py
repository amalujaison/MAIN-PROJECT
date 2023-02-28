import csv
from django.contrib import admin
from django.http import HttpResponse, response
from .models import Account, Category, Course, Mentor, Reviews, Quiz, payment, Lesson, Video, requirements, \
    what_you_learn
from .views import Review

# from .models import Cart, CartItem


class What_you_learn_TabularInline(admin.TabularInline):
    model = what_you_learn


class Requirements_TabularInline(admin.TabularInline):
    model = requirements


class Video_TabularInline(admin.TabularInline):
    model = Video


class course_admin(admin.ModelAdmin):
    inlines = (Video_TabularInline, What_you_learn_TabularInline, Requirements_TabularInline)


admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(Lesson)
admin.site.register(Course, course_admin)
admin.site.register(what_you_learn)
admin.site.register(requirements)


# def export_details(modeladmin, request, queryset):
#      response = HttpResponse(content_type='text/csv')
#      response['Content-Disposition'] = 'attachment; filename="freecourses.csv"'
#      writer = csv.writer(response)
#      writer.writerow(['Name', 'Image', 'Category', 'Publish'])
#      courses = queryset.values_list('name', 'image', 'category', 'publish')
#      for i in courses:
#          writer.writerow(i)
#      return response
#
#
# export_details.short_description = 'Export to csv'
#
#
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ['name', 'image', 'category', 'publish']
#     actions = [export_details]
#
#
# admin.site.register(C,CourseAdmin)


def export_reg(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registration.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email', 'Password', 'Address', 'Phone',  'State', 'Country'])
    registration = queryset.values_list('email', 'password', 'address', 'phone',  'state', 'country')
    for i in registration:
        writer.writerow(i)
    return response


export_reg.short_description = 'Export to csv'


class RegAdmin(admin.ModelAdmin):
    list_display = ['email', 'password', 'address', 'phone', 'state', 'country']
    actions = [export_reg]

admin.site.register(Account,RegAdmin)
# def export_pay(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="payment.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Name', 'Account No', 'Amount'])
#     payment = queryset.values_list('Cardholdername', 'AccountNo', 'Amount')
#     for i in payment:
#         writer.writerow(i)
#     return response
#
#
# export_reg.short_description = 'Export to csv'
#
# class CateAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     actions = [export_reg]
#
#
# admin.site.register(Category,CateAdmin)

class PayAdmin(admin.ModelAdmin):
    list_display = ['Cardholdername', 'AccountNo', 'Amount']
    actions = [export_reg]


admin.site.register(payment,PayAdmin)
# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     search_fields = ("first_name__startswith", )
#     list_display = ('email','first_name','last_name','password','address',  'phone',  'state', 'country')
#     list_filter = ('first_name',)


# ...




# def export_log(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="login.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Email', 'Password'])
#     login = queryset.values_list('email', 'password')
#     for i in login:
#         writer.writerow(i)
#     return response
#
#
# export_log.short_description = 'Export to csv'
#
#
# class LogAdmin(admin.ModelAdmin):
#     list_display = ['email', 'password']
#     actions = [export_log]
#
#
# admin.site.register(user_log, LogAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = (
        'cart_id',
        'date_added'
    )


class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'cart',
        'is_active',
    )


# admin.site.register(Cart, CartAdmin)
# admin.site.register(CartItem, CartItemAdmin)



class CourseAdmin(admin.ModelAdmin):
    search_fields = ("course_name__startswith", )
    list_display = ('course_name','price','description', 'students')
    list_filter = ('course_name',)

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    search_fields = ("mentor_name__startswith", )
    list_display = ('category', 'mentor_name')
    list_filter = ('mentor_name',)




