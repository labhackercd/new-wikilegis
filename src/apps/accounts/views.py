from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import date

User = get_user_model()


def participants_autocomplete(request):
    name = request.GET.get('name', None)
    themes = request.GET.getlist('theme', None)
    groups = request.GET.getlist('group', None)
    min_age = request.GET.get('minAge', None)
    max_age = request.GET.get('maxAge', None)
    gender = request.GET.get('gender', None)
    uf = request.GET.get('locale', None)
    selected_ids = request.GET.getlist('selected_participants', None)

    today = date.today()
    query = Q()

    if name:
        query = Q(first_name__istartswith=name) | Q(email__istartswith=name)
    if themes:
        query &= Q(profile__themes__id__in=themes)
    if groups:
        query &= Q(thematic_groups__id__in=groups)
    if min_age:
        query &= Q(
            profile__birthdate__year__lt=today.year - int(min_age))
    if max_age:
        query &= Q(
            profile__birthdate__year__gte=today.year - int(max_age))
    if gender:
        query &= Q(profile__gender=gender)
    if uf:
        query &= Q(profile__uf=uf)

    if query:
        query &= Q(is_active=True)
        users = User.objects.filter(query).distinct().exclude(
            id__in=selected_ids).exclude(id=request.user.id)
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
                {'name': theme.name, 'color': theme.color}
                for theme in user.profile.themes.all()
            ],
        }
        result.append(obj)

    return JsonResponse(result, safe=False)


def email_list_participants(request):
    emails = request.GET.get('emails', None)
    result = []

    for email in emails.replace(';', ',').split(','):
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_object = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'avatar': user.profile.avatar,
                'themes': [
                    {'name': theme.name, 'color': theme.color}
                    for theme in user.profile.themes.all()
                ],
            }
        else:
            user_object = {
                'email': email
            }
        result.append(user_object)

    return JsonResponse(result, safe=False)
