from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


# Create your views here.
class IndexView(generic.ListView):

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, reverse('polls:details'), {'question': question, 'error_message': "You didn't select a choice."})
    else:
        select_choice.votes = F('votes') + 1
        select_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
