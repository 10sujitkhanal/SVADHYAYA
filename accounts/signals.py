from django.contrib.auth.models import User
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added

@receiver(social_account_added)
def save_first_last_name(sender, **kwargs):
    user = kwargs['request'].user
    socialaccount = kwargs['socialaccount']

    if not user.first_name:
        if socialaccount.provider == 'google':
            user.first_name = socialaccount.extra_data.get('given_name', '')
        elif socialaccount.provider == 'github':
            user.first_name = socialaccount.extra_data.get('name', '').split()[0]

    if not user.last_name:
        if socialaccount.provider == 'google':
            user.last_name = socialaccount.extra_data.get('family_name', '')
        elif socialaccount.provider == 'github':
            user.last_name = ' '.join(socialaccount.extra_data.get('name', '').split()[1:])

    user.save()

    if not user.profile_picture:
        if socialaccount.provider == 'google':
            profile_picture_url = socialaccount.extra_data.get('picture', '')
        elif socialaccount.provider == 'github':
            profile_picture_url = socialaccount.extra_data.get('avatar_url', '')

        if profile_picture_url:
            user.profile_picture = profile_picture_url
            user.save()
