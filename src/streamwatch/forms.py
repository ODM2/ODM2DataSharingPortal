from re import I
from attr import field
from django import forms
#from .models import LeafPack, LeafPackType, Macroinvertebrate, LeafPackBug, LeafPackSensitivityGroup
from django.forms import formset_factory
from streamwatch import models

from typing import Dict
from typing import Any

place_holder_choices = (
        (1, 'Choice #1'), 
        (2, 'Choice #2'),
        (3, 'Choice #3')
    )

measurement_method_choices = (('Meter','Meter'), ('Lamotte', 'Lamotte'))

class MDLCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'mdl-checkbox-select-multiple.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context['choices'] = [choice[1][0] for choice in context['widget']['optgroups']]
        context['name'] = name
        return self._render(self.template_name, context, renderer)

class SetupForm(forms.Form):
    
    ACTIVITY_TYPE_CHOICES = (('School', 'School Program'),('chemical', 'Chemical Action Team'), ('biological', 'Biological Action Team'), ('baterial', 'Baterial Action Team'))

    investigator1 = forms.CharField(
        required=False,
        label='Investigator #1'
    )       
    investigator2 = forms.CharField(
        required=False,
        label='Investigator #2'
    )   
    collect_date = forms.DateField(
        required=False,
        label='Date'
    )
    collect_time = forms.TimeField(
        required=False,
        label='Time'
    )
    project_name = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Project Name',
        choices= place_holder_choices,
        initial='1'
    )
    reach_length = forms.FloatField(
        label='Approximate Reach Length',
        required=False,
    )
    # mutiple choices
    activity_type = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        label='Activity type(s)',
        required=True,
        choices = ACTIVITY_TYPE_CHOICES)    

    
class ConditionsForm(forms.Form):
    
    #TODO - PRT verify and delete if these are not required
    # types = forms.ModelMultipleChoiceField(
    #     widget=MDLCheckboxSelectMultiple,
    #     label='Activity type(s):',
    #     required=True,
    #     queryset=LeafPackType.objects.filter(created_by=None),
    # )

    #Wildlife Observations
    # wildlife_obs = forms.ModelMultipleChoiceField(
    #     widget=MDLCheckboxSelectMultiple,
    #     required=True,
    #     label='Wildlife Observations:',
    #     queryset= models.variable_choice_options('wildlife'),
    # )
    
    # Visual Assessment (All Forms)
    weather_cond = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='Current Weather Conditions',
        choices= models.variable_choice_options('weather'),
    )
    time_since_last_precip = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Time Since Last Rain or Snowmelt',
        choices= models.variable_choice_options('precipitation'),
        initial='1'
    )    
    water_color = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Water Color:',
        choices= models.variable_choice_options('waterColor'),
        initial='1'
    )
    water_odor = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='Water Odor',
        choices= models.variable_choice_options('waterOdor'),
    )
    turbidity_obs = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Turbidity',
        choices= models.variable_choice_options('turbidity'),
        initial='1'
    )
    water_movement = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Water Movement',
        choices= models.variable_choice_options('waterMovement'),
        initial='1'
    )
    aquatic_veg_amount = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Aquatic Vegetation Amount',
        choices= models.variable_choice_options('aquaticVegetation'),
        initial='1'
    )
    aquatic_veg_type = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='Aquatic Vegetation Type',
        choices= models.variable_choice_options('aquaticVegetationType'),
    )
    surface_coating = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='Surface Coating',
        choices= models.variable_choice_options('surfaceCoating'),
    )
    algae_amount = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Algae Amount',
        choices= models.variable_choice_options('algaeAmount'),
        initial='1'
    )
    algae_type = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='Algae Type',
        choices= models.variable_choice_options('algaeType'),
    )
    site_observation = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        label='General Comments and Site Observations'
    )   
    
    #TODO - PRT This is not being displayed on the condition template,
    #this should likely be pulled into a separate form (e.g. BATForm)
    # In-stream Habitat Assessment (BAT form)  
    instream_structure = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='In-Stream Structures',
        choices= models.variable_choice_options('instreamStructures'),
    )
    stream_flow = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Stream Flow',
        choices= models.variable_choice_options('streamFlow'),
        initial='1'
    )
    percent_riffle = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Percent Riffle Morphology',
        choices= place_holder_choices,
        initial='1'
    )
    percent_run = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Percent Run Morphology',
        choices= place_holder_choices,
        initial='1'
    )
    percent_pool = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Percent Pool Morphology',
        choices= place_holder_choices,
        initial='1'
    )
    woody_debris_amt = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Woody Debris Amount',
        choices= models.variable_choice_options('woodyDebris'),
        initial='1'
    )
    macroinvert_habitat_type = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='Macroinvertebrate Habitat Types',
        choices= models.variable_choice_options('macroinvertHabitat'),
    )
    percent_silt_clay = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Percent Silt and Clay Substrate',
        choices= place_holder_choices,
        initial='1'
    )
    percent_sand = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Percent Sand Substrate',
        choices= place_holder_choices,
        initial='1'
    )
    percent_gravel = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Percent Gravel Substrate',
        choices= place_holder_choices,
        initial='1'
    )
    percent_cobble = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Percent Cobble Substrate',
        choices= place_holder_choices,
        initial='1'
    )
    percent_boulder = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Percent Boulder Substrate',
        choices= place_holder_choices,
        initial='1'
    )
    percent_bedrock = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Percent Bedrock Substrate',
        choices= place_holder_choices,
        initial='1'
    )
    
    #TODO - PRT This is not being displayed on the condition template,
    #this should likely be pulled into a separate form (e.g. BATForm)
    # Riparian Habitat Assessment (BAT form)
    bank_veg_type = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='Bank Vegetation Type',
        choices= models.variable_choice_options('bankVegetation'),
    )
    tree_canopy = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Tree Canopy Coverage',
        choices= models.variable_choice_options('treeCanopy'),
        initial='1'
    )
    land_use = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='Land Uses in 1/4 Mile Radius',
        choices= models.variable_choice_options('landuseQuarterMile'),
    )
    litter_amt = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Litter Concentration',
        choices= models.variable_choice_options('litter'),
        initial='1'
    )
    wildlife_obs = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=False,
        label='Wildlife Observations',
        choices= models.variable_choice_options('wildlife'),
    )
    macroinvert_sample_collect = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Macroinvertebrate Sample Collected?',
        choices= place_holder_choices,
        initial='1'
    )


