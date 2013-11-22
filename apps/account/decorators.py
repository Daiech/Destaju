from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from apps.process_admin.models import UserType
from functools import wraps
from django.http import Http404


def access_required(*permission):
    """*permission is a list with the permissions like a String

    UserType codes:
    NAME        : CODE
    superadmin  : superadmin
    admin       : admin
    supervisor 1: s1
    supervisor 2: s2
    supervisor 3: s3
    consultor   : consultor
    empleado    : empleado
    proveedor   : proveedor"""

    def decorator(func):
        def get_permissions_like_objects(*permission):
            """ut_list is a list with the permissions like objects"""
            obj_list = UserType.objects.get_all_active()
            ut_list = list()
            if 'superadmin' in permission:
                ut_list.append(obj_list[0])
            if 'admin' in permission:
                ut_list.append(obj_list[1])
            if 's1' in permission:
                ut_list.append(obj_list[2])
            if 's2' in permission:
                ut_list.append(obj_list[3])
            if 's3' in permission:
                ut_list.append(obj_list[4])
            if 'consultor' in permission:
                ut_list.append(obj_list[5])
            if 'empleado' in permission:
                ut_list.append(obj_list[6])
            if 'proveedor' in permission:
                ut_list.append(obj_list[7])
            return ut_list

        def inner_decorator(request, *args, **kwargs):
            """can continue if the current user is in usertype_list"""
            my_ut = None
            usertype_list = get_permissions_like_objects(*permission)
            if len(usertype_list) > 0:
                try:
                    my_ut = request.user.userprofile.user_type
                except Exception, e:
                    return HttpResponseRedirect(reverse("personal_data") + "#usuario-sin-perfil")
                l = filter(lambda x: x.id == my_ut.id, usertype_list)
                s = False
                for o in usertype_list:
                    if o.id == my_ut.id:
                        s = True
                        break;
                if s:
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseRedirect(reverse('home'))
            else:
                raise Http404
        return wraps(func)(inner_decorator)
    return decorator
