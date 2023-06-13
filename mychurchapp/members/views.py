from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView

from accounts.models import ChurchMemberProfile
from .mixins import GroupRequiredMixin

from django.utils import timezone
from django.core.mail import send_mail
from django.views import View
from .models import ChurchMember, Newsletter

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from .forms import PrayerRequestForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Event
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import EventForm
from .models import Event
from django.views.generic import DetailView

from django.views.generic import ListView
from .models import Event
from django.contrib.auth import login as auth_login

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ChurchAttendance
from .forms import ChurchAttendanceForm
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser

# views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ServiceGroupMeeting
from .forms import ServiceGroupMeetingForm
from django.urls import reverse_lazy
# Now create a new view for email confirmation:
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import CellGroup
  
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth import logout
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from accounts.models import Profile
from accounts.forms import ProfilePictureForm

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth.models import Group

from django.views.generic import TemplateView
from .models import Testimonial

class IndexView(TemplateView):
    template_name = "members/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Handling Testimonials
        testimonials = Testimonial.objects.all()
        if not testimonials:
            # Define default testimonials
            testimonials = [
                {'text': "The community here is incredible. Since joining, I've felt a genuine connection with everyone. The workshops and events are always insightful and empowering. I'm so grateful to have found this place. Thank God", 'author': "Chris Adebajo", 'image_url': 'img/testimonia1.jpeg'},
                {'text': "I can't express enough how much this community has impacted my life. The positive environment and constant support have been crucial for my growth. I feel like I've found a  home here with dear friends.", 'author': "Mabel Yankey", 'image_url':  "img/testimonial4.jpeg"},
                {'text': "This place is a treasure trove of inspiration and knowledge. I've learned so much and met amazing people. The activities are fun and the leadership is exemplary. Joining this community has enriched my life. I appreciate God for this.", 'author': "Teddy O", 'image_url': "img/testimonial2.jpeg"},
            ]
        context['testimonials'] = testimonials

       # Handling Carousel Images
        carousel_images = CarouselImage.objects.all()
        if not carousel_images:
            # Define default carousel images
            carousel_images = [
                {'image_url': "img/testimonia1.jpeg"},
                {'image_url': "img/testimonial4.jpeg"},
                {'image_url': "img/testimonial2.jpeg"},
                {'image_url': "img/testimonial4.jpeg"},
                {'image_url': "img/testimonial2.jpeg"},
            ]
            context['is_default_carousel'] = True
        else:
            context['is_default_carousel'] = False
            
        context['carousel_images'] = carousel_images
        
        return context


class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'members/create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)  # Don't save yet
        user.is_active = False  # Deactivate account till it is confirmed
        user.save()

        # Add user to Members group
        group = Group.objects.get(name='Members')
        user.groups.add(group)

        # Rest of the method as before...
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = self.request.get_host()
        mail_subject = 'Activate your account.'
        message = render_to_string('members/acc_active_email.html', {
            'user': user,
            'domain': current_site,
            'uid': uid,
            'token': token,
        })
        send_mail(mail_subject, message, 'HOST_EMAIL', [user.email])
        
        return redirect('email_verification_sent')





def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # return redirect to 'account activated message' or log-in
        else:
            # invalid token
            pass
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    return redirect('create_user')  # or your desired url


class EmailVerificationSentView(TemplateView):
    template_name = "members/email_verification_sent.html"





class CustomLoginView(LoginView):
    template_name = 'members/login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())

        # If it's user's first login, redirect to password change
        if self.request.user.is_first_login:
            return redirect(reverse_lazy('password_change'))  # Use your password change URL pattern name here
        
        # Identify user's group
        if self.request.user.groups.filter(name='Admin').exists():
            return redirect(reverse('admin_dashboard'))
        elif self.request.user.groups.filter(name='Finance').exists():
            return redirect(reverse('finance_admin_dashboard'))
        elif self.request.user.groups.filter(name='Leaders').exists():
            return redirect(reverse('leaders_dashboard'))
        else:  # We assume that if not in any other group, user is a Member
            return redirect(reverse('members_dashboard'))

        
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'members/password_change_form.html'
    
    def form_valid(self, form):
        self.request.user.is_first_login = False
        self.request.user.save()
        return super().form_valid(form)

class ProfilePictureUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfilePictureForm
    template_name = 'members/profile_picture_form.html'

    def get_object(self):
        Profile.objects.get_or_create(user=self.request.user)
        return self.request.user.profile


    def get_success_url(self):
        return reverse('update_profile_picture')



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class MembersDashboardView(TemplateView):
    template_name = 'members/members_dashboard.html'
    
class LeadersDashboardView(TemplateView):
    template_name = 'members/leaders_dashboard.html'
    
class FinanceAdminDashboardView(TemplateView):
    template_name = 'members/finance_admin_dashboard.html'  
    
class AdminDashboardView(TemplateView):
    template_name = 'members/admin_dashboard.html'


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'members/password_change_done.html'


class CellGroupListView(ListView):
    model = CellGroup
    template_name = 'members/cellgroup_list.html'  # Update with your template

class CellGroupCreateView(CreateView):
    model = CellGroup
    fields = ('name', 'date_started', 'leader', 'secretary', 'assistant_leader', 'street_address', 'city', 'state', 'zipcode')
    template_name = 'members/cellgroup_form.html'
    success_url = reverse_lazy('cellgroup_list')

class CellGroupUpdateView(UpdateView):
    model = CellGroup
    fields = ('name', 'date_started', 'leader', 'secretary', 'assistant_leader', 'street_address', 'city', 'state', 'zipcode')
    template_name = 'members/cellgroup_form.html'
    success_url = reverse_lazy('cellgroup_list')


class CellGroupDeleteView(DeleteView):
    model = CellGroup
    template_name = 'members/cellgroup_confirm_delete.html'  # Update with your template
    success_url = reverse_lazy('cellgroup_list')



class ServiceGroupMeetingListView(ListView):
    model = ServiceGroupMeeting
    template_name = 'members/servicegroupmeeting_list.html'  # Update with your template

class ServiceGroupMeetingCreateView(CreateView):
    model = ServiceGroupMeeting
    form_class = ServiceGroupMeetingForm
    template_name = 'members/servicegroupmeeting_form.html'  # Update with your template
    success_url = reverse_lazy('servicegroupmeeting_list')  # Update to your list view URL name

class ServiceGroupMeetingUpdateView(UpdateView):
    model = ServiceGroupMeeting
    form_class = ServiceGroupMeetingForm
    template_name = 'members/servicegroupmeeting_form.html'  # Update with your template
    success_url = reverse_lazy('servicegroupmeeting_list')  # Update to your list view URL name

class ServiceGroupMeetingDeleteView(DeleteView):
    model = ServiceGroupMeeting
    template_name = 'members/servicegroupmeeting_confirm_delete.html'  # Update with your template
    success_url = reverse_lazy('servicegroupmeeting_list')  # Update to your list view URL name


# views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ServiceGroup
from .forms import ServiceGroupForm

class ServiceGroupListView(ListView):
    model = ServiceGroup
    context_object_name = 'service_groups'
    template_name = 'members/servicegroup_list.html'

class ServiceGroupCreateView(CreateView):
    model = ServiceGroup
    form_class = ServiceGroupForm
    template_name = 'members/servicegroup_form.html'
    success_url = reverse_lazy('servicegroup_list') 

class ServiceGroupUpdateView(UpdateView):
    model = ServiceGroup
    form_class = ServiceGroupForm
    template_name = 'members/servicegroup_form.html'
    success_url = reverse_lazy('servicegroup_list') 

class ServiceGroupDeleteView(DeleteView):
    model = ServiceGroup
    template_name = 'members/servicegroup_confirm_delete.html'
    success_url = reverse_lazy('servicegroup_list') 


# views.py
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CellGroupMeeting
from .forms import CellGroupMeetingForm

class CellGroupMeetingCreateView(CreateView):
    model = CellGroupMeeting
    form_class = CellGroupMeetingForm
    template_name = 'members/cellgroupmeeting_form.html'  # Update with your template
    success_url = reverse_lazy('cellgroupmeeting_list')  # Update to your list view URL name

class CellGroupMeetingUpdateView(UpdateView):
    model = CellGroupMeeting
    form_class = CellGroupMeetingForm
    template_name = 'members/cellgroupmeeting_form.html'  # Update with your template
    success_url = reverse_lazy('cellgroupmeeting_list')  # Update to your list view URL name

