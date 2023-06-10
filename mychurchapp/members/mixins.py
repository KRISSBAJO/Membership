from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None

    def test_func(self):
        # Check if user belongs to any of the groups in group_required
        if self.group_required and self.request.user.groups.filter(name__in=self.group_required).exists():
            return True
        # If the user is not in any of the groups, return False
        messages.error(self.request, 'You do not have permission to access this page.')
        return False
    
    def handle_no_permission(self):
        # Redirect to home page if the user does not have permission
        return redirect('index')
