from django.core.exceptions import ValidationError

def validate_email(value):
        email = value
        if ".edu" in email:
          raise forms.ValidationError('Sorry, we do not accept edu emails.')



ORGANS = ['Liver', 'Spleen', 'Kidneys', 'Bladder', 'Blood']

def validate_O_1(value):
    cat = value.capitalize()
    if not value in ORGANS and not cat in ORGANS:
       raise ValidationError(f'{value} not in the list') 

