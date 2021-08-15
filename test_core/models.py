from django.db import models
from django.conf import settings
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import deactivate
import random
# Create your models here.

GENDER_CHOICES = (
    ('L','Laki-Laki'),
    ('P','Perempuan'),
    ('N','Tidak Menyampaikan')
)

EDUCATION_CHOICES = (
    ('S3','Doktoral/S3'),
    ('S2','Magister/S2'),
    ('S1','Sarjana/S1'),
    ('D4','Diploma-4/D4/STr'),
    ('D3','Diploma-3/D3'),
    ('SMK','Sekolah Menengah Kejuruan/SMK'),
    ('SMA','Sekolah Menengah Atas/SMA/MA'),
    ('SMP','Sekolah Menengah Pertama/SMP/MTs'),
    ('SD','Sekolah Dasar/SD/MI'),
    ('NA','Tidak Lulus Sekolah Dasar')
)

TYPE_CHOICES = (
    ('MBTI','Myers-Briggs Type Indicator'),
    ('BFI','Big Five Inventory'),
    ('PAPI','PAPI Kostick'),
    ('TPA','Tes Potensi Akademik')
)

class Tester(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True,null=True)
    name = models.CharField(blank=True,null=True,max_length=30)
    age = models.IntegerField(blank=True,null=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=1,blank=True,)
    type = models.CharField(choices=TYPE_CHOICES,blank=True,null=True,max_length=30)
    education = models.CharField(choices=EDUCATION_CHOICES,blank=True,null=True,max_length=30)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.type}"

TENDENCY_MBTI_CHOICES = (
    ('E','Extroverted'),
    ('S','Sensing'),
    ('T','Thinking'),
    ('J','Judging')
)

class QuestionMbti(models.Model):
    text = models.TextField(blank=True,null=True)
    tendency = models.CharField(choices=TENDENCY_MBTI_CHOICES,max_length=1)
    modifier = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.tendency}: {self.text}"

TENDENCY_PAPI_CHOICES = (
    ('L','Leadership'),
    ('P','Need to Control Others'),
    ('I','Ease in Decision Making'),
    ('F','Need to Support Authority'),
    ('W','Need for Rules and Supervision'),
    ('T','Pace Type'),
    ('V','Vigorous Type'),
    ('R','Theoritical Type'),
    ('D','Interest in Details'),
    ('C','Organized Type'),
    ('X','Need to be Noticed'),
    ('B','Need to be Belonged to Group'),
    ('O','Need for Closeness and Affection'),
    ('S','Social Extension'),
    ('N','Need to Finish Task'),
    ('A','Need to Achieve'),
    ('G','Hard Intense Working'),
    ('Z','Need for Change'),
    ('K','Need to be Forceful'),
    ('E','Emotional Resistent'),
)

class QuestionPapi(models.Model):
    a = models.CharField(max_length=40)
    b = models.CharField(max_length=40)
    tendency_a = models.CharField(choices=TENDENCY_PAPI_CHOICES,max_length=1)
    tendency_b = models.CharField(choices=TENDENCY_PAPI_CHOICES,max_length=1)

    def __str__(self):
        return f"{self.tendency_a} and {self.tendency_b}"

TENDENCY_BFI_CHOICES = (
    ('O','Openness to Experience'),
    ('C','Conscientiousness'),
    ('E','Extraversion'),
    ('A','Agreableness'),
    ('N','Neuroticism')
)

class QuestionBfi(models.Model):
    text = models.TextField(blank=True,null=True)
    tendency = models.CharField(choices=TENDENCY_BFI_CHOICES,max_length=1)
    modifier = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.tendency}: {self.text}"

TENDENCY_EPPS_CHOICES = (
    ('Ach',''),
    ('Def',''),
    ('Ord',''),
    ('Exh',''),
    ('Aut',''),
    ('Aff',''),
    ('Int',''),
    ('Suc',''),
    ('Dom',''),
    ('Aba',''),
    ('Nur',''),
    ('Chg',''),
    ('End',''),
    ('Het',''),
    ('Agg',''),
)

class QuestionEpps(models.Model):
    a = models.CharField(max_length=40)
    b = models.CharField(max_length=40)
    tendency_a = models.CharField(choices=TENDENCY_EPPS_CHOICES,max_length=3)
    tendency_b = models.CharField(choices=TENDENCY_EPPS_CHOICES,max_length=3)
    consistency = models.CharField(choices=TENDENCY_EPPS_CHOICES,max_length=3)

    def __str__(self):
        return f"{self.tendency_a} and {self.tendency_b}"


STREAM_TPA_CHOICES = (
    ('AG','Analogi'),
    ('SN','Sinonim'),
    ('AN','Antonim'),
    ('LG','Logika')
)

class QuestionTpa(models.Model):
    text = models.TextField(blank=True,null=True)
    a = models.CharField(max_length=40)
    b = models.CharField(max_length=40)
    c = models.CharField(max_length=40)
    d = models.CharField(max_length=40)
    e = models.CharField(max_length=40)
    key = models.CharField(max_length=2)
    stream = models.CharField(max_length=2, choices=STREAM_TPA_CHOICES)

    def __str__(self):
        return f"{self.stream}: {self.text}"

