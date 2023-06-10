from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class CellGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_started = models.DateField(blank=True, null=True)
    leader = models.ForeignKey('ChurchMember', on_delete=models.SET_NULL, null=True, blank=True, related_name='cell_group_leader')
    secretary = models.ForeignKey('ChurchMember', on_delete=models.SET_NULL, null=True, blank=True, related_name='cell_group_secretary')
    assistant_leader = models.ForeignKey('ChurchMember', on_delete=models.SET_NULL, null=True, blank=True, related_name='cell_group_assistant_leader')
    
    street_address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    
    def __str__(self):
        return self.name

    @property
    def full_address(self):
        """Returns the full address as a single string."""
        address_parts = [self.street_address, self.city, self.state, self.zipcode]
        return ", ".join(part for part in address_parts if part)  # exclude any blank parts

    def clean(self):
        if self.date_started and self.date_started > timezone.now().date():
            raise ValidationError("Date started cannot be in the future.")



class ServiceGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_started = models.DateField(blank=True, null=True)
    leader = models.ForeignKey('ChurchMember', on_delete=models.SET_NULL, null=True, blank=True, related_name='service_group_leader')
    secretary = models.ForeignKey('ChurchMember', on_delete=models.SET_NULL, null=True, blank=True, related_name='service_group_secretary')
    assistant_leader = models.ForeignKey('ChurchMember', on_delete=models.SET_NULL, null=True, blank=True, related_name='service_group_assistant_leader')

    def __str__(self):
        return self.name

    def clean(self):
        if self.date_started and self.date_started > timezone.now().date():
            raise ValidationError("Date started cannot be in the future.")




from django.db import models
from django.utils import timezone

class ChurchMember(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    date_joined = models.DateField(auto_now_add=True)
    is_active_member = models.BooleanField(default=False)
    is_inactive = models.BooleanField(default=False)
    cell_group = models.ForeignKey(CellGroup, on_delete=models.SET_NULL, null=True, blank=True)
    service_group = models.ForeignKey(ServiceGroup, on_delete=models.SET_NULL, null=True, blank=True)
    is_new_member = models.BooleanField(default=False, help_text="New member of the church")
    is_baptized = models.BooleanField(default=False, help_text="Baptised by immersion in water")
    is_confirmed_member = models.BooleanField(default=False, help_text="Established member of the church")
    
    def clean(self):
        if self.date_of_birth > timezone.now().date():
            raise ValidationError("Birth date cannot be in the future.")
    
    def save(self, *args, **kwargs):
        # Set the member's status based on the conditions
        if self.is_inactive:
            self.is_active_member = False
        elif self.is_new_member:
            self.is_active_member = False
        elif self.date_joined == timezone.now().date():
            self.is_active_member = False
        else:
            self.is_active_member = True
            
        # Save with the updated attributes
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ChurchAttendance(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('MID_WK', 'Wednesday Midweek'),
        ('SUN', 'Sunday'),
        ('WOSE', 'Week of Spiritual Emphasis'),
        ('SHILOH', 'Shiloh'),
        ('ANNI', 'Anniversary'),
        ('LE_SUB', 'Leadership Empowerment Summit'),
        ('OTHER', 'Others'),
    ]

    date = models.DateTimeField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='SUN')
    other_service_type = models.CharField(max_length=100, blank=True, null=True)
    men = models.IntegerField(default=0)
    women = models.IntegerField(default=0)
    children = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_service_type_display()} on {self.date.strftime('%Y-%m-%d')}"

    def clean(self):
        super().clean()  # to keep the validation from parent class

        if self.date > timezone.now():
            raise ValidationError("Attendance date cannot be in the future.")
        if self.service_type == 'OTHER' and not self.other_service_type:
            raise ValidationError("Please specify the 'Other' service type.")
        if self.men < 0:
            raise ValidationError("Men count cannot be negative.")
        if self.women < 0:
            raise ValidationError("Women count cannot be negative.")
        if self.children < 0:
            raise ValidationError("Children count cannot be negative.")
    
    @property
    def total_attendees(self):
        return self.men + self.women + self.children

