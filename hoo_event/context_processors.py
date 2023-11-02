# /***************************************************************************************
# *  REFERENCES
# *  Title: Writing your own context processors
# *  Author: Django Documentation
# *  Date: October 7th, 2023
# *  Version: 4.2
# *  URL: https://docs.djangoproject.com/en/dev/ref/templates/api/#writing-your-own-context-processors
# ***************************************************************************************/


from django.contrib.auth.models import Group

def user_group(request):
    user_groups = []
    if request.user.is_authenticated:
        user_groups = [group.name for group in request.user.groups.all()]
    return {'user_groups': user_groups}