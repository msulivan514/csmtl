"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import RequestContext
from datetime import datetime
from app.models import AgeGroup, Sex, EducationLevel
from app.models import WorkField, Province, UnemploymentToVacanciesRatio

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
def _GetWorkFieldAll():
   ret = dict()
   for workField in WorkField.objects.all():
      ret[workField.id] = workField.name
   return ret 

#----------------------------------------------------------------
def _GetProvincesAll():
   ret = dict()
   for province in Province.objects.all():
      ret[province.id] = province.name
   return ret 

#----------------------------------------------------------------
def filters(request):
    """Builds Json file with search filters"""
    assert isinstance(request, HttpRequest)

    filters = dict()
    filters["fields"] = _GetWorkFieldAll() 
    filters["grades"] = _GetEducLevelsAll()
    filters["provinces"] = _GetProvincesAll() 
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
    results[0] = 100
    results[1] = 90
    results[11] = 80

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
            'year':datetime.now().year,
        })
    )