class CellGroupMeetingDeleteView(DeleteView):
    model = CellGroupMeeting
    template_name = 'members/cellgroupmeeting_confirm_delete.html'  # Update with your template
    success_url = reverse_lazy('cellgroupmeeting_list')  # Update to your list view URL name



class CellGroupMeetingListView(ListView):
    model = CellGroupMeeting
    template_name = 'members/cellgroupmeeting_list.html'  # Update with your template
    context_object_name = 'meetings'  # Specify the variable name used in the template



class ChurchAttendanceListView(ListView):
    model = ChurchAttendance
    template_name = 'members/churchattendance_list.html'  # replace with your own template path
    
    
class ChurchAttendanceCreateView(LoginRequiredMixin, CreateView):
    model = ChurchAttendance
    form_class = ChurchAttendanceForm
    template_name = 'members/churchattendance_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ChurchAttendanceCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('churchattendance_list')


class ChurchAttendanceUpdateView(UpdateView):
    model = ChurchAttendance
    form_class = ChurchAttendanceForm
    template_name = 'members/churchattendance_form.html'  # replace with your own template path
    success_url = reverse_lazy('churchattendance_list')

class ChurchAttendanceDeleteView(DeleteView):
    model = ChurchAttendance
    template_name = 'members/churchattendance_confirm_delete.html'  # replace with your own template path
    success_url = reverse_lazy('churchattendance_list')


# views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ChurchAttendanceRecord

class ChurchAttendanceRecordListView(ListView):
    model = ChurchAttendanceRecord
    template_name = 'members/attendance_record_list.html'  # Update with your template

class ChurchAttendanceRecordCreateView(CreateView):
    model = ChurchAttendanceRecord
    fields = ('member', 'church_attendance', 'date', 'service_type', 'other_service_type')
    template_name = 'members/churchattendance_form.html'  # Update with your template
    success_url = reverse_lazy('attendance_record_list')  # Update to your list view URL name

class ChurchAttendanceRecordUpdateView(UpdateView):
    model = ChurchAttendanceRecord
    fields = ('member', 'church_attendance', 'date', 'service_type', 'other_service_type')
    template_name = 'members/churchattendance_form.html'  # Update with your template
    success_url = reverse_lazy('attendance_record_list')  # Update to your list view URL name

class ChurchAttendanceRecordDeleteView(DeleteView):
    model = ChurchAttendanceRecord
    template_name = 'members/attendance_record_confirm_delete.html'  # Update with your template
    success_url = reverse_lazy('attendance_record_list')  # Update to your list view URL name
    

# views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CovenantHourOfPrayer
from .forms import CovenantHourOfPrayerForm

class CovenantHourOfPrayerListView(ListView):
    model = CovenantHourOfPrayer
    template_name = 'members/covenanthourofprayer_list.html'  # Update with your template

class CovenantHourOfPrayerCreateView(CreateView):
    model = CovenantHourOfPrayer
    form_class = CovenantHourOfPrayerForm
    template_name = 'members/covenanthourofprayer_form.html'  # Update with your template
    success_url = reverse_lazy('covenanthourofprayer_list')  # Update to your list view URL name

class CovenantHourOfPrayerUpdateView(UpdateView):
    model = CovenantHourOfPrayer
    form_class = CovenantHourOfPrayerForm
    template_name = 'members/covenanthourofprayer_form.html'  # Update with your template
    success_url = reverse_lazy('covenanthourofprayer_list')  # Update to your list view URL name

class CovenantHourOfPrayerDeleteView(DeleteView):
    model = CovenantHourOfPrayer
    template_name = 'members/covenanthourofprayer_confirm_delete.html'  # Update with your template
    success_url = reverse_lazy('covenanthourofprayer_list')  # Update to your list view URL name



from django.views.generic import CreateView, ListView, UpdateView
from .models import ChurchMember
from .forms import ChurchMemberForm
from django.urls import reverse_lazy

class ChurchMemberListView(ListView):
    model = ChurchMember
    template_name = 'members/churchmember_list.html'

from django.urls import reverse_lazy
from accounts.models import ChurchMemberProfile


