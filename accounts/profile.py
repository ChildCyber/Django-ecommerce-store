from accounts.forms import UserProfileForm
from accounts.models import UserProfile


def retrieve(request):
    """
    gets the UserProfile instance for a user, creates one if it does not exist
    """
    try:
        profile = request.user.userprofile_set.first()
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()
    return profile


def set(request):
    """
    updates the information stored in the user's profile
    """
    profile = retrieve(request)
    profile_form = UserProfileForm(request.POST, instance=profile)
    profile_form.save()
