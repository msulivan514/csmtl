"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import RequestContext
from datetime import datetime

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

def filters(request):
    """Builds Json file with search filters"""
    assert isinstance(request, HttpRequest)

    filters = dict()

    fields = dict()
    fields[0] = "field1"
    fields[1] = "field2"
    fields[2] = "field3"

    grades = dict()
    grades[0] = "grade1"
    grades[1] = "grade2"
    grades[2] = "grade3"

    provinces = dict()
    provinces[0] = "province1"
    provinces[1] = "province2"
    provinces[2] = "province3"

    ages = dict()
    ages[0] = "12-17"
    ages[1] = "18-24"
    ages[2] = "25-45"

    sex = dict()
    sex[0] = "male"
    sex[1] = "female"
    
    filters["fields"] = fields
    filters["grades"] = grades
    filters["provinces"] = provinces
    filters["ages"] = ages
    filters["sex"] = sex
    
    return JsonResponse(filters)

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