class ChurchMemberCreateView(CreateView):
    model = ChurchMember
    form_class = ChurchMemberForm
    template_name = 'members/churchmember_form.html'
    
    def form_valid(self, form):
        # Save the ChurchMember instance to the database
        church_member = form.save()
        # Return super class's form_valid method to redirect to success_url
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the list of church members (change this URL name if necessary)
        return reverse_lazy('churchmember_list')



class ChurchMemberUpdateView(UpdateView):
    model = ChurchMember
    form_class = ChurchMemberForm
    template_name = 'members/churchmember_form.html'

    def form_valid(self, form):
        # Manually save the ChurchMember object
        church_member = form.save()
        
        # Handle the profile picture in the update view
        profile_picture = self.request.FILES.get('profile_picture')
        if profile_picture:
            # Get or create ChurchMemberProfile and set church_member
            church_member_profile, created = ChurchMemberProfile.objects.get_or_create(church_member=church_member)
            church_member_profile.profile_picture = profile_picture
            church_member_profile.church_member = church_member
            church_member_profile.save()
            
        # Return success URL
        return HttpResponseRedirect(self.get_success_url())




        # Return the response object
        return response


    def get_success_url(self):
        return reverse_lazy('churchmember_list')




class ChurchMemberDeleteView(DeleteView):
    model = ChurchMember
    template_name = 'members/churchmember_confirm_delete.html' # update this to your actual template path
    success_url = reverse_lazy('churchmember_list')



class SendInactiveMemberNewslettersView(View):
    def get(self, request, *args, **kwargs):
        inactive_members = ChurchMember.objects.filter(is_inactive=True)

        for member in inactive_members:
            newsletter = Newsletter.objects.get(subject='Inactive Member')
            # Retrieve member's email address or contact information
            # Send the newsletter to the member using Django's email sending capabilities or a third-party email service

        new_members = ChurchMember.objects.filter(date_joined=timezone.now().date())
        for member in new_members:
            newsletter = Newsletter.objects.get(subject='Thank You for Worshiping')
            # Retrieve member's email address or contact information
            # Send the newsletter to the member using Django's email sending capabilities or a third-party email service

        first_time_attendees = ChurchMember.objects.filter(churchattendancerecord__service_type='SUN')
        for member in first_time_attendees:
            if member.date_joined == timezone.now().date():
                newsletter = Newsletter.objects.get(subject='Thank You for Attending Church')
                # Retrieve member's email address or contact information
                # Send the newsletter to the member using Django's email sending capabilities or a third-party email service

        return HttpResponse('Newsletters sent to inactive members, new members, and first-time attendees')



from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Newsletter

class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'members/newsletter_list.html'
    context_object_name = 'newsletters'

class NewsletterCreateView(CreateView):
    model = Newsletter
    template_name = 'members/newsletter_form.html'
    fields = ['subject', 'content', 'recipients']
    success_url = reverse_lazy('newsletter_list')

class NewsletterUpdateView(UpdateView):
    model = Newsletter
    template_name = 'members/newsletter_form.html'
    fields = ['subject', 'content', 'recipients']
    success_url = reverse_lazy('newsletter_list')

class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = 'members/newsletter_confirm_delete.html'
    success_url = reverse_lazy('newsletter_list')


from django.views.generic.edit import CreateView
from members.models import ConnectCard
from members.forms import ConnectCardForm

from django.contrib import messages
from django.shortcuts import redirect

from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import send_mail
from django.conf import settings

class ConnectCardCreateView(CreateView):
    model = ConnectCard
    form_class = ConnectCardForm
    template_name = 'members/connect_card_form.html'

    def form_valid(self, form):
        # Save the form and get the ConnectCard object
        self.object = form.save()

        # Send an email notification to the HOST_EMAIL
        subject = 'New Connect Card Submitted'
        message = 'You have a new Connect Card submission. Please check the admin panel for details. Thank you and God bless.'
        recipient_list = [settings.HOST_EMAIL]
        send_mail(subject, message, settings.HOST_EMAIL, recipient_list)

        # Display success message
        messages.success(self.request, 'Form received. Thank you for worshiping with us. - Pst. Francis Yankey')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('connectcard_success')



