from django.urls import path

from . import views
app_name= 'db'
urlpatterns = [
	path('', views.index, name='index'),
	path('items/', views.items, name='items'),
	path('employees/', views.employees, name='employees'),

	path('additem/', views.additem, name='additem'),
	path('addemployee/', views.addemployee, name='addemployee'),
	
	path('employees/<int:employee_id>/', views.empdetail, name='empdetail'),
	path('items/<int:item_id>/', views.itemdetail, name='itemdetail'),
	path('assign/', views.assign_items, name='assign_items'),
	path('employees/<int:employee_id>/status/', views.status, name='status'),
	
	
]