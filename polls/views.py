from urllib import response
from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse
from django.views import generic
# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html',context)

# this is used in place of index function
# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'

    # def get_queryset(self):
    #     return Question.objects.order_by('-pub_date')[:5]


def detail(request,pk):
    
    question = get_object_or_404(Question,id=pk)
    
    context = {
        'question':question
    }
    return render(request, 'polls/detail_page.html',context)

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail_page.html'


def results(request,pk):
    question = get_object_or_404(Question,pk=pk)
    return render(request,'polls/results_page.html',{'question':question})

# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results_page.html'

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))

    return HttpResponse("You are voting on question %s." % question_id)