from django.views.generic.base import TemplateView

class ConnectCardSuccessView(TemplateView):
    template_name = "members/connect_card_success.html"


from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.shortcuts import render, redirect

class BecomeAMemberView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'members/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            recipients = [settings.HOST_EMAIL]

            send_mail(subject, message, sender, recipients)
            return redirect('contact_thanks')

from django.shortcuts import render

def contact_thanks(request):
    return render(request, 'members/contact_thanks.html')




class EventView(ListView):
    model = Event
    template_name = 'members/event_view.html'
    context_object_name = 'events'
    ordering = ['-date'] #This will order your events by date in descending order. Newest first.

class EventListView(ListView):
    model = Event
    template_name = 'members/event_list_view.html'
    context_object_name = 'events'
    ordering = ['-date'] #This will order your events by date in descending order. Newest first.

class EventDetailView(DetailView):
    model = Event
    template_name = 'members/event_detail.html'


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'members/event_form.html'
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EventUpdateView(UpdateView):
    model = Event
    template_name = 'members/event_form.html'
    fields = ('title', 'description', 'image', 'date', 'venue', 'preacher')
    success_url = reverse_lazy('event_list')

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'members/event_delete.html'
    success_url = reverse_lazy('event_list')


class PrayerRequestView(View):
    def get(self, request):
        form = PrayerRequestForm()
        return render(request, 'members/prayer_request.html', {'form': form})

    def post(self, request):
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = f"Name: {form.cleaned_data['name']}\n\nEmail: {form.cleaned_data['email']}\n\nPrayer Request: {form.cleaned_data['prayer_request']}"
            sender = form.cleaned_data['email']
            recipients = [settings.HOST_EMAIL]

            send_mail(subject, message, sender, recipients)
            return redirect('prayer_request_thanks')

        return render(request, 'members/prayer_request.html', {'form': form})


from django.views.generic import TemplateView

class PrayerRequestThanksView(TemplateView):
    template_name = 'members/prayer_request_thanks.html'


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import CarouselImage

class CarouselImageListView(GroupRequiredMixin, ListView):
    group_required = ['GroupLevel_4']
    model = CarouselImage
    template_name = 'members/carousel_image_list.html'
    context_object_name = 'carousel_images'


class CarouselImageCreateView(GroupRequiredMixin, CreateView):
    group_required = ['GroupLevel_4']
    model = CarouselImage
    fields = ['image', 'alt_text']
    template_name = 'members/carousel_image_form.html'
    success_url = reverse_lazy('carousel_image_list')


class CarouselImageUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ['GroupLevel_4']
    model = CarouselImage
    fields = ['image', 'alt_text']
    template_name = 'members/carousel_image_update.html'
    success_url = reverse_lazy('carousel_image_list')


class CarouselImageDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ['GroupLevel_4']
    model = CarouselImage
    template_name = 'members/carousel_image_confirm_delete.html'
    success_url = reverse_lazy('carousel_image_list')


class TestimonialListView(GroupRequiredMixin, ListView):
    group_required = ['GroupLevel_4']
    model = Testimonial
    template_name = 'members/testimonials.html'
    context_object_name = 'testimonials'


class TestimonialCreateView(GroupRequiredMixin, CreateView):
    group_required = ['GroupLevel_4']
    model = Testimonial
    fields = ['image', 'text', 'author']
    template_name = 'members/testimonial_form.html'
    success_url = reverse_lazy('testimonials')


class TestimonialUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ['GroupLevel_4']
    model = Testimonial
    fields = ['image', 'text', 'author']
    template_name = 'members/testimonial_form.html'
    success_url = reverse_lazy('testimonials')


class TestimonialDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ['GroupLevel_4']
    model = Testimonial
    template_name = 'members/testimonial_confirm_delete.html'
    success_url = reverse_lazy('testimonials')


from django.views.generic import DetailView
from .models import Testimonial

class TestimonialDetailView(DetailView):
    model = Testimonial
    template_name = 'members/testimonial_detail.html'
    context_object_name = 'testimonial'

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages


def baptism_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Sending email to the host
        send_mail(
            subject=f'Baptism Registration by {name}',
            message=f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.HOST_EMAIL],
        )
        
        messages.success(request, 'Your registration has been successfully submitted.')
        return redirect('baptism')
    
    return render(request, 'members/baptism.html')





