from django.http import JsonResponse
from django.views.generic.base import TemplateView

from .models import Participant
from .forms import ParticipantForm


class ContestView(TemplateView):
    """Страница конкурса"""

    template_name = 'contest/contest.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ParticipantForm()
        context['participants'] = Participant.objects.all().order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        form = ParticipantForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if Participant.objects.filter(email=email).exists():
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'errors': {
                            'email': ['Этот email уже зарегистрирован.']
                        }
                    }, status=400)
                else:
                    return self.render_to_response(self.get_context_data(form=form, email_error='Этот email уже зарегистрирован.'))

            participant = form.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'message': 'Спасибо за участие!',
                    'participant': {
                        'name': participant.name,
                        'email': participant.email,
                        'code': participant.code
                    }
                })
            return self.render_to_response(self.get_context_data(form=form, success_message='Спасибо за участие!'))
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            return self.render_to_response(self.get_context_data(form=form))
