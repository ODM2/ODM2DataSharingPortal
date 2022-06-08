# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from dataloaderinterface.models import SiteRegistration
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView, BaseDetailView
from django.views.generic.detail import DetailView
from django.shortcuts import reverse, redirect
from django.http import HttpResponse
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from formtools.wizard.views import SessionWizardView, WizardView

from .forms import StreamWatchForm, StreamWatchForm2

class xStreamWatchCreateView(FormView):
    """
    Create View
    """
    form_class = StreamWatchForm
    template_name = 'streamwatch/streamwatch_form.html'
    slug_field = 'sampling_feature_code'
    object = None
    
    def get_context_data(self, **kwargs):
            # if 'leafpack_form' is in kwargs, that means self.form_invalid was most likely called due to a failed POST request
        if 'form' in kwargs:
            self.object = kwargs['form'].instance

        context = super(StreamWatchCreateView, self).get_context_data(**kwargs)

        context['sampling_feature_code'] = self.kwargs[self.slug_field]

        if self.object is None:
            site_registration = SiteRegistration.objects.get(sampling_feature_code=self.kwargs[self.slug_field])
            context['form'] = StreamWatchForm(initial={'site_registration': site_registration})

        return context

class StreamWatchCreateView(SessionWizardView):
    """
    Create View
    """
    #form_class = StreamWatchForm
    form_list = [StreamWatchForm, StreamWatchForm2]
    template_name = 'streamwatch/streamwatch_wizard.html'
    slug_field = 'sampling_feature_code'
    object = None
    
    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
            # if 'leafpack_form' is in kwargs, that means self.form_invalid was most likely called due to a failed POST request
        # if 'form' in kwargs:
        #     self.object = kwargs['form'].instance

        context = super(StreamWatchCreateView, self).get_context_data(**kwargs)

        context['sampling_feature_code'] = self.kwargs[self.slug_field]

        if self.object is None:
            site_registration = SiteRegistration.objects.get(sampling_feature_code=self.kwargs[self.slug_field])
            context['form'] = StreamWatchForm(initial={'site_registration': site_registration})

        return context