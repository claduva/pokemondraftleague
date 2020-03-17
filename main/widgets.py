from django.forms import MultiWidget
from django.forms.widgets import FileInput,Select
from django_select2.forms import Select2Widget
from pokemonadmin.models import historical_team
from leagues.models import coachdata

class LogoUploadWidget(MultiWidget):
    def __init__(self, attrs,*args, **kwargs):
        imagelist=[]
        a=historical_team.objects.all().filter(coach1=attrs['user']).exclude(logo__contains="defaultleaguelogo").exclude(logo__contains="defaultteamlogo")
        for item in a:
            imagelist.append((f'h_{item.id}',item.logo.url))
        a=coachdata.objects.all().filter(coach=attrs['user']).exclude(logo__contains="defaultleaguelogo").exclude(logo__contains="defaultteamlogo")
        for item in a:
            imagelist.append((f'c_{item.id}',item.logo.url))
        widgets = [
            Select(choices=imagelist),
            FileInput(),
        ]
        super().__init__(widgets,attrs,*args, **kwargs)
    
    def decompress(self, value):     
        return [None,None]
    
    def value_from_datadict(self, data, files, name):
        img1,img2 = super().value_from_datadict(data, files, name)
        if img2:
            return img2
        else:
            sp=img1.split("_")
            img1=int(sp[1])
            if sp[0]=="h":
                a=historical_team.objects.all().get(id=img1)
            elif sp[0]=="c":
                a=coachdata.objects.all().get(id=img1)
            img1=a.logo
            return img1

    def render(self, name, value, attrs=None,renderer=None):
        initial=super(LogoUploadWidget, self).render(name, value, attrs)
        output1=initial.split("</select>")
        output1[0]+="</select>"
        output2=["<div>Choose Existing Logo:</div><div class='logoselect'>", output1[0],"</div><div>Or Upload New File:</div><div>",output1[1],"</div>"]
        output=""
        for s in output2:
            output+=s
        return(output)
