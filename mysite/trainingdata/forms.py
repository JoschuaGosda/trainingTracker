from django.forms import ModelForm, Textarea, TextInput
from .models import Deadhang_max, Deadhang_endurance, Pullup_max, Pullup_endurance, CustomSession


class Deadhang_max_Form(ModelForm):
	class Meta:
		model = Deadhang_max
		exclude = ['user','training','session_counter','relative_strength']
		widgets = {
            'comment': Textarea(attrs={
			'placeholder':'How did you feel today? Add some extra notes if needed.',
			'cols': 2, 'rows': 2,
			}),
        }


class Deadhang_endurance_Form(ModelForm):
	class Meta:
		model = Deadhang_endurance
		exclude = ['user','training','session_counter']
		widgets = {
            'comment': Textarea(attrs={
			'placeholder':'How did you feel today? Add some extra notes if needed.',
			'cols': 2, 'rows': 2,
			}),
        }

class Pullup_max_Form(ModelForm):
	class Meta:
		model = Pullup_max
		exclude = ['user','training','session_counter']
		widgets = {
            'comment': Textarea(attrs={
			'placeholder':'How did you feel today? Add some extra notes if needed.',
			'cols': 2, 'rows': 2,
			}),
        }

class Pullup_endurance_Form(ModelForm):
	class Meta:
		model = Pullup_endurance
		exclude = ['user','training','session_counter']
		widgets = {
            'comment': Textarea(attrs={
			'placeholder':'How did you feel today? Add some extra notes if needed.',
			'cols': 2, 'rows': 2,
			}),
        }

class CustomSession_Form(ModelForm):
	class Meta:
		model = CustomSession
		exclude = ['user','training']
		widgets = {
            'comment': Textarea(attrs={
			'placeholder':'How did you feel today? Add some extra notes if needed.',
			'cols': 2, 'rows': 2,
			}),
			'on_off_time': TextInput({"placeholder":"Specify how long you exercise vs. how long you are resting in between reps, i.e 10/20 secs"}),
        }
