# forms.py
import datetime
from django import forms
from .models import ChurchMember, ServiceGroupMeeting

class ServiceGroupMeetingForm(forms.ModelForm):
    class Meta:
        model = ServiceGroupMeeting
        fields = ['date', 'service_group', 'attendees']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


# forms.py
from django import forms
from .models import ServiceGroup

class ServiceGroupForm(forms.ModelForm):
    class Meta:
        model = ServiceGroup
        fields = ['name', 'date_started', 'leader', 'secretary', 'assistant_leader']
        widgets = {
            'date_started': forms.DateInput(attrs={'type': 'date'}),
        }


# forms.py
from django import forms
from .models import CellGroupMeeting

class CellGroupMeetingForm(forms.ModelForm):
    class Meta:
        model = CellGroupMeeting
        fields = ['date', 'cell_group', 'attendees']
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import ChurchAttendance, ChurchAttendanceRecord


class ChurchAttendanceForm(forms.ModelForm):
    class Meta:
        model = ChurchAttendance
        fields = ['date', 'service_type', 'other_service_type', 'men', 'women', 'children']
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class ChurchAttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = ChurchAttendanceRecord
        fields = ['date', 'service_type', 'other_service_type', 'member']
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


# forms.py
from django import forms
from .models import CovenantHourOfPrayer

class CovenantHourOfPrayerForm(forms.ModelForm):
    class Meta:
        model = CovenantHourOfPrayer
        fields = ['date', 'venue', 'other_venue', 'count']


from django.core.exceptions import ValidationError
from django import forms
from django.core.exceptions import ValidationError
from  accounts.models import ChurchMember, ChurchMemberProfile

class ChurchMemberForm(forms.ModelForm):
    class Meta:
        model = ChurchMember
        fields = '__all__'  # includes all fields in the form
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ChurchMemberForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                self.initial['profile_picture'] = self.instance.churchmemberprofile.profile_picture
            except ChurchMemberProfile.DoesNotExist:
                pass
    
    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        date_of_birth = cleaned_data.get('date_of_birth')
        gender = cleaned_data.get('gender')
        address = cleaned_data.get('address')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')

        # Get the current instance id, if it exists
        id = self.instance.id if self.instance else None

        # Exclude the current instance from the check
        if id:
            if ChurchMember.objects.filter(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                address=address,
                email=email,
                phone_number=phone_number
            ).exclude(id=id).exists():
                raise ValidationError('A member with these details already exists.')
        else:
            if ChurchMember.objects.filter(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                address=address,
                email=email,
                phone_number=phone_number
            ).exists():
                raise ValidationError('A member with these details already exists.')

        return cleaned_data

    def save(self, *args, **kwargs):
        # Save the ChurchMember instance
        church_member = super(ChurchMemberForm, self).save(*args, **kwargs)
        
        # Get profile picture from the form
        profile_picture = self.cleaned_data.get('profile_picture')
        
        # Get or create the ChurchMemberProfile for this ChurchMember
        church_member_profile, created = ChurchMemberProfile.objects.get_or_create(church_member=church_member)
        
        # If profile_picture was provided, save it
        if profile_picture:
            church_member_profile.profile_picture = profile_picture
            church_member_profile.save()

        return church_member


from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Newsletter

class NewsletterForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(attrs={'style': 'width: 120%;'}))

    class Meta:
        model = Newsletter
        fields = ['subject', 'content', 'recipients']


from django import forms
from members.models import ConnectCard

class ConnectCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].widget.attrs['placeholder'] = 'How did you hear about us'

    class Meta:
        model = ConnectCard
        fields = '__all__'  # This will include all fields in the form.
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'spouse_dob': forms.DateInput(attrs={'type': 'date'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'children_names': forms.Textarea(attrs={'rows': 1}),
        }

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))


from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event

class EventForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    class Meta:
        model = Event
        fields = ['title', 'description', 'image', 'date', 'venue', 'preacher']
        
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now():
            raise ValidationError('The date cannot be in the past!')
        return date


# forms.py
from django import forms

class PrayerRequestForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    prayer_request = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))



from django import forms
from .models import Finance, CustomCategory, Expense


from django import forms
from django.core.exceptions import ValidationError
from .models import Finance

class FinanceForm(forms.ModelForm):
    class Meta:
        model = Finance
        fields = '__all__'
        
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError("Date cannot be in the future.")
        return date
    
    def clean(self):
        cleaned_data = super().clean()
        amount_fields = ['offering', 'tithe', 'shiloh', 'thanksgiving', 'welfare', 'project']
        
        for field_name in amount_fields:
            amount = cleaned_data.get(field_name)
            if amount is not None and amount < 0:
                self.add_error(field_name, "Amount cannot be negative.")
        
        return cleaned_data

       
class CustomCategoryForm(forms.ModelForm):
    class Meta:
        model = CustomCategory
        fields = ['name', 'amount']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description']
        
        
        
from django import forms
from .models import TithlyOffering

class TithlyOfferingForm(forms.ModelForm):
    class Meta:
        model = TithlyOffering
        fields = ['date', 'offering', 'tithe', 'shiloh', 'thanksgiving', 'welfare', 'project']

from django import forms
from .models import Expense, CustomCategory

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'amount', 'description']

class CustomCategoryForm(forms.ModelForm):
    class Meta:
        model = CustomCategory
        fields = ['name', 'amount', 'finance']


from django import forms

class ReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
