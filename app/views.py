"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import RequestContext
from datetime import datetime
from app.models import AgeGroup, Sex, EducationLevel

#----------------------------------------------------------------
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

#----------------------------------------------------------------
def _GetEducLevelsAll():
   ret = dict()
   for level in EducationLevel.objects.all():
      ret[level.id] = level.name
   return ret

#----------------------------------------------------------------
def _GetSexAll():
   ret = dict()
   for sex in Sex.objects.all():
      ret[sex.id] = sex.name
   return ret

#----------------------------------------------------------------
def _GetAgeGroupAll():
   ret = dict()
   for ageGroup in AgeGroup.objects.all():
      ret[ageGroup.id] = ageGroup.name
   return ret

#----------------------------------------------------------------
def filters(request):
    """Builds Json file with search filters"""
    assert isinstance(request, HttpRequest)

    filters = dict()

    fields = dict()
    fields[0] = "field1"
    fields[1] = "field2"
    fields[2] = "field3"

    provinces = dict()
    provinces[0] = "province1"
    provinces[1] = "province2"
    provinces[2] = "province3"

    filters["fields"] = fields
    filters["grades"] = _GetEducLevelsAll()
    filters["provinces"] = provinces
    filters["ages"] = _GetAgeGroupAll()
    filters["sex"] = _GetSexAll()
    
    return JsonResponse(filters)

#----------------------------------------------------------------
def search(request, fieldID, gradeID, provID, ageID, genderID):
    """Crunches the whole data with inputs from the user and return json as a result"""
    assert isinstance(request, HttpRequest)
    
    # add code to compute fitness functions f1 and f2
    # given inputs in parameters

    results = dict()
    results['fieldID'] = fieldID
    results['gradeID'] = gradeID
    results['provID'] = provID
    results['ageID'] = ageID
    results['genderID'] = genderID

    return JsonResponse(results)

#----------------------------------------------------------------
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

#----------------------------------------------------------------
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
