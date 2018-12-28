from django import forms

from .models import CumActivity
from .validators import validate_O_1

class CumActivityCreateForm(forms.ModelForm):
    #email = forms.EmailField(required=False)
    class Meta:
       model = CumActivity
       exclude = ['cumAct', 'doseAbs', 'slug', 'category', 'owner', 'location']
       # fields = [
       #   # 'name',
       #   # 'Organ',
       #   # 't_1',
       #   # 'A_1',
       #   # 't_2',
       #   # 'A_2',
       #   # 't_3',
       #   # 'A_3',
       #   # 't_4',
       #   # 'A_4',
       #   # 'CT_Patient',
       #   # 'CT_Organ',
       # ]
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name == "hello":
          raise forms.ValidationError('Not a valid name')
        return name

    #def clean_email(self):
    #    email = self.cleaned_data.get("email")
    #    if ".edu" in email:
    #      raise forms.ValidationError('Sorry, we do not accept edu emails.')
    #    return email

#class IRDoseCreateForm(forms.Form):
#    O_1        = forms.CharField()
#    name       = forms.CharField()
#    t_1        = forms.FloatField(required=False)
#    A_1        = forms.FloatField(required=False)
#    t_2        = forms.FloatField(required=False)
#    A_2        = forms.FloatField(required=False)
#    t_3        = forms.FloatField(required=False)
#    A_3        = forms.FloatField(required=False)
#    t_4        = forms.FloatField(required=False)
#    A_4        = forms.FloatField(required=False)
#    CT_Patient = forms.FileField()
#    CT_Organ   = forms.FileField()
#    CT_Target_1   = forms.FileField()
#    CT_Target_2   = forms.FileField()

#    def clean_name(self):
#        name = self.cleaned_data.get("name")
#        if name == "hello":
#          raise forms.ValidationError('Not a valid name')
#        return name
