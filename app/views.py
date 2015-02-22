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
#--------------------------------------------------------------

def score(ageGroup, sex, grade,metier, province)
"""the final score is F=aF1+(1-a)F2"""

    """Calcul du score F1 en %"""

    score_1=dict()
    F1=EmploymentRatio.objects.values_list('value',flat=True).filter(sex__name=sex).filter(educLevel__name=grade).filter(ageGroup__name=ageGroup)
    score_1['success']=F1[0]


    """Calcul du score F2 en %"""
    """unemp est le taux d unemployment"""
    """JVS pas encore definie"""

    score_2=dict()
    unemp= JVS.objects.values_list('value',flat=True).filter(name=metier).filter(province__name=province)
"""gestion exception lorsque pas de data depuis dataset JVS incomplete"""
        if (unemp)=[]:
                cont=dict()
                cont['results']="NA"
                return JsonResponse(cont)
        else:
    """qualite_2 est la qualite de mesure, sous forme literale"""

                qualite_2= JVS.objects.values_list('qualite',flat=True).filter(name=metier).filter(province__name=province)

    """F2 est la traduction en % de unemp. si unemp = 0, F2=100%, si unemp>=1, F2=0%"""
    """attention: eliminer data ou unemp n'existe pas  """
                if (unemp>=0 | unemp <=1):
                F2=100*(1-unemp)
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
                res=dict()
#----------------------------------------------------
