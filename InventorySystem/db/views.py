from django.shortcuts import render
from .models import Employee, Items, ItemAssignment
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .forms import EmpForm, ItemForm, EmpStatus, AssignmentForm
# Create your views here.

#Show All Options
def index(request):
	return render(request, 'db/index.html')

#List of Employees
def employees(request):
	all_employees=Employee.objects.all()
	return render(request, 'db/employees.html',{'all_employees':all_employees})

#List of Items
def items(request):
	all_items=Items.objects.all()
	return render(request,'db/items.html',{'all_items':all_items})

#Detail of each Item
def itemdetail(request, item_id):
	try:
		item=Items.objects.get(pk=item_id)
	except Items.DoesNotExist:
		raise Http404("Item does not exist")
	return render(request, 'db/itemdetails.html',{'item':item})

#Detail of each employee
def empdetail(request, employee_id):
	try:
		employee=Employee.objects.get(pk = employee_id)
	except Employee.DoesNotExist:
		raise Http404("Employee does not exist")
	return render(request, 'db/empdetails.html',{'employee':employee})

#Adding New Employee
def addemployee(request):
	if request.method == 'POST':
		form = EmpForm(request.POST)
		if form.is_valid():
			name = request.POST['emp_name']
			doj = request.POST['doj']

			emp = Employee.objects.create(
				name = name,
				doj= doj,
				)
			emp.save()
			return HttpResponseRedirect('')
	else:
		form = EmpForm()
	return render(request, 'db/addemp.html', {'form': form})

#Adding New Item
def additem(request):
	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			name=request.POST['item_name']
			qty=request.POST['quantity']
			item_type=request.POST['item_type']
			price=request.POST['price']
			desc=request.POST['description']
			all_items=Items.objects.all()
			for item in all_items:
				if (item.name == name and item.type == item_type and item.price == price and item.description == desc):
					item.quantity += int(qty)
					item.save()
					return render(request,'db/items.html',{'all_items':all_items})
				else:
					item = Items.objects.create(
						name= name,
						quantity=qty,
						type=item_type,
						price=price,
						description=desc,
						)
					item.save()
					return render(request,'db/items.html',{'all_items':all_items})
	else:
		print("Try Again")
		form = ItemForm()
	return render(request, 'db/additem.html', {'form':form})

def assign_items(request):
	form_class = AssignmentForm
	form = form_class(request.POST or None)
	if request.method == 'POST':
		
		if form.is_valid():
			emp_name = request.POST['emp_name']
			item_name = request.POST['item_name']
			qty = request.POST['quantity']
			from_date = request.POST['from_date']
			to_date = request.POST['to_date']

			emp_selected = Employee.objects.get(name = emp_name)
			if emp_selected.active == "Y":
			
				item_selected = Items.objects.get(name = item_name)
				
				item_qty = item_selected.quantity
				if item_qty >= int(qty):
					item_selected.quantity -= int(qty)
					item_selected.save()

					item_assignment = ItemAssignment.objects.create(
							emp_id = emp_selected,
							item_id = item_selected,
							quantity = qty,
							from_date = from_date,
							to_date = to_date,
						)
					item_assignment.save()
					return HttpResponseRedirect('')
				else:
					return HttpResponse("Insufficient Items in Inventory")
			else: 
				return HttpResponse("Employee not active")
			
		else:
			form = AssignmentForm()
	return render(request, 'db/assign.html',{'form':form})


def status(request, employee_id):
	employee=Employee.objects.get(pk = employee_id)
	if request.method == 'POST':
		form = EmpStatus(request.POST)
		if form.is_valid():
			status=request.POST['active']
			employee.active = status
			employee.save()
			if status == "N":
				for i in employee.itemassignment_set.all():
					i.item_id.quantity+=i.quantity
					i.item_id.save()
					i.delete()
			return HttpResponseRedirect('')
	else:
		form = EmpStatus()
	return render(request, 'db/status.html',{'employee':employee,'form':form})





'''def assignitems(request):
	try:
		selected_employee='''
