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

    #results = dict()
    #results['fieldID'] = fieldID
    #results['gradeID'] = gradeID
    #results['provID'] = provID
    #results['ageID'] = ageID
    #results['genderID'] = genderID

    #return JsonResponse(results)

    """the final score is F=aF1+(1-a)F2"""

    """Calcul du score F1 en %"""
    #genderID='Female'
    #ageID='15 to 24 years'
    #provID='Alberta'
    #fieldID='Construction'
    #gradeID='High school graduate'
    score_1=dict()
    print('%s, %s, %s,%s,%s',genderID, provID, ageID,fieldID,gradeID)
    F1=EmploymentRatio.objects.values_list('value',flat=True).filter(sex__id=genderID).filter(educLevel__id=gradeID).get(ageGroup__id=ageID)
       
    score_1['success']=F1
    print('%f',F1)

    """Calcul du score F2 en %"""
    """unemp est le taux d unemployment"""

    print "workfiel id %s, province id %s" %(fieldID, provID)
    score_2=dict()
    try:
        unemp = UnemploymentToVacanciesRatio.objects.filter( workField__id=fieldID, province__id=provID )
 #       unemp=UnemploymentToVacanciesRatio.objects.values_list('value',flat=True).filter(workField__id=fieldID).get(province__id=provID)
    except:
       print "unemp not found"
       unemp=None

    """gestion exception lorsque pas de data depuis dataset JVS incomplete"""
    """qualite_2 est la qualite de mesure, sous forme literale"""
    if (not unemp):
       cont=dict()
       print "unemp not found"
       cont['results']=F1
       return JsonResponse(cont)
    else:
           print('%f',unemp)
           temp=DataQuality.objects.get(workfield__name=fieldID)
           qualite_2=temp.name
    """F2 est la traduction en % de unemp. si unemp = 0, F2=100%, si unemp>=1, F2=0%"""
    """attention: eliminer data ou unemp n'existe pas  """
    if(unemp >=0 or unemp <=1):
          F2=100*(1-unemp)
          print('%f',F2)
    else:
          F2=0
    """Q2 est la ponderation de Qualite_2, ex: A=1, F=0.1"""

    if (qualite_2=='A'):
          Q2=1
    if (qualite_2=='B'):
          Q2=0.8
    if (qualite_2=='C'):
          Q2=0.6
    if (qualite_2=='D'):
          Q2=0.4
    if (qualite_2=='E'):
          Q2=0.2
    if (qualite_2=='F'):
          Q2=0.1

    score_2['success']=F2
    score_2['qualite']=Q2
#    return JsonResponse(score_2)

    """Retourne la valeur de F"""
    a=1-Q2
    b=Q2
    print('%f,%f',a,b)
    results=dict()
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
