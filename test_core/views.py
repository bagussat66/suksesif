from datetime import datetime, timedelta
from shop.models import Product
import random

from django.http import request
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from .forms import AnswerBfiForm, AnswerEppsForm, AnswerMbtiForm, AnswerPapiForm, AnswerTpaForm, TesterModelForm

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import FormView, UpdateView
from .models import AnsweredQuestion, QuestionBfi, QuestionEpps, QuestionMbti, QuestionPapi, QuestionTpa, TestAttempt, TestResult, Tester
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.utils import timezone

from django.core.paginator import Paginator

def load_tester(type,session):
    for key, value in session.items():
        print('{} => {}'.format(key, value))
    if f"tester_{type}" in session:
        tester = get_object_or_404(Tester,pk=session[f"tester_{type}"],finished=False,type=type)
        print("Already in session")
    else:
        tester = Tester(type=type)
        tester.save()
        session[f"tester_{type}"] = tester.pk
        print("New in session")
    return tester

class TesterUpdateView(UpdateView):
    template_name = 'test/tester.html'
    form_class = TesterModelForm
    model = Tester

    def get_object(self):
        type = self.kwargs['type'].upper()
        tester = load_tester(type,self.request.session)

        if self.request.user.is_authenticated:
            tester.user = self.request.user

        return tester
    
    def get_context_data(self, **kwargs):
        context = super(TesterUpdateView, self).get_context_data(**kwargs)

        context['object'] =  get_object_or_404(Product,type=self.kwargs['type'].upper())
        return context

    def get_success_url(self):
        return reverse('test:result',kwargs={'type': self.kwargs['type']})

    def form_valid(self,form):
        return super().form_valid(form)

class TestResultView(DetailView):
    model = TestResult
    template_name = 'test/result.html'

    def get_object(self):
        try:
            type = self.kwargs['type'].upper()
            tester = load_tester(type,self.request.session)
            test_attempt = get_object_or_404(TestAttempt,tester=tester,type=type,finished=False)
            if type=='MBTI':
                E,I,S,N,T,F,J,P = test_attempt.get_score_mbti()
                personality = test_attempt.get_personality_mbti(E,I,S,N,T,F,J,P)
            else:
                personality = "pintar"

            return get_object_or_404(self.model,personality=personality)
        except ObjectDoesNotExist:
            messages.error(self.request,"Tes tidak ditemukan.")
            return redirect("core:home")


class TestPageView(View):
    template_name = 'test/assessment.html'
    template_name_alt = 'test/assessment_summary.html'
    paginate_by = 5

    def load(self,*args,**kwargs):
        type = self.kwargs['type'].upper()
        tester = load_tester(type,self.request.session)
        test_attempt,create = TestAttempt.objects.get_or_create(tester=tester,type=type,finished=False)

        
        initial = {}

        if create:
            print("New Test")
            if (self.request.user.is_authenticated):
                test_attempt.user = self.request.user
            test_attempt.reload()
        else:
            print("Reload")
            i = 1
            for answered_question in test_attempt.answered_questions.all():
                key = f"ans{i:03}"
                initial[key]=answered_question.answer
                i+=1

        return test_attempt,create,initial

    def collect_answers(self,cleaned_data,*args,**kwargs):
        answers = []

        max = len(cleaned_data)
        
        for i in range(1,max+1):
            key = f"ans{i:03}"
            answers.append(cleaned_data.get(key))

        return answers


    def get(self,*args,**kwargs):
        type = self.kwargs['type'].upper()
        no = self.kwargs['no'] if self.kwargs['no'] else '1'
        

        if type=='MBTI':
            form_class = AnswerMbtiForm
        elif type=='BFI':
            form_class = AnswerBfiForm
        elif type=='PAPI':
            form_class = AnswerPapiForm
        elif type=='EPPS':
            form_class = AnswerEppsForm
        elif type=='TPA':
            form_class = AnswerTpaForm
        else:
            messages.info(self.request,"Test tidak ditemukan.")
            return redirect("core:home")

        test_attempt,create,initial = self.load()

        if create == False and (test_attempt.expected.replace(tzinfo=None) < timezone.now().replace(tzinfo=None)):
            messages.info(self.request,"Waktu test habis.")
            return redirect("test:tester",type=self.kwargs['type'])
            

        max=int(no)+self.paginate_by

        form = form_class(initial=initial,answered_questions=test_attempt.answered_questions.all(),no=no,max=max)
        object = get_object_or_404(Product,type=type)
        expected = test_attempt.expected
        prev = int(no) - self.paginate_by if int(no) - self.paginate_by > 1 else 1
        context = {
                'no' : no,
                'max' : max,
                'prev' : prev,
                'form' : form,
                'object' : object,
                'expected' : expected
            }
        
        if no == '0':
            return render(self.request,self.template_name_alt,context)
        else:
            return render(self.request,self.template_name,context)
        
    def post(self,*args,**kwargs):
        type = self.kwargs['type'].upper()
        no = self.kwargs['no'] if self.kwargs['no'] else '1'

        if type=='MBTI':
            form_class = AnswerMbtiForm
        elif type=='BFI':
            form_class = AnswerBfiForm
        elif type=='PAPI':
            form_class = AnswerPapiForm
        elif type=='EPPS':
            form_class = AnswerEppsForm
        elif type=='TPA':
            form_class = AnswerTpaForm
        else:
            messages.info(self.request,"Test tidak ditemukan.")
            return redirect("core:home")
        
        test_attempt,create,initial = self.load()

        if create == False and (test_attempt.expected.replace(tzinfo=None) < timezone.now().replace(tzinfo=None)):
            messages.info(self.request,"Waktu test habis.")
            return redirect("core:tester")

        max=int(no)+self.paginate_by
        form = form_class(self.request.POST,answered_questions=test_attempt.answered_questions.all(),no=no,max=max)
        
        if form.is_valid():
            answers = self.collect_answers(form.cleaned_data)
            answered_questions = list(test_attempt.answered_questions.all())

            i = 0
            for answered_question in answered_questions:
                if answers[i]:
                    answered_question.answer = answers[i]
                    answered_question.save()
                i += 1
            no = int(no)
            if no>=len(answered_questions):
                return redirect("test:tester",type=self.kwargs['type'])
            else:
                return redirect("test:assessment",type=self.kwargs['type'],no=max)
        
        object = get_object_or_404(Product,type=type)
        expected = test_attempt.expected

        prev = int(no) - self.paginate_by if int(no) - self.paginate_by > 1 else 1
        context = {
                'no' : no,
                'max' : max,
                'prev' : prev,
                'form' : form,
                'object' : object,
                'expected' : expected
            }

        if no == '0':
            return render(self.request,self.template_name_alt,context)
        else:
            return render(self.request,self.template_name,context)