class ChurchAttendanceRecord(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('MID_WK', 'Wednesday Midweek'),
        ('SUN', 'Sunday'),
        ('WOSE', 'Week of Spiritual Emphasis'),
        ('SHILOH', 'Shiloh'),
        ('ANNI', 'Anniversary'),
        ('LE_SUB', 'Leadership Empowerment Summit'),
        ('OTHER', 'Others'),
    ]
    member = models.ForeignKey(ChurchMember, on_delete=models.CASCADE)
    church_attendance = models.ForeignKey(ChurchAttendance, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateTimeField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='SUN')
    other_service_type = models.CharField(max_length=100, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_member_confirmation_status()

    def update_member_confirmation_status(self):
        attendance_count = ChurchAttendanceRecord.objects.filter(member=self.member).count()
        if attendance_count >= 10:
            self.member.is_confirmed_member = True
        else:
            self.member.is_confirmed_member = False
        self.member.save()

    def __str__(self):
        return f"{self.member} attended {self.get_service_type_display()} on {self.date.strftime('%Y-%m-%d')}"



class CellGroupMeeting(models.Model):
    date = models.DateTimeField()
    cell_group = models.ForeignKey(CellGroup, on_delete=models.CASCADE, related_name='meetings')
    attendees = models.ManyToManyField(ChurchMember, related_name='cell_group_meetings_attended')

    def __str__(self):
        return f"Cell Group Meeting on {self.date.strftime('%Y-%m-%d')}"

    def clean(self):
        if self.date > timezone.now():
            raise ValidationError("Meeting date cannot be in the future.")

class ServiceGroupMeeting(models.Model):
    date = models.DateTimeField()
    service_group = models.ForeignKey(ServiceGroup, on_delete=models.CASCADE, related_name='meetings')
    attendees = models.ManyToManyField(ChurchMember, related_name='service_group_meetings_attended')

    def __str__(self):
        return f"Service Group Meeting on {self.date.strftime('%Y-%m-%d')}"

    def clean(self):
        if self.date > timezone.now():
            raise ValidationError("Meeting date cannot be in the future.")


from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class CovenantHourOfPrayer(models.Model):
    VENUE_CHOICES = [
        ('zoom', 'Zoom'),
        ('church_premise', 'Church Premise'),
        ('others', 'Others'),
    ]
    
    date = models.DateField()
    venue = models.CharField(max_length=20, choices=VENUE_CHOICES, default='zoom')
    other_venue = models.CharField(max_length=100, blank=True, null=True)
    count = models.IntegerField(validators=[MinValueValidator(0)])

    def clean(self):
        if self.date > timezone.now().date():
            raise ValidationError("Date cannot be in the future.")
        if self.count < 0:
            raise ValidationError("Count cannot be negative.")

    def __str__(self):
        return f"Covenant Hour of Prayer - {self.date}"


from ckeditor.fields import RichTextField

class Newsletter(models.Model):
    SUBJECT_CHOICES = [
        ('New Member', 'New Member'),
        ('Inactive Member', 'Inactive Member'),
        ('Thank You', 'Thank You'),
    ]

    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    content = RichTextField(blank=True, null=True)
    recipients = models.ManyToManyField('ChurchMember', related_name='newsletters')
    date_created = models.DateTimeField(auto_now_add=True)
    send_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.date_created}"


from django.db import models

class ConnectCard(models.Model):
    # Choices
    TITLE_CHOICES = [('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Dr', 'Dr'), ('Rev', 'Rev')]
    STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married')]
    VISIT_STATUS_CHOICES = [('1st Time Guest', '1st Time Guest'), ('2nd Time Guest', '2nd Time Guest'), ('3rd Time Guest', '3rd Time Guest'), ('Regular Visitor', 'Regular Visitor'), ('Out of Town Guest', 'Out of Town Guest'), ('Member', 'Member')]

    # Fields
    date = models.DateField()
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    cell_phone = models.CharField(max_length=20 )
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    spouse_name = models.CharField(max_length=200, null=True, blank=True)
    spouse_email = models.EmailField(null=True, blank=True)
    spouse_dob = models.DateField(null=True, blank=True)
    children_names = models.TextField(null=True, blank=True)
    visit_status = models.CharField(max_length=20, choices=VISIT_STATUS_CHOICES)
    guest_of = models.CharField(max_length=200, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='members/media')
    date = models.DateTimeField()
    venue = models.CharField(max_length=200, blank=True)
    preacher = models.CharField(max_length=200, blank=True)
    
    def short_description(self):
        return self.description[:150]

    def __str__(self):
        return self.title

from django.db import models

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.alt_text
    


from django.db import models

class Testimonial(models.Model):
    image = models.ImageField(upload_to='testimonials/')
    text = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    
    def __str__(self):
        return self.author
    
from django.db import models

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='announcement_images/')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
