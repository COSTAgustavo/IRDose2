from decimal import Decimal
import math
import numpy as np
import random
import subprocess

import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .models import CumActivity
from .forms import CumActivityCreateForm #IRDoseCreateForm, 
from .registerForm import RegisterForm



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'

class IRDoseListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
       return CumActivity.objects.filter(owner=self.request.user)

class IRDoseDetailView(LoginRequiredMixin, DetailView):

    model = CumActivity
    login_url = '/login/'

    def get_context_data(self, *args, **kwargs):
        context = super(IRDoseDetailView, self).get_context_data(*args, **kwargs)
        AC = CumActivity.objects.filter(owner=self.request.user)
        AC = AC.get(slug = kwargs['object'].slug)
        #AC.Organ = 'New'
        radioNuclide = AC.nuclidechoice
        print(radioNuclide)
        AB = AC.Organ
        argName = str(AC.Organ + AC.name)
        CT = str(AC.CT_Patient)
        source = str(AC.CT_Organ)
        target1 = str(AC.CT_Target_1)
        target2 = str(AC.CT_Target_2)
        if AC.CT_Target_1:
           target_1 = 'True'
           #subprocess.call('python DICOM_to_mhd_source.py' +argName + 'target_1', shell=True)
        else: 
           target_1 = 'False'
        
        if AC.CT_Target_2:
           target_2 = 'True'
           #subprocess.call('python DICOM_to_mhd_source.py' +argName + 'target_2', shell=True)

        else: 
           target_2 = 'False'

        print(argName, CT, source, target1, target_1, target2, target_2)

        t = [0, AC.t_1, AC.t_2, AC.t_3, AC.t_4]
        A = [0, AC.A_1, AC.A_2, AC.A_3, AC.A_4]
        AC.cumAct = cumActivity(t,A)
        CA = AC.cumAct
        Doses = [' ',' ',' ']
        if AC.doseAbs < 0:
            AC.doseAbs = 120
            AC.save()
            print('*************  Inside if')
            subprocess.call('python DICOM_to_mhd_source2.py ' + argName + ' ' + source + ' ' + target_1 + ' ' + target_2 + ' ' + target1 + ' ' + target2, shell=True)
            subprocess.call('python DICOM_to_mhd.py ' + argName + ' ' + CT, shell=True)
            print('*********************** Running -> Dose to Organs ***')
            subprocess.call('python doseToOrgans.py ' + argName + ' ' + target_1 + ' ' + target_2 + ' '+ str(CA), shell=True)        
        else:
            pass
        b = AC.doseAbs
        #a = str(subprocess.call('grep Dose dosimetrie/stdGATE/output/liverIRDSourceDose.txt', shell=True))
        with open('dosimetrie/stdGATE/output/'+argName+'SourceDose_'+str(CA)+'.txt') as reader_rad:           #Idem...
             i=0
             for  line in reader_rad:
               Doses[i] = line
               print(Doses[i])
               i+=1
        #GateS
        
        print(CA)
        context['title'] = 'Insert Cumulated activities'
        context['organ'] = b
        #context['doseA'] = AC.doseAbs
        context['doseS'] = Doses[0]
        if Doses[1]:
            context['dose_t1'] = Doses[1]
        if Doses[2]:
            context['dose_t2'] = Doses[2]
        context['CA'] = AC.cumAct
        #context = {'doseA':AC.doseAbs , 'CA':AC.cumAct}
        return context



class IRDoseCreateView(LoginRequiredMixin, CreateView):
    form_class = CumActivityCreateForm
    login_url = '/login/'
    template_name = 'IRDoseApp/form.html'
    #success_url = '/IRDoseApp/'

    def form_valid(self, form):
      instance = form.save(commit=False)
      instance.owner = self.request.user
      return super(IRDoseCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
       context = super(IRDoseCreateView, self).get_context_data(*args, **kwargs)
       context['title'] = 'Insert Cumulated activities'
       return context

class IRDoseUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CumActivityCreateForm
    model = CumActivity
    login_url = '/login/'
    template_name = 'IRDoseAPP/detail-update.html'
    success_url = '/IRDoseApp/'
    #
    # def get_queryset(self):
    #    queryset = CumActivity.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
       context = super(IRDoseUpdateView, self).get_context_data(*args, **kwargs)
       #AC = CumActivity.objects.filter(owner=self.request.user)
       #AC = AC.get(slug = kwargs['object'].slug)
       #if AC.doseAbs > 0:
       #print(AC.doseAbs)
       #AC.doseAbs = -10
       #    AC.save()
       #name = self.get_object().name
       #context['title'] = f'Update {name}'
       context['title'] = 'Update calcul'
       return context



def cumActivity(t,A):
    #for i in range(0,4):
    #  t = T_i
      #A[i] = CumActivity.objects.filter(name =t_
   #   A[i] = CumActivity.objects.filter(name=t)
    #print(A[i])
    return '%.2E' % Decimal((np.trapz(A,t,axis=0) + A[4]*np.exp(-t[4]*(np.log(2)/(6.6457*24))) / (np.log(2)/(6.6457*24)) )*math.pow(10,6)*3600)



#http://oddbird.net/2017/04/17/async-notifications/

# Channel('my-background-task').send(some_arguments)

# def websocket_connect(message):
#     # Accept connection
#     message.reply_channel.send({"accept": True})
#     Group(get_group_id_from(message)).add(message.reply_channel)

#     # In the front-end, where??
#     socket = new WebSocket("ws://" + window.location.host);
#     socket.onmessage = show_some_toast_for(message);
#     #Call onopen directly if socket is already open
#     if (socket.readyState == WebSocket.OPEN) socket.onopen();

# def my_background_task(message):
#     # ...
#     Group(get_group_id_from(message)).send({
#         "Simulating, please wait...": some_status_update,
#     })
#     # ...

