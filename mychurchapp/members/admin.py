from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser
from accounts.models import ChurchMemberProfile

class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'contact_number', 'address', 'baptism_date', 'is_staff']
    search_fields = ['email', 'username']
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CustomUser, CustomUserAdmin)


from django.contrib import admin
from .models import (Announcement, CarouselImage, CellGroup, CellGroupMeeting, ChurchAttendance, ChurchAttendanceRecord, ConnectCard,
                     CovenantHourOfPrayer, CustomCategory, Expense, Finance, Newsletter, ServiceGroup, ChurchMember, ServiceGroupMeeting, Event, Testimonial, TithlyOffering )
from accounts.models import Profile

@admin.register(CellGroup)
class CellGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(ChurchMember)
class ChurchMemberAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(ChurchAttendance)
class ChurchAttendanceAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceGroupMeeting)
class ServiceGroupMeetingAdmin(admin.ModelAdmin):
    pass

@admin.register(CellGroupMeeting)
class CellGroupMeetingAdmin(admin.ModelAdmin):
    pass

@admin.register(CovenantHourOfPrayer)
class CovenantHourOfPrayerAdmin(admin.ModelAdmin):
    pass

@admin.register(ChurchAttendanceRecord)
class ChurchAttendanceRecordAdmin(admin.ModelAdmin):
    pass

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    pass

@admin.register(ConnectCard)
class ConnectCardAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(CarouselImage) # 
class  CarouselImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Testimonial) # CarouselImage
class TestimonialAdmin(admin.ModelAdmin):
    pass
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):  
    pass

@admin.register(ChurchMemberProfile)
class ChurchMemberProfileAdmin(admin.ModelAdmin):
    pass 

@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    pass

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomCategory)
class CustomCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(TithlyOffering)
class TithlyOfferingAdmin(admin.ModelAdmin):
    pass