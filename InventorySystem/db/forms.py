from django import forms
from .models import Employee, Items

class EmpForm(forms.Form):
	emp_name=forms.CharField(label='Name', max_length=50)
	doj = forms.DateField(label='Date of Joining')

class ItemForm(forms.Form):
	item_name=forms.CharField(label='Name', max_length=100)
	quantity = forms.IntegerField(label='Quantity')
	item_type = forms.CharField(label='Type', max_length=50)
	price = forms.IntegerField(label='Price (Rs)')
	description = forms.CharField(label='Description',max_length=200, widget=forms.Textarea)

class EmpStatus(forms.Form):
	active = forms.CharField(label='Change Status',max_length=1)

class AssignmentForm(forms.Form):
	EMPLOYEE_NAME_CHOICES = []
	ITEM_CHOICES = []

	for emp in Employee.objects.all():
		name=emp.name
		EMPLOYEE_NAME_CHOICES.append((name,name))
	
	for item in Items.objects.all():
		name=item.name
		ITEM_CHOICES.append((name, name))
	
	emp_name=forms.CharField(
		label="Employee Name", 
		max_length=50,
		widget=forms.Select(choices=EMPLOYEE_NAME_CHOICES)
		
	)
	item_name=forms.CharField(
		label='Item Name', 
		max_length=100,
		widget=forms.Select(choices=ITEM_CHOICES))
	quantity = forms.IntegerField(label='Quantity')
	from_date=forms.DateField(label='From')
	to_date=forms.DateField(label='To')