#!python3.6#    def get_object(self, *args, **kwargs):
#       app_id = self.kwargs.get('app_id')
#       obj = get_object_or_404(CumActivity, id=app_id)  #or: pk = app_id
#       return obj
#    def get_object(self, *args, **kwargs):
#       app_id = self.kwargs.get('app_id')
#       obj = get_object_or_404(CumActivity, id=app_id)  #or: pk = app_id
#       return obj
#    def get_object(self, *args, **kwargs):
#       app_id = self.kwargs.get('app_id')
#       obj = get_object_or_404(CumActivity, id=app_id)  #or: pk = app_id
#       return obj

from decimal import Decimal
import math
import numpy as np
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .models import CumActivity
from .forms import IRDoseCreateForm, CumActivityCreateForm

@login_required()
def IRDose_createview(request):
    form = CumActivityCreateForm(request.POST or None)    
    errors = None
    if form.is_valid():
       if request.user.is_authenticated():
          instance = form.save(commit=False)
          instance.owner = request.user
          instance.save()
          return HttpResponseRedirect("/IRDoseApp/")
       else:
          return HttpResponseRedirect("/login/")
            
    if form.errors:
      errors = form.errors
    template_name = 'IRDoseApp/form.html'
    context = {"form":form, "errors":errors}
    return render(request, template_name, context) 

def IRDose_listView(request):
    template_name = 'IRDoseApp/IRDoseList.html'
    queryset = CumActivity.objects.all()
    context = {
       "object_list": querySet
    }
    return render(request, template_name, context)

class IRDoseListView(ListView):
#    template_name = 'IRDoseApp/IRDoseList.html'

    def get_queryset(self):
       slug = self.kwargs.get("slug")
       if slug:
           queryset = CumActivity.objects.filter(
                  Q(location__iexact=slug) |
                  Q(location__icontains=slug)
           )
       else:
           queryset = CumActivity.objects.all()
       return queryset

class IRDoseDetailView(DetailView):
    queryset = CumActivity.objects.all()

### Convert queryset into array ?? Where?
#    t = np.empty[5]
#    A = np.empty[5]
#    for i in range(0,4):
#        t[i] = CumActivity.objects.filter(t_str(i))
#        A[i] = CumActivity.objects.filter(A_str(i))
#    CA = cumActivity(t,A)
#    print(CA)


class IRDoseCreateView(LoginRequiredMixin, CreateView):
    form_class = CumActivityCreateForm
    login_url = '/login/'
    template_name = ('IRDoseApp/form.html')
    #success_url = '/IRDoseApp/'
   
    def form_valid(self, form):
      instance = form.save(commit=False)
      instance.owner = self.request.user
      return super(IRDoseCreateView, self).form_valid(form)
   
    def get_context_data(self, *args, **kwargs):
       context = super(IRDoseCreateView, self).get_context_data(*args, **kwargs)
       context['title'] = 'Insert Cumulated activities'
       return context

def cumActivity(t,A):
    #for i in range(0,4):
    #  t = T_i
      #A[i] = CumActivity.objects.filter(name=t_ 
   #   A[i] = CumActivity.objects.filter(name=t)
    #print(A[i])
    return '%.2E' % Decimal((np.trapz(A,t,axis=0) + A[4]*np.exp(-t[4]*(np.log(2)/(6.6457*24))))*math.pow(10,6)*3600)

