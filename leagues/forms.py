from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import FileInput, CheckboxSelectMultiple, SelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import *
from individualleague.models import *
from django.forms import DateTimeInput

class CreateLeagueForm(forms.ModelForm):

    class Meta:
        model = league
        fields = ['name']

class UpdateLeagueForm(forms.ModelForm):
    logo=forms.FileField(widget=FileInput,required=False)
    
    def __init__(self, *args, **kwargs):
        
        super(UpdateLeagueForm, self).__init__(*args, **kwargs)
        self.fields["host"].widget = FilteredSelectMultiple("User", False, attrs={'rows':'2'})
        self.fields["host"].queryset = User.objects.all().order_by('username')

    class Meta:
        model = league
        fields = ['name','host','logo']

class UpdateLeagueSettingsForm(forms.ModelForm):

    class Meta:
        model = league_settings
        fields = ['is_recruiting','number_of_teams','number_of_conferences','number_of_divisions','teambased','allows_teams','is_public']

class LeagueConfigurationForm(forms.ModelForm):

    class Meta:
        model = league_configuration
        exclude=[]
        widgets = {
            'league': forms.HiddenInput(),
            }


class CreateTierForm(forms.ModelForm):
    
    class Meta:
        model = leaguetiers
        fields = ['league','subleague','tiername','tierpoints']
        widgets = {
            'league': forms.HiddenInput(),'subleague': forms.HiddenInput(),
            }

class UpdateTierForm(forms.ModelForm):
    
    class Meta:
        model = leaguetiers
        fields = ['league','subleague','tiername','tierpoints']
        widgets = {
            'league': forms.HiddenInput(),'subleague': forms.HiddenInput(),
            }

class UpdateCoachInfoForm(forms.ModelForm):
    logo=forms.FileField(widget=FileInput)

    class Meta:
        model = coachdata
        fields = ['logo','teamabbreviation','teamname']

class UpdateCoachRecordForm(forms.ModelForm):

    class Meta:
        model = coachdata
        fields = ['wins','losses','differential','streak','forfeit']

class UpdateCoachTeammateForm(forms.ModelForm):
    teammate = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = coachdata
        fields = ['teammate']


class UpdateParentTeamForm(forms.ModelForm):

    class Meta:
        model = coachdata
        fields = ['parent_team']

    def __init__(self,league, *args, **kwargs):
        super(UpdateParentTeamForm, self).__init__(*args, **kwargs)
        self.fields['parent_team'].queryset = league_team.objects.all().filter(league=league).order_by('name')
        self.fields['parent_team'].label_from_instance = lambda obj: obj.name  

class CreateSeasonSettingsForm(forms.ModelForm):

    class Meta:
        model = seasonsetting
        fields = ['league','subleague','seasonname','number_of_teams','draftbudget','drafttype','picksperteam','seasonlength','playoffslength','freeagenciesallowed','tradesallowed','numzusers','candeletez']
        widgets = {
            'league': forms.HiddenInput(),
            'subleague': forms.HiddenInput(),
            }

class EditSeasonSettingsForm(forms.ModelForm):

    seasonstart = forms.DateTimeField(label='Season Start: (Format=YYYY-MM-DD HH:MM) Timezone=UTC' , required=False )
    draftstart = forms.DateTimeField(label='Draft Start: (Format=YYYY-MM-DD HH:MM) Timezone=UTC' , required=False )

    class Meta:
        model = seasonsetting
        fields = ['seasonname','number_of_teams','draftstart','drafttimer','draftbudget','drafttype','seasonstart','seasonlength','playoffslength','freeagenciesallowed','tradesallowed','numzusers','candeletez']
        
class ManageCoachForm(forms.ModelForm):
    logo=forms.FileField(widget=FileInput,required=False)
    
    class Meta:
        model = coachdata
        fields = ['coach','teamname','teamabbreviation','logo','parent_team','teammate','conference','division']

    def __init__(self,league,subleague, *args, **kwargs):
        super(ManageCoachForm, self).__init__(*args, **kwargs)
        self.fields['coach'].queryset = User.objects.all().order_by('username')
        self.fields['conference'].queryset = conference_name.objects.filter(subleague=subleague).order_by('name')

        self.fields['division'].queryset = division_name.objects.filter(subleague=subleague).order_by('name')
        self.fields['division'].required = False
        self.fields['teammate'].required=False
        self.fields['teammate'].queryset = User.objects.all().order_by('username')
        self.fields['parent_team'].queryset = league_team.objects.all().filter(league=league).order_by('name')
        self.fields['parent_team'].label_from_instance = lambda obj: obj.name
        self.fields['parent_team'].required=False

class DesignateZUserForm(forms.Form):
    zuser = forms.ModelChoiceField(queryset=roster.objects.all().filter(pokemon__isnull=False), required=True)
    zmovetype = forms.ChoiceField(choices=(
        ("OS","Offensive & Status"),
        ("O","Offensive"),
    ))
    class Meta:
        fields = ['zuser','zmovetype']
    
    def __init__(self,season,team,*args, **kwargs):
        super(DesignateZUserForm, self).__init__(*args, **kwargs)
        self.fields['zuser'].queryset = roster.objects.all().filter(season=season,team=team,pokemon__isnull=False).order_by('pokemon__pokemon')
        self.fields['zuser'].label_from_instance = lambda obj: obj.pokemon.pokemon

class AddTeamOfCoachsForm(forms.ModelForm):
    
    class Meta:
        model=league_team
        exclude=['wins','losses','ties','points','gp','gw','differential']
        widgets = {'league': forms.HiddenInput()}
    
    def __init__(self,*args, **kwargs):
        super(AddTeamOfCoachsForm, self).__init__(*args, **kwargs)
        self.fields['captain'].queryset = User.objects.all().order_by('username')


class DiscordSettingsForm(forms.ModelForm):
    
    class Meta:
        model=discord_settings
        exclude=[]
        widgets = {'league': forms.HiddenInput(),'subleague': forms.HiddenInput()}

class CreateMatchForm(forms.ModelForm):
    
    class Meta:
        model = schedule
        fields = ['season','week','team1','team2']
        widgets = {'season': forms.HiddenInput()}

    def __init__(self,season,subleague, *args, **kwargs):
        super(CreateMatchForm, self).__init__(*args, **kwargs)
        self.fields['team1'].queryset = coachdata.objects.filter(subleague=subleague).order_by('teamname')
        self.fields['team1'].label_from_instance = lambda obj: obj.teamname
        self.fields['team2'].queryset = coachdata.objects.filter(subleague=subleague).order_by('teamname')
        self.fields['team2'].label_from_instance = lambda obj: obj.teamname
        c=[(i+1,i+1) for i in range(season.seasonlength)]
        d=[(f'Playoffs Round {i+1}',f'Playoffs Round {i+1}') for i in range(season.playoffslength-3)]
        e=[('Playoffs Quarterfinals','Playoffs Quarterfinals'),('Playoffs Semifinals','Playoffs Semifinals'),('Playoffs Third Place Match','Playoffs Third Place Match'),('Playoffs Finals','Playoffs Finals')]
        c=c+d+e
        self.fields['week']=forms.ChoiceField(choices=c)