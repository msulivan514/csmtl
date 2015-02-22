"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import RequestContext
from django.db.models import *
from datetime import datetime
from app.models import *

#----------------------------------------------------------------
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home',
            'year':datetime.now().year,
        }))

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
def getProvinceChance(fieldID, gradeID, provID, ageID, genderID):
    """Crunches the whole data with inputs from the user and return dictionary as a result"""

    try:
        # min/max ratio of unemployment VS vacancies for this field
        minMaxRatio = UnemploymentToVacanciesRatio.objects.aggregate(Min('value'), Max('value'))
        minRatio = minMaxRatio["value__min"]
        maxRatio = minMaxRatio["value__max"]
        
        # F1
        employmentRatio = EmploymentRatio.objects.values_list('value',flat=True).filter(sex__id=genderID).filter(educLevel__id=gradeID).get(ageGroup__id=ageID)
        F1 = employmentRatio

        # compute F2
        F2 = 0
        C1 = 1
        C2 = 0

        unEmploymentRatios = UnemploymentToVacanciesRatio.objects.filter(workField__id=fieldID, province__id=provID)
        if(len(unEmploymentRatios) > 0):
            unEmploymentRatioValue = unEmploymentRatios[0].value;
        
            # slope
            slope = (100 - 5) / (minRatio - maxRatio)
            offset = 100 - slope*minRatio
            F2 = (slope * unEmploymentRatioValue) + offset
            if(F2 < 0.1):
                return None

            # data quality
            dataQuality = DataQuality.objects.get(workfield__id=fieldID)
            dataQualityName = dataQuality.name
            dataQualityFactors = {
                'A':0.85,
                'B':0.73,
                'C':0.65,
                'D':0.46,
                'E':0.38,
                'F':0.1
            }
            dataQualityFactor = dataQualityFactors[dataQualityName];

            # compute C1 and C2
            C1 = 1 - dataQualityFactor
            C2 = dataQualityFactor

        # impact results
        overallChance = C1*F1 + C2*F2
        
        return overallChance

    except Exception as e:
        # general error, no results
        print e
        return None

#----------------------------------------------------------------
def search(request, fieldID, gradeID, ageID):
    """Crunches the whole data with inputs from the user and return json as a result"""
    assert isinstance(request, HttpRequest)

    results = dict()

    provinces = _GetProvincesAll()
    genders = _GetSexAll()

    for provId in provinces.keys():
        byGenders = dict()
        for genderId in genders.keys():
            chance = getProvinceChance(fieldID, gradeID, provId, ageID, genderId)
            if(chance == None):
                continue
            byGenders[genderId] = chance
            results[provId] = byGenders;

    return JsonResponse(results)

#----------------------------------------------------------------
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'year':datetime.now().year,
        }))

#----------------------------------------------------------------
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'year':datetime.now().year,
        }))