from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .models import Announcement

# The ListView from before

class AnnouncementCreateView(CreateView):
    model = Announcement
    fields = ['title', 'image', 'message']
    template_name = 'members/announcement_form.html'
    success_url = reverse_lazy('announcement_list')

class AnnouncementUpdateView(UpdateView):
    model = Announcement
    fields = ['title', 'image', 'message']
    template_name = 'members/announcement_form.html'
    success_url = reverse_lazy('announcement_list')

class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = 'members/announcement_confirm_delete.html'
    success_url = reverse_lazy('announcement_list')

class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'members/announcement_detail.html'


from django.views.generic import ListView
from .models import Announcement

from django.views.generic import ListView
from .models import Announcement

# In views.py
from django.views.generic.list import ListView
from .models import Announcement

class AnnouncementListView(ListView):
    model = Announcement
    template_name = "announcements/announcement_list.html"
    context_object_name = "announcements"
    
class AnnouncementDisplayView(ListView):
    model = Announcement
    template_name = 'members/announcement_display.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not queryset.exists():
            queryset = [
                {'title': "Midweek Communion Service", 'message': "Our mid-week communion service holds this coming Wednesday...", 'image_url': 'img/testimonia1.jpeg'},
                {'title': "Winners’ Satellite Fellowship", 'message': "Our House-to-House fellowship holds on Saturday...", 'image_url': "img/testimonial4.jpeg"},
                {'title': "Sunday Service at WCIN", 'message': " Our power pack  Sunday service aims to reveal the mystery embeded in the word...", 'image_url': "img/testimonial2.jpeg"},
            ]
        return queryset

        

# views.py
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChurchMember, ChurchAttendanceRecord, ChurchAttendance
from django.utils import timezone
from django.shortcuts import render

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView

