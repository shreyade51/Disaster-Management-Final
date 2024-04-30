from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DisasterList(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name


class States(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(States,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length=200)
    id_proof =  models.CharField(max_length = 100)
    business = models.CharField(max_length=100)

class Resource(models.Model):
    name =  models.CharField(max_length = 100)
    category =  models.CharField(max_length = 100)
    quantity = models.IntegerField()
    provider = models.ForeignKey(Contributor,on_delete=models.CASCADE)

    @property
    def remaining(self):
        n = self.quantity
        ra = ResourceAlloc.objects.filter(resource = self)
        for i in ra:
            n -= i.quantity
        return n

class Disaster(models.Model):
    name = models.CharField(max_length = 100)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    disaster = models.ForeignKey(DisasterList,on_delete=models.CASCADE)
    resources = models.ManyToManyField(Resource,related_name='disaster_resources',through='ResourceAlloc')
    reporttime = models.DateTimeField(auto_now_add = True)
    isactive = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    




class Volunteer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    isassigned = models.BooleanField(default= False)

    def __str__(self):
        return self.name

    
class VolunteerAssginment(models.Model):
    volunteer = models.ForeignKey(Volunteer,on_delete= models.CASCADE)
    disaster = models.ForeignKey(Disaster,on_delete=models.CASCADE)

class Task(models.Model):
    name = models.CharField(max_length = 100)
    disaster = models.ForeignKey(Disaster,on_delete = models.CASCADE)
    status = models.BooleanField(default = False)



class ResourceAlloc(models.Model):
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    disaster = models.ForeignKey(Disaster,on_delete=models.CASCADE)
    quantity = models.IntegerField()