class AnsweredQuestion(models.Model):
    tester = models.ForeignKey(Tester,on_delete=models.CASCADE,null=True)
    question_mbti  = models.ForeignKey(QuestionMbti,on_delete=models.CASCADE,null=True,blank=True,default=None)
    question_bfi  = models.ForeignKey(QuestionBfi,on_delete=models.CASCADE,null=True,blank=True,default=None)
    question_papi  = models.ForeignKey(QuestionPapi,on_delete=models.CASCADE,null=True,blank=True,default=None)
    question_epps  = models.ForeignKey(QuestionEpps,on_delete=models.CASCADE,null=True,blank=True,default=None)
    question_tpa  = models.ForeignKey(QuestionTpa,on_delete=models.CASCADE,null=True,blank=True,default=None)
    answer = models.CharField(blank=True,null=True,max_length=5)

    def __str__(self):
        if self.question_mbti:
            return f"{self.tester.name}: {self.answer} for {self.question_mbti.tendency}: {self.question_mbti.text}"
        elif self.question_bfi:
            return f"{self.tester.name}: {self.answer} for {self.question_bfi.tendency}: {self.question_bfi.text}"
        elif self.question_papi:
            return f"{self.tester.name}: {self.answer} for {self.question_papi.tendency_a} and {self.question_papi.tendency_b}"
        elif self.question_epps:
            return f"{self.tester.name}: {self.answer} for {self.question_epps.tendency_a} and {self.question_epps.tendency_b}"
        elif self.question_tpa:
            return f"{self.tester.name}: {self.answer} for {self.question_tpa.stream}: {self.question_tpa.text}"
        else:
            return "None answered"

class TestAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True)
    answered_questions = models.ManyToManyField(AnsweredQuestion)
    tester = models.ForeignKey(Tester,on_delete=models.CASCADE,null=True)
    finished = models.BooleanField(default=False)
    type = models.CharField(choices=TYPE_CHOICES,blank=True,null=True,max_length=5)
    
    def __str__(self):
        return f"{self.tester.name}: {self.type}"

    def re_init(self, *args, **kwargs):
        if self.type=='MBTI':
            questions=list(QuestionMbti.objects.all())
        elif self.type=='BFI':
            questions=list(QuestionBfi.objects.all())
        elif self.type=='PAPI':
            questions=list(QuestionPapi.objects.all())
        elif self.type=='EPPS':
            questions=list(QuestionEpps.objects.all())
        elif self.type=='TPA':
            questions=list(QuestionTpa.objects.all())

        if type!='TPA':  
            random.shuffle(questions)          
        
        for question in questions:
            if self.type=='MBTI':
                ans = AnsweredQuestion(question_mbti=question, tester=self.tester)
            elif self.type=='BFI':
                ans = AnsweredQuestion(question_bfi=question, tester=self.tester)
            elif self.type=='PAPI':
                ans = AnsweredQuestion(question_papi=question, tester=self.tester)
            elif self.type=='EPPS':
                ans = AnsweredQuestion(question_epps=question, tester=self.tester)
            elif self.type=='TPA':
                ans = AnsweredQuestion(question_tpa=question, tester=self.tester)
            ans.save()
            self.answered_questions.add(ans)
        self.save()

    def get_score_mbti(self):
        E = 0
        I = 0
        S = 0
        N = 0
        T = 0
        F = 0
        J = 0
        P = 0
        for answered_question in self.answered_questions.all():
            if answered_question.answer:
                if answered_question.question_mbti.tendency == "E":
                    if answered_question.question_mbti.modifier == "+":
                        E += int(answered_question.answer)
                    else:
                        I += int(answered_question.answer)
                if answered_question.question_mbti.tendency == "S":
                    if answered_question.question_mbti.modifier == "+":
                        S += int(answered_question.answer)
                    else:
                        N += int(answered_question.answer)
                if answered_question.question_mbti.tendency == "T":
                    if answered_question.question_mbti.modifier == "+":
                        T += int(answered_question.answer)
                    else:
                        F += int(answered_question.answer)
                if answered_question.question_mbti.tendency == "J":
                    if answered_question.question_mbti.modifier == "+":
                        J += int(answered_question.answer)
                    else:
                        P += int(answered_question.answer)
        
        return E,I,S,N,T,F,J,P
    
    def get_personality_mbti(self,E,I,S,N,T,F,J,P):
        e="E" if E>=I else "I"
        s="S" if S>=N else "N"
        t="T" if T>=F else "F"
        j="J" if J>=P else "P"

        return f"{e}{s}{t}{j}"
  
class TestResult(models.Model):
    personality = models.CharField(max_length=4)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True,null=True)
    additional_information = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)

    def __str__(self):
        return f"{self.personality} {self.title}"