class CATParameterForm(forms.Form):
    
    PARAMETER_CHOICES = (
        (1, 'Air Temperature'),
        (2, 'Dissolved Oxygen (mg/L)'),
        (3, 'Nitrate'),
        (4, 'Phosphate'),
        (5, 'pH'),
        (6, 'Specific Conductivity (uL/cm)'),
        (7, 'Total Dissolved Solids'),
        (8, 'Turbidity (JTU)'),
        (9, 'Water Temp (C)')
    )
    
    parameter = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        label='Parameter',
        choices= PARAMETER_CHOICES,
        # initial='1'
    )
    
    measurement = forms.FloatField(
        label='Measurement',
        required=True,
    )
    
    unit = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        label='Unit',
        choices= place_holder_choices,
        # initial='1'
    )


class CATParametersSet(forms.BaseFormSet):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, prefix='parameter', **kwargs)



class CATForm(forms.Form):
    meter = forms.CharField(
        required=False,
        label='pH Meter #'
    )     
    calibration_date = forms.DateField(
        required=False,
        label='Date of Last Calibration'
    )
    test_method = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Test Method',
        choices= place_holder_choices,
        initial='1'
    )
    parameters = formset_factory(CATParameterForm, formset=CATParametersSet, extra=3)

    
    def clean_data(self) -> Dict[str, Any]:
        cleaned = self.cleaned_data
        parameters  = {}
        for key in self.data:
            if 'parameter' not in key: continue
            _, index, attribute = key.split('-')
            if index not in parameters: parameters[index] = models.CATParameter()
            setattr(parameters[index], attribute, self.data[key])
        cleaned['parameters'] = list(parameters.values())
        return cleaned

#TODO - PRT Verify this form is no longer needed
class StreamWatchForm3(forms.Form):
    
    # Field Measurmenets (CAT/BaCT Forms)
    meter = forms.CharField(
        required=False,
        label='pH Meter #'
    )     
    calibration_date = forms.DateField(
        required=False,
        label='Date of Last Calibration'
    )
    test_method = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Test Method',
        choices= place_holder_choices,
        initial='1'
    )
    parameter = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Parameter',
        choices= place_holder_choices,
        initial='1'
    )
    unit = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Unit',
        choices= place_holder_choices,
        initial='1'
    )
    air_temp = forms.FloatField(
        label='Air Temperature',
        required=False,
    )
    water_temp = forms.FloatField(
        label='Water Temperature',
        required=False,
    )
    do1 = forms.FloatField(
        label='Dissolved Oxygen #1',
        required=False,
    )
    do2 = forms.FloatField(
        label='Dissolved Oxygen #2',
        required=False,
    )
    avg_do = forms.FloatField(
        label='Average Dissolved Oxygen',
        required=False,
    )
    spec_cond = forms.FloatField(
        label='Specific Conductivity',
        required=False,
    )
    pH = forms.FloatField(
        label='pH',
        required=False,
    )
    turbidity = forms.FloatField(
        label='Dissolved Oxygen #2',
        required=False,
    )
    tds = forms.FloatField(
        label='Total Dissolved Solids',
        required=False,
    )
    nitrate = forms.FloatField(
        label='Nitrate',
        required=False,
    )
    phosphate = forms.FloatField(
        label='Phosphate',
        required=False,
    )
    water_sample_collect = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Water Sample Collected?',
        choices= place_holder_choices,
        initial='1'
    )
    water_sample_type = forms.MultipleChoiceField(
        widget=MDLCheckboxSelectMultiple,
        required=True,
        label='Water Sample Types',
        choices= place_holder_choices,
    )
    wq_comments = forms.CharField(
        required=False,
        label='Comments about Water Quality Measurements',
        max_length=255
    )

    # Velocity (BAT form)
    rep_wetted_width = forms.FloatField(
        label='Representative Wetted Width',
        required=False,
    )
    rep_depth2 = forms.FloatField(
        label='Representative Depth Profile 2',
        required=False,
    )
    rep_depth3 = forms.FloatField(
        label='Representative Depth Profile 3',
        required=False,
    )
    rep_depth4 = forms.FloatField(
        label='Representative Depth Profile 4',
        required=False,
    )
    rep_depth5 = forms.FloatField(
        label='Representative Depth Profile 5',
        required=False,
    )
    avg_depth = forms.FloatField(
        label='Average Depth',
        required=False,
    )
    avg_float_time = forms.FloatField(
        label='Average Float Time',
        required=False,
    )
    avg_velocity = forms.FloatField(
        label='Average Velocity',
        required=False,
    )
    physical_assessment = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        label='Physical Assessment Conducted?',
        choices= place_holder_choices,
        initial='1'
    )

