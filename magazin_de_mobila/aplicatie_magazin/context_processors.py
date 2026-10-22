from django.conf import settings

def firma_context(request):
    return {
        'firma': getattr(settings, 'INFORMATII_FIRMA', {})
    }