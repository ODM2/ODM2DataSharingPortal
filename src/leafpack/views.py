# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import csv
import io
import re
from tempfile import mkstemp
from datetime import date, timedelta
from functools import reduce
from operator import __or__ as OR

from django.db.models import Q
from dataloaderinterface.models import SiteRegistration
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView, BaseDetailView
from django.views.generic.detail import DetailView
from django.shortcuts import reverse, redirect
from django.http import HttpResponse
from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist

from .models import LeafPack, Macroinvertebrate, LeafPackType
from .forms import LeafPackForm, LeafPackBugForm, LeafPackBugFormFactory, LeafPackBug
from dataloaderinterface.views import LoginRequiredMixin

from csv_writer import LeafPackCSVWriter


class LeafPackFormMixin(object):
    def get_bug_count_forms(self, leafpack=None):
        re_bug_name = re.compile(r'^(?P<bug_name>.*)-bug_count')
        form_data = list()
        for key, value in self.request.POST.iteritems():
            if 'bug_count' in key:
                form_data.append((re_bug_name.findall(key)[0], value))

        bug_forms = list()
        for data in form_data:
            bug = Macroinvertebrate.objects.get(scientific_name=data[0])
            count = data[1]

            form = LeafPackBugForm(data={'bug_count'.format(bug.scientific_name): count})
            if leafpack is not None:
                form.instance = LeafPackBug.objects.get(leaf_pack=leafpack, bug=bug)
            else:
                form.instance.bug = bug

            bug_forms.append(form)

        return bug_forms

    def get_leafpack_types_other(self):
        lp_types = self.request.POST.get('types', None)

        if lp_types is None:
            return []


class LeafPackUpdateCreateMixin(LeafPackFormMixin):
    def forms_valid(self, forms):
        is_valid = True
        for form in forms:
            if not form.is_valid():
                is_valid = False
        return is_valid

    def get_object(self):
        return LeafPack.objects.get(id=self.kwargs['pk'])

    def add_types_other(self):
        """
        Creates new LeafPackTypes from self.request.POST['types_other'] (i.e., custom leaf pack types entered by user)
        :return: None
        """

        leafpack_types_other = self.request.POST.get('types_other', '')
        for other_type in leafpack_types_other.split(','):
            try:
                _ = LeafPackType.objects.get(name=other_type.strip())
            except ObjectDoesNotExist:
                LeafPackType.objects.create(name=other_type.strip(), created_by=self.request.user)


class LeafPackDetailView(DetailView):
    """
    Detail View
    """
    template_name = 'leafpack/leafpack_detail.html'
    slug_field = 'sampling_feature_code'
    model = LeafPack

    def get_object(self, queryset=None):
        return LeafPack.objects.get(id=self.kwargs['pk'])

    def get_taxon(self):
        lptaxons = []
        leafpack = self.get_object()

        # order taxon by pollution_tolerance, then by sort_priority in descending order
        taxon = Macroinvertebrate.objects.filter(family_of=None)\
            .order_by('pollution_tolerance')\
            .order_by('-sort_priority')

        # get subcategories of taxon
        for parent in taxon:
            parent_taxon = LeafPackBug.objects.get(leaf_pack=leafpack, bug=parent)
            child_taxons = []
            for child in parent.families.all().order_by('common_name'):
                child_taxons.append(LeafPackBug.objects.get(leaf_pack=leafpack, bug=child))
            lptaxons.append((parent_taxon, child_taxons))

        return lptaxons

    def get_context_data(self, **kwargs):
        context = super(LeafPackDetailView, self).get_context_data(**kwargs)
        context['leafpack'] = self.get_object()
        context['leafpack_bugs'] = self.get_taxon()
        context['sampling_feature_code'] = self.get_object().site_registration.sampling_feature_code

        return context


