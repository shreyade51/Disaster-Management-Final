from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Location,Volunteer,Disaster,DisasterList,VolunteerAssginment,Task,States, Contributor, Resource, ResourceAlloc
from allauth.account.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'base.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        email = request.POST.get('email')
        password1 = request.POST.get('pass')
        password2 = request.POST.get('pass2')

        # Validate form data
        if password1 != password2:
            return HttpResponse('Password non match')

        # Check if username is unique
        if User.objects.filter(username=username).exists():
            return HttpResponse('Username already exists')

        # Check if email is unique
        if User.objects.filter(email=email).exists():
            return HttpResponse('email already exsists')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        loc = Location.objects.get(id = request.POST.get('loc'))

        volunteer = Volunteer(
            user = user,
            location = loc,
            name = request.POST.get('name'),
            dob = request.POST.get('dob')
        )
        volunteer.save()

        return redirect('account_login')
    location  = Location.objects.all()
    return render(request,'volunteers/register.html',context={'locations':location})


def newDisaster(request):
    if request.method == 'POST':

        disaster = Disaster(
            name = request.POST.get('name'),
            location = Location.objects.get(id = request.POST.get('loc')),
            disaster = DisasterList.objects.get(id = request.POST.get('type'))
        )

        disaster.save()
        return redirect('admindashboard')
    
    loc = Location.objects.all()
    disaster = DisasterList.objects.all()
    print(disaster)
    return render(request,'admin/newdisaster.html',context={'locs':loc,'disasters':disaster})



@login_required
def volunteerdashboard(request):
    if request.user.is_superuser:
        return redirect('admindashboard')
    if request.method == 'POST':
        disaster = Disaster.objects.get(id = request.POST.get('dis'))
        volunteer = Volunteer.objects.get(user = request.user)
        assginment =  VolunteerAssginment(
            volunteer = volunteer,
            disaster = disaster
        )
        assginment.save()
        volunteer.isassigned = True
        volunteer.save()
        return redirect('volunteerdashboard')

    tasks = False
    volunteer = Volunteer.objects.get(user = request.user)
    if volunteer.isassigned:
        tasks = Task.objects.filter(disaster = VolunteerAssginment.objects.get(volunteer=volunteer).disaster)
    return render(request,'volunteers/dashboard.html',context={'disasters':Disaster.objects.all(),'tasks':tasks,'isassigned':volunteer.isassigned})

def admindashboard(request):
    d = Disaster.objects.all()
    return render(request,'admin/dashboard.html',context={'disasters':d})

def adminvolunteers(request):
    v = Volunteer.objects.all()
    print(v.query)
    return render(request,'admin/volunteers.html',context={'volunteers':v})

def disastertasks(request):
    t = Task.objects.all()
    return render(request,'admin/task.html',context={'tasks':t})

def addtask(request):
    if request.method == 'POST':
        task = Task(
            name = request.POST.get('name'),
            disaster = Disaster.objects.get(id = request.POST.get('type'))
        )
        task.save()

        return redirect('admintasks')

    disaster = Disaster.objects.all()
    return render(request,'admin/newtask.html',context = {'disasters':disaster})


def edittask(request,id):
    if request.method == 'POST':
        t = get_object_or_404(Task, id=id)
        t.name = request.POST.get('name',t.name)
        t.status = request.POST.get('status','false') == 'true'
        t.save()
        return render(request,'admin/edittask.html',context={'task':t})
    t = Task.objects.get(id=id)
    return render(request,'admin/edittask.html',context={'task':t})


def addlocation(request):
    state = States.objects.all()
    if request.method == 'POST':
        s = get_object_or_404(States,id=request.POST.get('state'))
        l = Location(
            name = request.POST.get('loc'),
            state = s
        )
        l.save()
        return redirect('admindashboard')
    return render(request,'admin/addlocation.html',context={'states':state})

def location(request):
    l =Location.objects.all()
    return render(request,'admin/location.html',context={'locations':l})




def sendmapdata(request):
    count = {}
    for i in States.objects.all():
        count[i.name] = 0
    
    for i in Disaster.objects.filter(isactive=True):
        s = i.location.state
        count[s.name] = count[s.name] + 1
        
    data = [
        [],[],[],[],[]
    ]

    for i in count:
        if count[i] == 0:
            data[4].append(i)
        elif count[i] == 1:
            data[3].append(i)
        elif count[i] == 2:
            data[2].append(i)
        elif count[i] == 3:
            data[1].append(i)
        else:
            data[0].append(i)
    return JsonResponse({
        'data':data,
        'count':count
    })

def heatmap(request):

    return render(request,'admin/map.html')


def contributor(request):
    info = None
    if request.method == 'POST':
        c = Contributor(
            name = request.POST.get('name'),
            description = request.POST.get('desc'),
            id_proof = request.POST.get('id_proof'),
            business = request.POST.get('buss')
        )
        c.save()
        info = f'Use this id while contributing resources: {c.id}'
    return render(request,'contributor/register.html',context={'info':info})

def getresource(request):

    if request.method == 'POST':
        c = get_object_or_404(Contributor,id = request.POST.get('provider'))
        r = Resource(
            name = request.POST.get('name'),
            category = request.POST.get('cat'),
            quantity = request.POST.get('quantity'),
            provider = c
        )
        r.save()

    c = None
    if 'id' in request.GET:
        c_id = request.GET['id']
        try:
            c = Contributor.objects.get(id=c_id)
        except c.DoesNotExist:
            pass
    return render(request,'contributor/resource.html',context={'c':c})



def admincontributors(request):
    contributor = Contributor.objects.all()
    return render(request,'admin/contributor.html',context={'contributors':contributor})

def adminresources(request):
    resources = Resource.objects.all()
    return render(request,'admin/resources.html',context={'resources':resources})


def assignresource(request):
    resources = Resource.objects.all()
    disaster = Disaster.objects.all()
    if request.method == 'POST':
        ra = ResourceAlloc(
            resource = Resource.objects.get(id = request.POST.get('resource')),
            disaster = Disaster.objects.get(id = request.POST.get('disaster')),
            quantity = request.POST.get('quantity')
        )
        ra.save()
    return render(request,'admin/assignresource.html',context={'disasters':disaster,'resources':resources})

def resoucealloc(request):
    ra = ResourceAlloc.objects.all()
    return render(request,'admin/resourcealloc.html',context={'resources':ra})

def editdisaster(request,id):
    if request.method == 'POST':
        d = get_object_or_404(Disaster, id=id)
        d.name = request.POST.get('name',d.name)
        d.isactive = request.POST.get('status','false') == 'true'
        d.save()
        return render(request,'admin/editdisaster.html',context={'disaster':d})
    d = Disaster.objects.get(id=id)
    return render(request,'admin/editdisaster.html',context={'disaster':d})