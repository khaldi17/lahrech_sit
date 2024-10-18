from django.conf import settings

def superadmin_status(request):
    if request.user.is_authenticated:
        return {
            'superadmin': request.user.is_superuser
        }
    return {
        'superadmin': False
    }
