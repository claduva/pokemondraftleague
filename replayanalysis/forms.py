from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from .models import *
from individualleague.models import schedule
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.db.models import Q

from leagues.models import *

class MatchReplayForm(forms.Form):
    url=forms.CharField(max_length=200,label="Replay URL")

class LeagueReplayForm(forms.ModelForm):
   
   class Meta:
        model = schedule
        fields = ['replay']

"""
class ManualLeagueReplayForm(forms.ModelForm):
    replay=forms.CharField(max_length=200,label="Replay")
    t1megaevolved=forms.BooleanField(label='Team 1 Mega Evolved',required=False)
    t2megaevolved=forms.BooleanField(label='Team 2 Mega Evolved',required=False)
    t1usedz=forms.BooleanField(label='Team 1 Used Z Move',required=False)
    t2usedz=forms.BooleanField(label='Team 2 Used Z Move',required=False)
    t1pokemon1=forms.ModelChoiceField(queryset = None,label='Team 1 Pokemon 1')
    t1pokemon2=forms.ModelChoiceField(queryset = None, label='Team 1 Pokemon 2')
    t1pokemon3=forms.ModelChoiceField(queryset = None, label='Team 1 Pokemon 3')
    t1pokemon4=forms.ModelChoiceField(queryset = None, label='Team 1 Pokemon 4')
    t1pokemon5=forms.ModelChoiceField(queryset = None, label='Team 1 Pokemon 5')
    t1pokemon6=forms.ModelChoiceField(queryset = None, label='Team 1 Pokemon 6')
    t2pokemon1=forms.ModelChoiceField(queryset = None, label='Team 2 Pokemon 1')
    t2pokemon2=forms.ModelChoiceField(queryset = None, label='Team 2 Pokemon 2')
    t2pokemon3=forms.ModelChoiceField(queryset = None, label='Team 2 Pokemon 3')
    t2pokemon4=forms.ModelChoiceField(queryset = None, label='Team 2 Pokemon 4')
    t2pokemon5=forms.ModelChoiceField(queryset = None, label='Team 2 Pokemon 5')
    t2pokemon6=forms.ModelChoiceField(queryset = None, label='Team 2 Pokemon 6')
    t1pokemon1kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t1pokemon2kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t1pokemon3kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t1pokemon4kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t1pokemon5kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t1pokemon6kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t2pokemon1kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t2pokemon2kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t2pokemon3kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t2pokemon4kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t2pokemon5kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t2pokemon6kills=forms.IntegerField(label='Kills',max_value=6,min_value=0)
    t1pokemon1death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t1pokemon2death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t1pokemon3death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t1pokemon4death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t1pokemon5death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t1pokemon6death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t2pokemon1death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t2pokemon2death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t2pokemon3death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t2pokemon4death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t2pokemon5death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    t2pokemon6death=forms.IntegerField(label='Deaths',max_value=1,min_value=0)
    winner=forms.ModelChoiceField(queryset=None,label='Winner')
    t1forfeit=forms.BooleanField(label='Team 1 Forfeited?',required=False)
    t2forfeit=forms.BooleanField(label='Team 2 Forfeited?',required=False)

    class Meta:
        model = manual_replay
        exclude = []
        widgets = {'match': forms.HiddenInput()}

    def __init__(self,match, *args, **kwargs):
        super(ManualLeagueReplayForm,self).__init__(*args, **kwargs)
        t1roster=roster.objects.all().filter(season=match.season,team=match.team1).exclude(pokemon__isnull=True)
        pokemonlist=[]
        for item in t1roster:
            pokemonlist.append(item.pokemon.id)
        t1queryset=all_pokemon.objects.all().filter(id__in=pokemonlist).order_by('pokemon')
        self.fields['t1pokemon1'].queryset = t1queryset
        self.fields['t1pokemon1'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t1pokemon2'].queryset = t1queryset
        self.fields['t1pokemon2'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t1pokemon3'].queryset = t1queryset
        self.fields['t1pokemon3'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t1pokemon4'].queryset = t1queryset
        self.fields['t1pokemon4'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t1pokemon5'].queryset = t1queryset
        self.fields['t1pokemon5'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t1pokemon6'].queryset = t1queryset
        self.fields['t1pokemon6'].label_from_instance = lambda obj: obj.pokemon
        t2queryset=all_pokemon.objects.all().order_by('pokemon')
        t2roster=roster.objects.all().filter(season=match.season,team=match.team2).exclude(pokemon__isnull=True)
        pokemonlist=[]
        for item in t2roster:
            pokemonlist.append(item.pokemon.id)
        t2queryset=all_pokemon.objects.all().filter(id__in=pokemonlist).order_by('pokemon')
        self.fields['t2pokemon1'].queryset = t2queryset
        self.fields['t2pokemon1'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t2pokemon2'].queryset = t2queryset
        self.fields['t2pokemon2'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t2pokemon3'].queryset = t2queryset
        self.fields['t2pokemon3'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t2pokemon4'].queryset = t2queryset
        self.fields['t2pokemon4'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t2pokemon5'].queryset = t2queryset
        self.fields['t2pokemon5'].label_from_instance = lambda obj: obj.pokemon
        self.fields['t2pokemon6'].queryset = t2queryset
        self.fields['t2pokemon6'].label_from_instance = lambda obj: obj.pokemon
        teams=set()
        teams.add(match.team1)
        teams.add(match.team2)
        self.fields['winner'].queryset = coachdata.objects.all().filter(Q(id=match.team1.id)|Q(id=match.team2.id))
        self.fields['winner'].label_from_instance = lambda obj: obj.teamname

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'match',
            Row(
                Column('t1pokemon1', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon1kills', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon1death', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon1', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon1kills', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon1death', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('t1pokemon2', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon2kills', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon2death', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon2', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon2kills', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon2death', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('t1pokemon3', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon3kills', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon3death', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon3', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon3kills', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon3death', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('t1pokemon4', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon4kills', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon4death', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon4', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon4kills', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon4death', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('t1pokemon5', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon5kills', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon5death', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon5', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon5kills', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon5death', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('t1pokemon6', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon6kills', css_class='form-group col-md-2 mb-0'),
                Column('t1pokemon6death', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon6', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon6kills', css_class='form-group col-md-2 mb-0'),
                Column('t2pokemon6death', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('t1megaevolved', css_class='form-group col-md-3 mb-0'),
                Column('t1usedz', css_class='form-group col-md-3 mb-0'),
                Column('t2megaevolved', css_class='form-group col-md-3 mb-0'),
                Column('t2usedz', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'winner',
            Row(
                Column('t1forfeit', css_class='form-group col-md-3 mb-0'),
                Column('t2forfeit', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'replay',
            Submit('submit', 'Submit')
        )
        """
