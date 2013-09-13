def get_project_name(request):
    from django.conf import settings
    return {"PROJECT_NAME": settings.PROJECT_NAME, "PROJECT_DESCRIPTION": settings.PROJECT_DESCRIPTION}


def is_debug(request):
    from django.conf import settings
    return {"DEBUG": settings.DEBUG}

