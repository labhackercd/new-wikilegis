from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


def participants_autocomplete(request):
    name = request.GET.get('name', None)
    themes = request.GET.getlist('theme', None)
    query = Q()
    if name:
        query = Q(first_name__istartswith=name) | Q(email__istartswith=name)
    elif themes:
        query &= Q(profile__themes__id__in=themes)

    if query:
        users = User.objects.filter(query).distinct()
    else:
        users = User.objects.none()

    result = []
    for user in users:
        obj = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar': user.profile.avatar,
            'themes': [
                (theme.name, theme.color)
                for theme in user.profile.themes.all()
            ],
        }
        result.append(obj)

    return JsonResponse(result, safe=False)