class MemberAttendanceView(TemplateView):
    template_name = 'members/member_attendance.html'
    paginate_by = 16
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members = ChurchMember.objects.all()
        
        paginator = Paginator(members, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['members'] = page_obj
        return context

@csrf_exempt
def register_attendance(request):
    member_id = request.POST.get('member_id')
    service_type = request.POST.get('service_type', 'SUN')
    
    try:
        member = ChurchMember.objects.get(id=member_id)
    except ChurchMember.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Member not found'})
    
    today = timezone.now().date()
    church_attendance, created = ChurchAttendance.objects.get_or_create(date=today, service_type=service_type)
    
    attendance_record = ChurchAttendanceRecord()
    attendance_record.member = member
    attendance_record.church_attendance = church_attendance
    attendance_record.date = timezone.now()
    attendance_record.service_type = service_type
    
    if service_type == 'OTHER':
        other_service_type = request.POST.get('other_service_type')
        attendance_record.other_service_type = other_service_type
    
    attendance_record.save()
    
    return JsonResponse({'status': 'success'})

import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import CreateView, UpdateView
from .models import Finance
from .forms import FinanceForm

class FinanceCreateView(LoginRequiredMixin, CreateView):
    model = Finance
    form_class = FinanceForm
    template_name = 'members/finance_form.html'
    success_url = reverse_lazy('finance_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = False
        return context

    def form_valid(self, form):
        # Validate date
        if form.cleaned_data['date'] > datetime.date.today():
            raise forms.ValidationError("Date cannot be in the future.")

        # Validate amounts
        for amount in [
            form.cleaned_data['tithe'],
            form.cleaned_data['shiloh'],
            form.cleaned_data['thanksgiving'],
            form.cleaned_data['welfare'],
            form.cleaned_data['project'],
        ]:
            if amount < 0:
                raise forms.ValidationError("Amount cannot be negative.")

        # Set the created_by attribute
        form.instance.created_by = self.request.user

        return super().form_valid(form)


from django.urls import reverse_lazy

class FinanceUpdateView(UpdateView):
    model = Finance
    form_class = FinanceForm
    template_name = 'members/finance_form.html'
    success_url = reverse_lazy('finance_list') # Redirect back to finance list after successful update
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context

    
    def form_valid(self, form):
        # Validate date
        if form.cleaned_data['date'] > datetime.date.today():
            raise forms.ValidationError("Date cannot be in the future.")
        
        # Validate amounts
        for amount in [
            form.cleaned_data['offering'],
            form.cleaned_data['tithe'],
            form.cleaned_data['shiloh'],
            form.cleaned_data['thanksgiving'],
            form.cleaned_data['welfare'],
            form.cleaned_data['project'],
        ]:
            if amount < 0:
                raise forms.ValidationError("Amount cannot be negative.")
        
        # Set the updated_by attribute
        form.instance.updated_by = self.request.user
        
        return super().form_valid(form)


class FinanceListView(ListView):
    model = Finance
    template_name = 'members/finance_list.html'
    context_object_name = 'finances'


class FinanceDetailView(DetailView):
    model = Finance
    template_name = 'members/finance_detail.html'

class FinanceDeleteView(DeleteView):
    model = Finance
    template_name = 'members/finance_delete.html'
    success_url = reverse_lazy('finance_list')  # Redirect to the list view after deletion


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import TithlyOffering
from .forms import TithlyOfferingForm
class TithlyOfferingListView(ListView):
    model = TithlyOffering
    template_name = 'members/tithly_offering_list.html'
    context_object_name = 'tithly_offerings'


from django.views.generic.edit import CreateView

from django.views.generic.edit import CreateView

class TithlyOfferingCreateView(CreateView):
    model = TithlyOffering
    form_class = TithlyOfferingForm
    template_name = 'members/tithly_offering_form.html'
    success_url = reverse_lazy('tithly_offering_list')

    def form_valid(self, form):
        # Get the initial values for the form
        initial = super().get_initial()

        # Create the object
        self.object = form.save(commit=False)
        # Save the object
        self.object.save()

        return super().form_valid(form)


    
from django.views.generic.edit import UpdateView



class TithlyOfferingUpdateView(UpdateView):
    model = TithlyOffering
    form_class = TithlyOfferingForm
    template_name = 'members/tithly_offering_form.html'
    success_url = reverse_lazy('tithly_offering_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
    # Validate date
        if form.cleaned_data['date'] > datetime.date.today():
            raise forms.ValidationError("Date cannot be in the future.")

        # Validate amounts
        for amount in [
            form.cleaned_data['offering'],
            form.cleaned_data['tithe'],
            form.cleaned_data['shiloh'],
            form.cleaned_data['thanksgiving'],
            form.cleaned_data['welfare'],
            form.cleaned_data['project'],
        ]:
            if amount < 0:
                raise forms.ValidationError("Amount cannot be negative.")

        # Set the updated_by attribute
        form.instance.updated_by = self.request.user

        # Save the object
        form.save()

        return super().form_valid(form)

    
class TithlyOfferingDeleteView(DeleteView):
    model = TithlyOffering
    template_name = 'members/tithly_offering_delete.html'
    success_url = reverse_lazy('tithly_offering_list')

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Expense, CustomCategory
from .forms import ExpenseForm, CustomCategoryForm  # Assuming you have created forms for these models

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'members/expense_form.html'
    success_url = reverse_lazy('expense_list')

class ExpenseListView(ListView):
    model = Expense
    template_name = 'members/expense_list.html'
    context_object_name = 'expenses'

class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'members/expense_form.html'
    success_url = reverse_lazy('expense_list')

class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'members/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')

class CustomCategoryCreateView(CreateView):
    model = CustomCategory
    form_class = CustomCategoryForm
    template_name = 'members/customcategory_form.html'
    success_url = reverse_lazy('customcategory_list')

class CustomCategoryListView(ListView):
    model = CustomCategory
    template_name = 'members/customcategory_list.html'
    context_object_name = 'customcategories'

class CustomCategoryUpdateView(UpdateView):
    model = CustomCategory
    form_class = CustomCategoryForm
    template_name = 'members/customcategory_form.html'
    success_url = reverse_lazy('customcategory_list')

class CustomCategoryDeleteView(DeleteView):
    model = CustomCategory
    template_name = 'members/customcategory_confirm_delete.html'
    success_url = reverse_lazy('customcategory_list')


from django.views import View
from django.shortcuts import render
from .models import Finance, TithlyOffering
from .forms import ReportForm

class FinanceRecordReportView(View):
    
    def get(self, request):
        form = ReportForm()
        return render(request, 'members/finance_report.html', {'form': form})
    
    def post(self, request):
        form = ReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Fetch records for the given date range
            finances = Finance.objects.filter(date__range=[start_date, end_date])
            tithly_offerings = TithlyOffering.objects.filter(date__range=[start_date, end_date])
            expenses = Expense.objects.filter(date__range=[start_date, end_date])

            # Calculate totals for finances
            finance_totals = {
                "offering": sum(f.offering for f in finances),
                "tithe": sum(f.tithe for f in finances),
                "shiloh": sum(f.shiloh for f in finances),
                "thanksgiving": sum(f.thanksgiving for f in finances),
                "welfare": sum(f.welfare for f in finances),
                "project": sum(f.project for f in finances),
                "total_income": sum(f.total_income for f in finances),
            }

            # Calculate totals for TithlyOffering
            tithly_totals = {
                "offering": sum(t.offering for t in tithly_offerings),
                "tithe": sum(t.tithe for t in tithly_offerings),
                "shiloh": sum(t.shiloh for t in tithly_offerings),
                "thanksgiving": sum(t.thanksgiving for t in tithly_offerings),
                "welfare": sum(t.welfare for t in tithly_offerings),
                "project": sum(t.project for t in tithly_offerings),
                "total_income": sum(t.total_income for t in tithly_offerings),
            }
            
            # Calculate grand totals
            grand_totals = {
                "offering": finance_totals["offering"] + tithly_totals["offering"],
                "tithe": finance_totals["tithe"] + tithly_totals["tithe"],
                "shiloh": finance_totals["shiloh"] + tithly_totals["shiloh"],
                "thanksgiving": finance_totals["thanksgiving"] + tithly_totals["thanksgiving"],
                "welfare": finance_totals["welfare"] + tithly_totals["welfare"],
                "project": finance_totals["project"] + tithly_totals["project"],
                "total_income": finance_totals["total_income"] + tithly_totals["total_income"],
            }

            # Inside your post method after tithly_totals

            # Calculate grand total expenses
            grand_total_expenses = sum(e.amount for e in Expense.objects.filter(date__range=[start_date, end_date]))
            # Calculate grand total net income
            grand_total_net_income = grand_totals['total_income'] - grand_total_expenses

            return render(request, 'members/finance_report.html', {
                'form': form,
                'finances': finances,
                'tithly_offerings': tithly_offerings,
                'finance_totals': finance_totals,
                'tithly_totals': tithly_totals,
                'grand_totals': grand_totals,
                'grand_total_expenses': grand_total_expenses,
                'grand_total_net_income': grand_total_net_income
            })




from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import InviteFriendForm

class InviteFriendView(View):
    def get(self, request):
        form = InviteFriendForm()
        return render(request, 'members/invite_friend.html', {'form': form})

    def post(self, request):
        form = InviteFriendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            sender_name = form.cleaned_data['sender_name']

            message = f"""Dear {name},

I hope this card finds you well.

I am writing to invite you to join me at Winners Chapel International Nashville for a Sunday service or Wednesday service. We meet at 9am on Sundays and 6pm on Wednesdays at 5270 Murfreesboro Road, La Vergne, TN 37086.

Winners Chapel International is a non-denominational church that is committed to teaching the Word of God and helping people grow in their faith. We believe that everyone has a purpose in life and that God has a plan for each of us. We want to help you discover your purpose and fulfill it.

Our Sunday services are a time of worship, teaching, and fellowship. We have a variety of music ministries that will help you to worship God in spirit and in truth. Our teaching is based on the Word of God and is designed to help you grow in your faith. Our fellowship is a time to connect with other believers and build relationships.

I would love for you to join me at Winners Chapel International. I believe that you will find a warm welcome and a place where you can grow in your faith.

Sincerely,
{sender_name}
"""

            send_mail(
                'Invitation to Winners Chapel International',
                message,
                'HOST_EMAIL', # Sender email
                [email], # Recipient email
                fail_silently=False,
            )
            
            return HttpResponse('Email sent successfully')

        return HttpResponse('Invalid form data')


class LandingPageView(TemplateView):
    template_name = 'members/landing_page.html'