class LeafPackCreateView(LeafPackUpdateCreateMixin, CreateView):
    """
    Create View
    """
    form_class = LeafPackForm
    template_name = 'leafpack/leafpack_create.html'
    slug_field = 'sampling_feature_code'
    object = None

    def form_invalid(self, leafpack_form, bug_forms):
        context = self.get_context_data(leafpack_form=leafpack_form, bug_forms=bug_forms)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):

        # TODO: Probably get rid of this eventually...
        if not len(Macroinvertebrate.objects.all()):
            # If there are no macroinvertebrates in the database, run 'set_leafpackdb_defaults' command to populate
            # database with default macroinvertebrate and leaf pack types.
            call_command('set_leafpackdb_defaults')

        # if 'leafpack_form' is in kwargs, that means self.form_invalid was most likely called due to a failed POST request
        if 'leafpack_form' in kwargs:
            self.object = kwargs['leafpack_form'].instance

        context = super(LeafPackCreateView, self).get_context_data(**kwargs)

        context['sampling_feature_code'] = self.kwargs[self.slug_field]

        if 'leafpack_form' not in context:
            site_registration = SiteRegistration.objects.get(sampling_feature_code=self.kwargs[self.slug_field])
            context['leafpack_form'] = LeafPackForm(initial={'site_registration': site_registration})

        context['bug_count_form_list'] = LeafPackBugFormFactory.formset_factory()

        return context

    def post(self, request, *args, **kwargs):

        self.add_types_other()

        leafpack_form = self.get_form()
        bug_forms = self.get_bug_count_forms()

        if self.forms_valid([leafpack_form] + bug_forms):
            leafpack_form.save()

            for bug_form in bug_forms:
                LeafPackBug.objects.create(bug=bug_form.instance.bug, leaf_pack=leafpack_form.instance,
                                           bug_count=bug_form.cleaned_data['bug_count'])

            return redirect(reverse('site_detail', kwargs={'sampling_feature_code':
                                                           self.kwargs['sampling_feature_code']}))

        return self.form_invalid(leafpack_form, bug_forms)


class LeafPackUpdateView(LoginRequiredMixin, LeafPackUpdateCreateMixin, UpdateView):
    """
    Update view
    """
    form_class = LeafPackForm
    template_name = 'leafpack/leafpack_update.html'
    slug_field = 'sampling_feature_code'
    object = None

    def get_context_data(self, **kwargs):
        context = super(LeafPackUpdateView, self).get_context_data(**kwargs)

        context['sampling_feature_code'] = self.kwargs[self.slug_field]
        context['leafpack_bugform'] = LeafPackBugFormFactory.formset_factory(self.get_object())

        return context

    def post(self, request, *args, **kwargs):

        self.add_types_other()

        leafpack_form = LeafPackForm(request.POST, instance=self.get_object())
        bug_forms = self.get_bug_count_forms()

        if self.forms_valid([leafpack_form] + bug_forms):
            leafpack_form.save()

            for bug_form in bug_forms:
                bug = LeafPackBug.objects.get(bug=bug_form.instance.bug, leaf_pack=leafpack_form.instance)
                bug.bug_count = bug_form.cleaned_data['bug_count']
                bug.save()

            return redirect(reverse('leafpack:view', kwargs={self.slug_field: self.kwargs[self.slug_field],
                                                             'pk': self.get_object().id}))

        return self.form_invalid(leafpack_form)


class LeafPackDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete view
    """
    slug_field = 'sampling_feature_code'

    def get_object(self, queryset=None):
        return LeafPack.objects.get(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        leafpack = self.get_object()
        leafpack.delete()
        return redirect(reverse('site_detail', kwargs={self.slug_field: self.kwargs[self.slug_field]}))


def download_leafpack_csv(request, sampling_feature_code, pk):
    """
    Download handler that uses csv_writer.py to parse out a leaf pack expirement into a csv file.
    :param request: the request object
    :param sampling_feature_code: the first URL parameter
    :param pk: the second URL parameter and id of the leafpack experiement to download 
    """
    leafpack = LeafPack.objects.get(id=pk)
    site = SiteRegistration.objects.get(sampling_feature_code=sampling_feature_code)

    writer = LeafPackCSVWriter(leafpack, site)
    writer.write()

    # filename format: {Sampling Feature Code}_{Placement date}_{leafpack ID padded with zeros}.csv
    filename = '{}_{}_{:03d}.csv'.format(sampling_feature_code, leafpack.placement_date, int(pk))

    response = HttpResponse(writer.read(), content_type='application/csv')
    response['Content-Disposition'] = 'inline; filename={0}'.format(filename)

    return response
