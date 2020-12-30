from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from datetime import timedelta, datetime
from django.utils import timezone
# Create your models here.

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
class Training(models.Model):       

	dmax = 'd1'
	dend = 'd2'
	pullmax = 'p1'
	pullend = 'p2'
	custom = 'c'

	SETS_CHOICES = [
		(dmax, 'Deadhang Maximum Strength'),
		(dend, 'Deadhang Strength-Endurance'),
		(pullmax, 'Pullups Maximum Strength'),
		(pullend, 'Pullups Strength-Endurance'),
		(custom, 'Custom Training'),
	]
	title = models.CharField(max_length=2, choices=SETS_CHOICES)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
	)
	date = models.DateField(blank=True)

class TrainingHistory:
	def __init__(self, past_weeks, user):
		self.max_finger = [] * (past_weeks+1)
		self.max_pull   = [] * (past_weeks+1)
		self.max_core   = [] * (past_weeks+1)
		self.end_finger = [] * (past_weeks+1)
		self.end_pull   = [] * (past_weeks+1)
		self.end_core   = [] * (past_weeks+1)
		self.flex       = [] * (past_weeks+1)
		self.antagonist = [] * (past_weeks+1)
		self.other      = [] * (past_weeks+1)
		self.week       = [] * (past_weeks+1)
		day_offset = datetime.today().weekday()
		# current_date starts at beginning of this week
		current_date = timezone.now().date() - timedelta(days=day_offset)
		#print("date", current_date)
		for i in range(past_weeks+1): #loop through weeks
			print(i)
			start_date = current_date - timedelta(days=7*(past_weeks-i))
			end_date = start_date + timedelta(days=7)
			#user = self.request.user
			predefined_weekly_training_objects = Training.objects.filter(user=user).filter(date__gte=start_date, date__lt=end_date)
			custom_weekly_training_objects = CustomSession.objects.filter(user=user).filter(date__gte=start_date, date__lt=end_date)
			self.week.append(start_date.isocalendar()[1])
			self.max_finger.append(predefined_weekly_training_objects.filter(title='d1').count() + custom_weekly_training_objects.filter(Q(target='1') & Q(energy_system='1')).count())
			self.max_pull.append(predefined_weekly_training_objects.filter(title='p1').count())
			self.max_core.append(custom_weekly_training_objects.filter(Q(target='3') & Q(energy_system='1')).count())
			self.end_finger.append(predefined_weekly_training_objects.filter(title='d2').count())
			self.end_pull.append(predefined_weekly_training_objects.filter(title='p2').count())
			self.end_core.append(custom_weekly_training_objects.filter(Q(target='3') & Q(energy_system='2')).count())
			self.flex.append(custom_weekly_training_objects.filter(target='4').count())
			self.antagonist.append(custom_weekly_training_objects.filter(target='5').count())
			self.other.append(custom_weekly_training_objects.filter(target='6').count())


	def get_trainingHistory(self):
		history_dict = dict.fromkeys(['max_finger', 'max_pull', 'max_core','end_finger','end_pull', 'end_core', 'flex', 'antagonist','other','weeks'])
		history_dict['max_finger'] = self.max_finger
		history_dict['max_pull']   = self.max_pull
		history_dict['max_core']   = self.max_core
		history_dict['end_finger'] = self.end_finger
		history_dict['end_pull']   = self.end_pull
		history_dict['end_core']   = self.end_core
		history_dict['flex']       = self.flex
		history_dict['antagonist'] = self.antagonist
		history_dict['other']      = self.other
		history_dict['weeks']      = str(self.week) 
		print(history_dict)
		return history_dict


class CustomSession(models.Model):
	title = models.CharField(max_length=30)
	date = models.DateTimeField(default=timezone.now)
	MAXIMUM_STRENGTH = '1'
	STRENGTH_ENDURANCE = '2'
	AEROBIC_ENDURANCE = '3'
	NONE = '0'

	ENERGYSYTEM_CHOICES = [
		(MAXIMUM_STRENGTH, 'Maximum Strength (anaerobic alactic)'),
		(STRENGTH_ENDURANCE, 'Strength-Endurance (glycolytic/anaerobic lactic)'),
		(AEROBIC_ENDURANCE, 'Aerobic Endurance (aerobic/oxidative)'),
		(NONE, 'None'),
	]
	energy_system = models.CharField(max_length=1, choices=ENERGYSYTEM_CHOICES, default=MAXIMUM_STRENGTH)

	FINGERS = '1'
	UPPER_BODY = '2'
	CORE = '3'
	FLEXIBILITY = '4'
	ANTAGONIST = '5'
	OTHER = '6'
	TARGET_CHOICES = [
		(FINGERS, 'Fingers'),
		(UPPER_BODY, 'Upper Body'),
		(CORE, 'Core'),
		(FLEXIBILITY, 'Flexibility'),
		(ANTAGONIST, 'Antagonists'),
		(OTHER, 'Other')
	]
	target = models.CharField(max_length=1, choices=TARGET_CHOICES, default=FINGERS)

	repetitions = models.IntegerField( blank=True, null=True) #repetions per set
	on_off_time = models.CharField(max_length=15, blank=True, null=True)
	sets = models.IntegerField( blank=True, null=True)


	weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	crimp_size = models.IntegerField(blank=True, null=True)

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
		related_name='custom_training'
	)
	training = models.OneToOneField(
		Training,
		on_delete=models.CASCADE,
		blank=True,
		related_name='custom_training'
	)
	comment = models.TextField(null=True, blank=True)
	def get_absolute_url(self):
		return reverse('record_list')

