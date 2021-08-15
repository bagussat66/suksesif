from .models import Tester
from django import forms


SCORING_CHOICES = (
    ("-2","Sangat Tidak Sesuai"),
    ("-1","Tidak Sesuai"),
    ("0","Ragu-Ragu"),
    ("1","Sesuai"),
    ("2","Sangat Sesuai")
)

class AnswerMbtiForm(forms.Form):
    def __init__(self, *args, **kwargs):
        answered_questions = kwargs.pop('answered_questions')
        super(AnswerMbtiForm, self).__init__(*args, **kwargs)
        i = 1
        for answered_question in answered_questions:
            self.fields[f"ans{i:03}"] = forms.ChoiceField(widget=forms.RadioSelect(),choices=SCORING_CHOICES,required=False,label=f"{i}. {answered_question.question_mbti.text}")
            i += 1

class AnswerBfiForm(forms.Form):
    def __init__(self, *args, **kwargs):
        answered_questions = kwargs.pop('answered_questions')
        super(AnswerBfiForm, self).__init__(*args, **kwargs)
        i = 1
        for answered_question in answered_questions:
            self.fields[f"ans{i:03}"] = forms.ChoiceField(widget=forms.RadioSelect(),choices=SCORING_CHOICES,required=False,label=f"{i}. {answered_question.question_bfi.text}")
            i += 1

class AnswerPapiForm(forms.Form):
    def __init__(self, *args, **kwargs):
        answered_questions = kwargs.pop('answered_questions')
        super(AnswerPapiForm, self).__init__(*args, **kwargs)
        i = 1
        for answered_question in answered_questions:
            SCORING_CHOICES = (
                ("a",answered_question.question_papi.a),
                ("b",answered_question.question_papi.b)
            )
            self.fields[f"ans{i:03}"] = forms.ChoiceField(widget=forms.RadioSelect(),choices=SCORING_CHOICES,required=False,label=f"{i}. Pilih paling sesuai")
            i += 1

class AnswerEppsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        answered_questions = kwargs.pop('answered_questions')
        super(AnswerEppsForm, self).__init__(*args, **kwargs)
        i = 1
        for answered_question in answered_questions:
            SCORING_CHOICES = (
                ("a",answered_question.question_epps.a),
                ("b",answered_question.question_epps.b)
            )
            self.fields[f"ans{i:03}"] = forms.ChoiceField(widget=forms.RadioSelect(),choices=SCORING_CHOICES,required=False,label=f"{i}. Pilih paling sesuai")
            i += 1

class AnswerTpaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        answered_questions = kwargs.pop('answered_questions')
        super(AnswerTpaForm, self).__init__(*args, **kwargs)
        i = 1
        for answered_question in answered_questions:
            SCORING_CHOICES = (
                ("a",answered_question.question_tpa.a),
                ("b",answered_question.question_tpa.b),
                ("c",answered_question.question_tpa.c),
                ("d",answered_question.question_tpa.d),
                ("e",answered_question.question_tpa.e)
            )
            self.fields[f"ans{i:03}"] = forms.ChoiceField(widget=forms.RadioSelect(),choices=SCORING_CHOICES,required=False,label=f"{i}. {answered_question.question_tpa.text}")
            i += 1

class TesterModelForm(forms.ModelForm):
    class Meta:
        model = Tester
        fields = [
            'name',
            'age',
            'gender',
            'education'
        ]
        labels = {
            "name": "Nama",
            "age": "Usia",
            "gender": "Jenis Kelamin",
            "education": "Pendidikan Terakhir"
        }