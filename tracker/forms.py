from django import forms
from models import *

class StoreStatusForm(forms.ModelForm):
    
    class Meta:
        model = StoreStatus
        fields = '__all__'

class BusinessHourForm(forms.ModelForm):
    
    class Meta:
        model = BusinessHour
        fields = '__all__'

class TimezoneForm(forms.ModelForm):
    
    class Meta:
        model = Timezone
        fields = '__all__'