class Deadhang_max(models.Model):
	date = models.DateTimeField(default=timezone.now)
	HALFGRIMP = 'HG'
	OPENHAND = 'OH'
	HAND_POSITION_CHOICES = [
		(HALFGRIMP, 'Half Grimp'),
		(OPENHAND, 'Open Hand')
	]
	hand_position = models.CharField(
		max_length=2,
		choices=HAND_POSITION_CHOICES,
		default=HALFGRIMP,
		)
	ONEHAND = 'OH'
	TWOHANDS = 'TH'
	NUMBER_OF_HANDS_CHOIES = [
		(ONEHAND, 'One Hand'),
		(TWOHANDS, 'Two Hands')
	]
	hands = models.CharField(
		max_length=2,
		choices = NUMBER_OF_HANDS_CHOIES,
		default = TWOHANDS,
		)
	additional_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	body_weight = models.DecimalField(max_digits=5, decimal_places=2, default = 72)
	relative_strength = models.IntegerField(default=100)
	crimp_size = models.IntegerField(default=20)

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
		related_name='deadhang_max'
	)
	training = models.OneToOneField(
		Training,
		on_delete=models.CASCADE,
		blank=True,
		related_name='training_dmax'
	)
	session_counter = models.IntegerField(blank=True, null=True)
	sets = models.IntegerField(default=5)
	comment = models.TextField(null=True, blank=True)

	def get_absolute_url(self):
		return reverse('record_list')
	#person = models.ForeignKey(
	#	Person,
	#	on_delete = models.CASCADE,
	#	verbose_name = "the related person")

	class Meta:
			verbose_name_plural = "Deadhangs Max"

class Deadhang_endurance(models.Model):
	date = models.DateTimeField(default=timezone.now)
	HALFGRIMP = 'HG'
	OPENHAND = 'OH'
	HAND_POSITION_CHOICES = [
		(HALFGRIMP, 'Half Grimp'),
		(OPENHAND, 'Open Hand')
	]
	hand_position = models.CharField(
		max_length=2,
		choices=HAND_POSITION_CHOICES,
		default=HALFGRIMP,
		)
	SHORT_DURATION = '1'
	LONG_DURATION = '2'
	DURATION_CHOICES = [
		(SHORT_DURATION, 'Short'),
		(LONG_DURATION, 'Long')
	]
	hold_duration = models.CharField(max_length=1, choices=DURATION_CHOICES, default=SHORT_DURATION)
	additional_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	body_weight = models.DecimalField(max_digits=5, decimal_places=2, default = 72)
	crimp_size = models.IntegerField(default=20)
	level = models.CharField(max_length=1)

	# S1 = '1'
	# S2 = '2'
	# S3 = '3'
	# S4 = '4'
	# S5 = '5'
	# S6 = '6'
	# SETS_CHOICES = [
	# 	(S1, '1 Set'),
	# 	(S2, '2 Sets'),
	# 	(S3, '3 Sets'),
	# 	(S4, '4 Sets'),
	# 	(S5, '5 Sets'),
	# 	(S6, '6 Sets')
	# ]
	# sets = models.CharField(max_length=1, choices=SETS_CHOICES, default=S3)
	sets = models.IntegerField(default=4)
	repetitions = models.IntegerField(default=6) #repetions per set
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
		null=True,
	)
	training = models.OneToOneField(
		Training,
		on_delete=models.CASCADE,
		blank=True,
		related_name='training_dend'
	)
	session_counter = models.IntegerField()
	comment = models.TextField(null=True, blank=True)
	def get_absolute_url(self):
		return reverse('record_list')

	class Meta:
			verbose_name_plural = "Deadhangs Endurance"

class Pullup_max(models.Model):
	date = models.DateTimeField(default=timezone.now)
	additional_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	body_weight = models.DecimalField(max_digits=5, decimal_places=2, default = 72)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
	)
	training = models.OneToOneField(
		Training,
		on_delete=models.CASCADE,
		blank=True,
		related_name='training_pmax'
	)
	session_counter = models.IntegerField()
	sets = models.IntegerField( default=3)
	repetitions = models.IntegerField(default=3)
	comment = models.TextField(null=True, blank=True)

	def get_absolute_url(self):
		return reverse('record_list')

	class Meta:
			verbose_name_plural = "Pullups Max"

class Pullup_endurance(models.Model):
	date = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
	)
	training = models.OneToOneField(
		Training,
		on_delete=models.CASCADE,
		blank=True,
		related_name='training_pend'
	)
	session_counter = models.IntegerField()
	sets = models.IntegerField( default=20)
	repetitions = models.IntegerField(default=5)
	comment = models.TextField(null=True, blank=True)
	#user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1, on_delete = models.CASCADE,)

	def get_absolute_url(self):
		return reverse('record_list')

	class Meta:
			verbose_name_plural = "Pullups Endurance"
