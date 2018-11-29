from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from apps.projects.models import Excerpt
from apps.participations import models
from utils.decorators import require_ajax
from datetime import date


@require_ajax
def send_suggestion(request):
    excerpt_id = request.POST.get('excerptId')
    content = request.POST.get('suggestion')
    start_index = int(request.POST.get('startSelection'))
    end_index = int(request.POST.get('endSelection'))
    excerpt = get_object_or_404(Excerpt, pk=excerpt_id)

    closed_groups = excerpt.document.invited_groups.filter(
        closing_date__gte=date.today(),
        public_participation=False
    )

    invited_group = None
    for group in closed_groups:
        if request.user in group.thematic_group.participants.all():
            invited_group = group
            break

    public_groups = excerpt.document.invited_groups.filter(
        closing_date__lte=date.today(),
        public_participation=True
    )

    if invited_group is not None and public_groups.exists():
        invited_group = public_groups.first()

    if invited_group:
        models.Suggestion.objects.create(
            invited_group=invited_group,
            selected_text=excerpt.content[start_index:end_index],
            start_index=start_index,
            end_index=end_index,
            excerpt=excerpt,
            content=content,
            author=request.user,
        )
        html = render_to_string(
            'components/document-excerpt.html',
            {'excerpt': excerpt}
        )
        return JsonResponse({
            'id': excerpt.id,
            'html': html,
        })
    else:
        return JsonResponse(
            {'error': _('Project closed for participation')},
            status=400
        )
