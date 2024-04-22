import requests
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django import views

def chart_list(request):
    return render(request, "index.html")

def chartBar(request):
    legend = ['铁路', '航空'],
    xAxis = ['2013', '2014', '2015', '2016', '2017', '2018',
             '2019', '2020', '2021', '2022', '2023'],
    series = [
        {
            "name": '铁路',
            "type": 'bar',
            "data": [21.06, 23.2,  25.35, 27.7, 30.3, 33.17, 36.6, 22.0, 26.1,  16.1, 36.8 ],
        },
        {
            "name": '航空',
            "type": 'bar',
            "data": [3.54, 3.92, 4.36, 4.88, 5.52, 6.1, 6.6, 4.2, 4.4, 5.7, 6.2 ]
        }
    ]

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "xAxis": xAxis,
            "series": series
        }
    }
    return JsonResponse(result)