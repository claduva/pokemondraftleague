def awardcheck(coach,awardtogive,awardtext,messagebody,admin):
    try:
        coachaward.objects.filter(coach=coach, award=awardtogive).get(text=awardtext)
    except:
        inbox.objects.create(sender=admin,recipient=coach,messagesubject='You have been awarded a trophy!', messagebody=messagebody)
        coachaward.objects.create(coach=coach,award=awardtogive,text=awardtext)

def findpoke(team1,team2,pokemonname,line_count):
    try:
        item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(pokemon__pokemon=pokemonname)
    except:
        try:
            item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(pokemon__pokemon=f'{pokemonname}-Mega')
        except:
            try:
                item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(pokemon__pokemon=f'{pokemonname}-Mega-X')
            except:
                try:
                    item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(pokemon__pokemon=f'{pokemonname}-Mega-Y')
                except:
                    try:
                        historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(droppedpokemon__pokemon=pokemonname)   
                        item=all_pokemon.objects.all().get(pokemon=pokemonname)
                    except Exception as e:
                        try:
                            historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(droppedpokemon__pokemon=f'{pokemonname}-Mega')   
                            item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega')
                        except:
                            try:
                                historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(droppedpokemon__pokemon=f'{pokemonname}-Mega-X')   
                                item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega-X')
                            except:
                                try:
                                    historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(droppedpokemon__pokemon=f'{pokemonname}-Mega-Y')   
                                    item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega-Y')
                                except:
                                    try:
                                        historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(droppedpokemon__pokemon=pokemonname)   
                                        item=all_pokemon.objects.all().get(pokemon=pokemonname)
                                    except Exception as e:
                                        try:
                                            historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(droppedpokemon__pokemon=f'{pokemonname}-Mega')   
                                            item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega')
                                        except:
                                            try:
                                                historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(droppedpokemon__pokemon=f'{pokemonname}-Mega-X')   
                                                item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega-X')
                                            except:
                                                try:
                                                    historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(droppedpokemon__pokemon=f'{pokemonname}-Mega-Y')   
                                                    item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega-Y')
                                                except:
                                                    try:
                                                        item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(pokemon__pokemon=pokemonname)
                                                    except:
                                                        try:
                                                            item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(pokemon__pokemon=f'{pokemonname}-Mega')
                                                        except:
                                                            try:
                                                                item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(pokemon__pokemon=f'{pokemonname}-Mega-X')
                                                            except:
                                                                try:
                                                                    item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(pokemon__pokemon=f'{pokemonname}-Mega-Y')
                                                                except:
                                                                    item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}')
                                                                    print(f'{line_count}. {pokemonname}')                      
    return item