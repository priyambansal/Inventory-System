from django.db import models

# Create your models here.
'''
class ItemManager(models.Manager):
	def unassign(self)
'''

class Items(models.Model):
	name = models.CharField(max_length=100)
	quantity = models.IntegerField()
	type = models.CharField(max_length=50)
	price = models.IntegerField()
	description = models.CharField(max_length=200)

	def __str__(self):
        	return self.name

class Employee(models.Model):
	name =  models.CharField(max_length=50)
	doj = models.DateField(auto_now=False, auto_now_add=False)
	active = models.CharField(max_length=1, default="Y")
	doe = models.DateField(auto_now=False, auto_now_add=False,null=True, blank=True)

	def __str__(self):
        	return self.name

class ItemAssignment(models.Model):
	emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
	item_id = models.ForeignKey(Items, on_delete=models.CASCADE, default=1)
	quantity = models.IntegerField()
	from_date = models.DateField(auto_now=False, auto_now_add=False)
	to_date = models.DateField(auto_now=False, auto_now_add=False,null=True, blank=True)

	def __str__(self):
		return '%s %s' % (self.emp_id, self.item_id)
'''

	def test(self, *args, **kwargs):
		item_object=Items().objects.get(name="some_item")
		item_object.quantity += 3
		item_object.save()
'''
'''
	def save(self, *args, **kwargs):
		if self.quantity == 0:
			return
		else:
			super().save(*args, **kwargs)         
'''