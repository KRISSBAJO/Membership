from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AdminDashboardView, AnnouncementCreateView, AnnouncementDeleteView, AnnouncementDetailView, AnnouncementDisplayView, AnnouncementListView, AnnouncementUpdateView, BecomeAMemberView, CarouselImageCreateView, CarouselImageDeleteView, CarouselImageListView, CarouselImageUpdateView, CellGroupCreateView, CellGroupDeleteView, CellGroupListView, CellGroupMeetingCreateView, CellGroupMeetingDeleteView, CellGroupMeetingListView, CellGroupMeetingUpdateView, CellGroupUpdateView, ChurchAttendanceCreateView, ChurchAttendanceDeleteView, ChurchAttendanceListView, ChurchAttendanceRecordCreateView, ChurchAttendanceRecordDeleteView, ChurchAttendanceRecordListView, ChurchAttendanceRecordUpdateView, ChurchAttendanceUpdateView, ChurchMemberCreateView, ChurchMemberDeleteView, ChurchMemberListView, ChurchMemberUpdateView, ConnectCardCreateView, ConnectCardSuccessView, CovenantHourOfPrayerCreateView, CovenantHourOfPrayerDeleteView, CovenantHourOfPrayerListView, CovenantHourOfPrayerUpdateView, CustomLoginView, CustomPasswordChangeDoneView, CustomPasswordChangeView, CustomUserCreateView, EmailVerificationSentView, EventCreateView, EventDeleteView, EventDetailView, EventListView, EventUpdateView, EventView, FinanceAdminDashboardView, IndexView, LeadersDashboardView, LogoutView, MemberAttendanceView, MembersDashboardView, NewsletterCreateView, NewsletterDeleteView, NewsletterListView, NewsletterUpdateView, PrayerRequestThanksView, PrayerRequestView, ProfilePictureUpdateView, ServiceGroupCreateView, ServiceGroupDeleteView, ServiceGroupListView, ServiceGroupMeetingCreateView, ServiceGroupMeetingDeleteView, ServiceGroupMeetingListView, ServiceGroupMeetingUpdateView, ServiceGroupUpdateView, TestimonialCreateView, TestimonialDeleteView, TestimonialDetailView, TestimonialListView, TestimonialUpdateView, activate, baptism_view, contact_thanks, register_attendance

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create_user/', CustomUserCreateView.as_view(), name='create_user'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='members/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='members/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='members/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='members/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change-done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('email_verification_sent/', EmailVerificationSentView.as_view(), name='email_verification_sent'),
    path('members_dashboard/', MembersDashboardView.as_view(), name='members_dashboard'),
    path('leaders_dashboard/', LeadersDashboardView.as_view(), name='leaders_dashboard'),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('finance_admin_dashboard/', FinanceAdminDashboardView.as_view(), name='finance_admin_dashboard'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('update_profile_picture/', ProfilePictureUpdateView.as_view(), name='update_profile_picture'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # URLS for cellgroup & CellGroupMeeting
    path('cellgroup/', CellGroupListView.as_view(), name='cellgroup_list'),
    path('cellgroup/new/', CellGroupCreateView.as_view(), name='cellgroup_new'),
    path('cellgroup/<int:pk>/edit/', CellGroupUpdateView.as_view(), name='cellgroup_edit'),
    path('cellgroup/<int:pk>/delete/', CellGroupDeleteView.as_view(), name='cellgroup_delete'),
    
    path('cellgroupmeeting/', CellGroupMeetingListView.as_view(), name='cellgroupmeeting_list'),
    path('cellgroupmeeting/new/', CellGroupMeetingCreateView.as_view(), name='cellgroupmeeting_create'),
    path('cellgroupmeeting/<int:pk>/edit/', CellGroupMeetingUpdateView.as_view(), name='cellgroupmeeting_update'),
    path('cellgroupmeeting/<int:pk>/delete/', CellGroupMeetingDeleteView.as_view(), name='cellgroupmeeting_delete'),
    
    
    path('servicegroup/', ServiceGroupListView.as_view(), name='servicegroup_list'),
    path('servicegroup/new/', ServiceGroupCreateView.as_view(), name='servicegroup_new'),
    path('servicegroup/<int:pk>/edit/', ServiceGroupUpdateView.as_view(), name='servicegroup_edit'),
    path('servicegroup/<int:pk>/delete/', ServiceGroupDeleteView.as_view(), name='servicegroup_delete'),

    
    path('servicegroupmeeting/', ServiceGroupMeetingListView.as_view(), name='servicegroupmeeting_list'),
    path('servicegroupmeeting/new/', ServiceGroupMeetingCreateView.as_view(), name='servicegroupmeeting_new'),
    path('servicegroupmeeting/<int:pk>/edit/', ServiceGroupMeetingUpdateView.as_view(), name='servicegroupmeeting_edit'),
    path('servicegroupmeeting/<int:pk>/delete/', ServiceGroupMeetingDeleteView.as_view(), name='servicegroupmeeting_delete'),
    
    # URLS for church attendance 
    path('churchattendance/', ChurchAttendanceListView.as_view(), name='churchattendance_list'),
    path('churchattendance/new/', ChurchAttendanceCreateView.as_view(), name='churchattendance_new'),
    path('churchattendance/<int:pk>/edit/', ChurchAttendanceUpdateView.as_view(), name='churchattendance_edit'),
    path('churchattendance/<int:pk>/delete/', ChurchAttendanceDeleteView.as_view(), name='churchattendance_delete'),
    
    path('attendance_records/', ChurchAttendanceRecordListView.as_view(), name='attendance_record_list'),
    path('attendance_records/new/', ChurchAttendanceRecordCreateView.as_view(), name='attendance_record_create'),
    path('attendance_records/<int:pk>/edit/', ChurchAttendanceRecordUpdateView.as_view(), name='attendance_record_update'),
    path('attendance_records/<int:pk>/delete/', ChurchAttendanceRecordDeleteView.as_view(), name='attendance_record_delete'),
    
    path('covenanthourofprayer/', CovenantHourOfPrayerListView.as_view(), name='covenanthourofprayer_list'),
    path('covenanthourofprayer/new/', CovenantHourOfPrayerCreateView.as_view(), name='covenanthourofprayer_create'),
    path('covenanthourofprayer/<int:pk>/edit/', CovenantHourOfPrayerUpdateView.as_view(), name='covenanthourofprayer_update'),
    path('covenanthourofprayer/<int:pk>/delete/', CovenantHourOfPrayerDeleteView.as_view(), name='covenanthourofprayer_delete'),
         
         
    path('churchmember/', ChurchMemberListView.as_view(), name='churchmember_list'),
    path('churchmember/new/', ChurchMemberCreateView.as_view(), name='churchmember_new'),
    path('churchmember/<int:pk>/edit/', ChurchMemberUpdateView.as_view(), name='churchmember_edit'),
    path('churchmember/<int:pk>/delete/', ChurchMemberDeleteView.as_view(), name='churchmember_delete'),
    
    
    path('newsletters/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/new/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletters/<int:pk>/edit/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletters/<int:pk>/delete/', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    
    path('connectcard/new/', ConnectCardCreateView.as_view(), name='connectcard_new'),
    path('connectcard/success/', ConnectCardSuccessView.as_view(), name='connectcard_success'),
    path('become-a-member/', BecomeAMemberView.as_view(), name='become_a_member'),
    path('contact_thanks/', contact_thanks, name='contact_thanks'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/new/', EventCreateView.as_view(), name='event_create'),
    path('even_list/', EventListView.as_view(), name='event_list'),
    path('event/edit/<int:pk>/', EventUpdateView.as_view(), name='event_edit'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),
    path('prayer_request/', PrayerRequestView.as_view(), name='prayer_request'),
    path('prayer-request-thanks/', PrayerRequestThanksView.as_view(), name='prayer_request_thanks'),
    
    path('carousel-images/', CarouselImageListView.as_view(), name='carousel_image_list'),
    path('carousel-images/create/', CarouselImageCreateView.as_view(), name='carousel_image_create'),
    path('carousel-images/update/<int:pk>/', CarouselImageUpdateView.as_view(), name='carousel_image_update'),
    path('carousel-images/delete/<int:pk>/', CarouselImageDeleteView.as_view(), name='carousel_image_delete'),
    
    path('testimonials/', TestimonialListView.as_view(), name='testimonials'),
    path('testimonials/create/', TestimonialCreateView.as_view(), name='testimonial_create'),
    path('testimonials/<int:pk>/update/', TestimonialUpdateView.as_view(), name='testimonial_update'),
    path('testimonials/<int:pk>/delete/', TestimonialDeleteView.as_view(), name='testimonial_delete'),
    path('testimonial/<int:pk>/', TestimonialDetailView.as_view(), name='testimonial_detail'),
    path('baptism/', baptism_view, name='baptism_registration'),

    path('announcements/', AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/create/', AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcements/update/<int:pk>/', AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('announcements/delete/<int:pk>/', AnnouncementDeleteView.as_view(), name='announcement_delete'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
    path('announcements/display/', AnnouncementDisplayView.as_view(), name='announcement_display'),
    
    path('member_attendance/', MemberAttendanceView.as_view(), name='member-attendance'),
    path('register_attendance/', register_attendance, name='register-attendance'),

    
    
]
