from django.core.management.base import BaseCommand
from job.models import Region, Town, Quarter

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        self.populate()

    def populate(self):
        data = {
            "Centre Region": {
                "towns": {
                    "Yaoundé": [
                        "Melen", "Nkolmesseng", "Etoudi", "Essos", 
                        "Mvog-Ada", "Nlongkak", "Bastos", "Nkoldongo", 
                        "Mokolo", "Biyem-Assi"
                    ],
                    "Obala": [
                        "Oyomabang", "Bokito", "Ekié", "Esseng", 
                        "Bité", "Nkolmebanga", "Olembe", "Ndong", 
                        "Mbang", "Nkolmewout"
                    ],
                    "Mbalmayo": [
                        "Afanoyoa", "Akonolinga", "Ebebda", "Nkongmesseng", 
                        "Nkolnda", "Nyom II", "Biteng", "Okong", 
                        "Logbikang", "Abem"
                    ],
                    "Monatele": [
                        "Etétak", "Ngali", "Manya", "Nkolmbong", 
                        "Edéa", "Nkoma", "Essele", "Bibé", 
                        "Ebogo", "Nkolbonzang"
                    ],
                    "Nanga Eboko": [
                        "Bibondo", "Nsom", "Mbam", "Ebonda", 
                        "Ngoumou", "Mbiko", "Essong", "Efok", 
                        "Siméon", "Etoun"
                    ],
                    "Eseka": [
                        "Baham", "Ndom", "Ngambé", "Libamba", 
                        "Bibaya", "Mbandjock", "Edéa", "Nyambé", 
                        "Mbanjock", "Ndong"
                    ],
                    "Ngoumou": [
                        "Akouda", "Mokolo", "Atout", "Biwong", 
                        "Ngousso", "Nyom II", "Nkolbisson", 
                        "Nkolguem", "Eloumden", "Ekoumdoum"
                    ],
                    "Bafia": [
                        "Moundou", "Olembe", "Yoko", "Nkondjock", 
                        "Bitcheu", "Manengouba", "Ebebda", "Lemba", 
                        "Makalengue", "Yaoundé II"
                    ],
                    "Mfou": [
                        "Nkolbisson", "Obala", "Okola", "Bokito", 
                        "Yebekolo", "Etoudi", "Bibé", "Olembe", 
                        "Mbandjock", "Djibouti"
                    ],
                    "Akono": [
                        "Nkolguem", "Mbele", "Nkolmeyang", "Essong", 
                        "Bilone", "Nkolbisson", "Ebogo", "Mekok", 
                        "Nkolmebanga", "Ebonda"
                    ]
                }
            },
            "Littoral Region": {
                "towns": {
                    "Douala": [
                        "Bonapriso", "Bonamoussadi", "Makepe", "Akwa", 
                        "Bepanda", "Bonanjo", "Deido", "Bali", 
                        "Ndokoti", "Bonaberi"
                    ],
                    "Nkongsamba": [
                        "Bouraka", "Mile 10", "Njombe", "Melong", 
                        "Baré", "Littoral", "Penja", "Ekom", 
                        "Manjo", "Matomb"
                    ],
                    "Edéa": [
                        "Pouma", "Eseka", "Songloulou", "Bidjocka", 
                        "Sanaga", "Makak", "Mouanko", "Songdong", 
                        "Evodoula", "Loum"
                    ],
                    "Loum": [
                        "Nkolmekok", "Njombe", "Mapak", "Melong II", 
                        "Matap", "Ngoklit", "Batentam", "Monbat", 
                        "Nkong", "Babong"
                    ],
                    "Manjo": [
                        "Mambengue", "Melong", "Ngwambo", "Bafang", 
                        "Ndom", "Nkongsamba II", "Mombo", "Mbouda", 
                        "Lobe", "Mbayangam"
                    ],
                    "Mbanga": [
                        "Ediki", "Ndjock-Nkong", "Muela", "Kombé", 
                        "Nyombé", "Eboné", "Ndoungue", "Ngundja", 
                        "Moutoukou", "Mouatong"
                    ],
                    "Melong": [
                        "Nkolla", "Njombe", "Makondo", "Ekang", 
                        "Bougna", "Manengouba", "Bouraka", "Batock", 
                        "Babou", "Soungo"
                    ],
                    "Pouma": [
                        "Mouanko", "Nkondjock", "Bivouba", "Malende", 
                        "Bidjocka", "Maka", "Mewoulou", "Ndogbon", 
                        "Mankom", "Bossa"
                    ],
                    "Yabassi": [
                        "Ebombe", "Makondo", "Mouton", "Meka", 
                        "Ndogpassi", "Bangou", "Ngambé", "Bonja", 
                        "Babenga", "Ekomé"
                    ],
                    "Penja": [
                        "Nyombé", "Njombe", "Nkola", "Bibondi", 
                        "Batieng", "Menou", "Soungo", "Bonamengue", 
                        "Mouanko", "Eboumé"
                    ]
                }
            },
            "West Region": {
                "towns": {
                    "Bafoussam": [
                        "Djeleng", "Banengo", "Kamkop", "Ngouache", 
                        "Tamdja", "Kouogouo", "Haoussa", "Tobe", 
                        "Toukouop", "Baham"
                    ],
                    "Dschang": [
                        "Foto", "Foreke", "Bamendjou", "Bandrefam", 
                        "Fongo-Tongo", "Fondonera", "Nkong-Ni", 
                        "Mbouda", "Baleng", "Nkong-Zem"
                    ],
                    "Bangangté": [
                        "Banekane", "Bapa", "Bangoulap", "Babété", 
                        "Bakong", "Bandjoun", "Baleng", "Bansoa", 
                        "Bassamba", "Bahouoc"
                    ],
                    "Foumban": [
                        "Njimom", "Foumbot", "Koutaba", "Bangourain", 
                        "Kena", "Magba", "Kankop", "Foumbot II", 
                        "Kouoptamo", "Mbouda"
                    ],
                    "Mbouda": [
                        "Baleng", "Babadjou", "Balessing", "Babété", 
                        "Bandjoun", "Bamendjou", "Bansoa", 
                        "Bamougoum", "Bahouoc", "Bapi"
                    ],
                    "Bafang": [
                        "Banwa", "Bamesso", "Batcha", "Bandja", 
                        "Babou", "Bana", "Bahouoc", "Batié", 
                        "Babadjou", "Bangangté"
                    ],
                    "Bamboutos": [
                        "Mbouda", "Babété", "Balessing", "Batcha", 
                        "Bapi", "Bahouoc", "Bamendjou", "Bansoa", 
                        "Babadjou", "Baham"
                    ],
                    "Bana": [
                        "Batchingou", "Batié", "Bamesso", "Babou", 
                        "Baham", "Bamendjou", "Bangoua", "Babété", 
                        "Mbouda", "Baleng"
                    ],
                    "Bandja": [
                        "Balounga", "Batcha", "Bamengou", "Bamendjou", 
                        "Bahouoc", "Bana", "Bangoua", "Bassamba", 
                        "Babong", "Bateng"
                    ],
                    "Bafou": [
                        "Batsangue", "Babeng", "Balessing", "Baboud", 
                        "Balessing II", "Babam", "Fombot", 
                        "Foto", "Fongo", "Foto-Balem"
                    ]
                }
            },
            "Southwest Region": {
                "towns": {
                    "Buea": [
                        "Molyko", "Great Soppo", "Bokwango", "Bomaka", 
                        "Bonduma", "Muea", "Tole", "Sandpit", 
                        "Mile 16", "Mile 17"
                    ],
                    "Limbe": [
                        "Limbe I", "Limbe II", "Limbe III", "Limbe IV", 
                        "Limbe V", "Limbe VI", "Limbe VII", "Limbe VIII", 
                        "Limbe IX", "Limbe X"
                    ],
                    "Tiko": [
                        "Bokwango", "Bota", "Mile 12", "Mile 16", 
                        "Mile 19", "Mile 17", "Mile 14", "Mile 15", 
                        "Mile 13", "Mile 11"
                    ],
                    "Bimbia": [
                        "Nkambe", "Mile 1", "Mile 2", "Mile 3", 
                        "Mile 4", "Mile 5", "Mile 6", "Mile 7", 
                        "Mile 8", "Mile 9"
                    ],
                    "Bole": [
                        "Bole I", "Bole II", "Bole III", "Bole IV", 
                        "Bole V", "Bole VI", "Bole VII", "Bole VIII", 
                        "Bole IX", "Bole X"
                    ],
                    "Mile 16": [
                        "Mile 16 I", "Mile 16 II", "Mile 16 III", "Mile 16 IV", 
                        "Mile 16 V", "Mile 16 VI", "Mile 16 VII", 
                        "Mile 16 VIII", "Mile 16 IX", "Mile 16 X"
                    ],
                    "Mile 17": [
                        "Mile 17 I", "Mile 17 II", "Mile 17 III", "Mile 17 IV", 
                        "Mile 17 V", "Mile 17 VI", "Mile 17 VII", 
                        "Mile 17 VIII", "Mile 17 IX", "Mile 17 X"
                    ],
                    "Wokoko": [
                        "Wokoko I", "Wokoko II", "Wokoko III", "Wokoko IV", 
                        "Wokoko V", "Wokoko VI", "Wokoko VII", 
                        "Wokoko VIII", "Wokoko IX", "Wokoko X"
                    ],
                    "Mile 19": [
                        "Mile 19 I", "Mile 19 II", "Mile 19 III", "Mile 19 IV", 
                        "Mile 19 V", "Mile 19 VI", "Mile 19 VII", 
                        "Mile 19 VIII", "Mile 19 IX", "Mile 19 X"
                    ],
                    "Bota": [
                        "Bota I", "Bota II", "Bota III", "Bota IV", 
                        "Bota V", "Bota VI", "Bota VII", 
                        "Bota VIII", "Bota IX", "Bota X"
                    ]
                }
            },
            "Northwest Region": {
                "towns": {
                    "Bamenda": [
                        "Mankon", "Bafut", "Bali", "Nkwen", 
                        "Nkwen II", "Bamenda II", "Bamenda III", 
                        "Bamenda IV", "Bamenda V", "Bamenda VI"
                    ],
                    "Donga Mantung": [
                        "Nkambe", "Ndu", "Jakiri", "Fungom", 
                        "Nwang", "Mbingo", "Ntem", "Balikumbat", 
                        "Tinto", "Wum"
                    ],
                    "Mezam": [
                        "Bafut", "Bali", "Nkwen", "Ndu", 
                        "Jakiri", "Fungom", "Nkambe", "Ntem", 
                        "Mbingo", "Tinto"
                    ],
                    "Momo": [
                        "Momo I", "Momo II", "Momo III", "Momo IV", 
                        "Momo V", "Momo VI", "Momo VII", 
                        "Momo VIII", "Momo IX", "Momo X"
                    ],
                    "Bui": [
                        "Bui I", "Bui II", "Bui III", "Bui IV", 
                        "Bui V", "Bui VI", "Bui VII", 
                        "Bui VIII", "Bui IX", "Bui X"
                    ],
                    "Boyow": [
                        "Boyow I", "Boyow II", "Boyow III", "Boyow IV", 
                        "Boyow V", "Boyow VI", "Boyow VII", 
                        "Boyow VIII", "Boyow IX", "Boyow X"
                    ],
                    "Ngoketunjia": [
                        "Ngoketunjia I", "Ngoketunjia II", "Ngoketunjia III", "Ngoketunjia IV", 
                        "Ngoketunjia V", "Ngoketunjia VI", "Ngoketunjia VII", 
                        "Ngoketunjia VIII", "Ngoketunjia IX", "Ngoketunjia X"
                    ],
                    "Momo": [
                        "Momo I", "Momo II", "Momo III", "Momo IV", 
                        "Momo V", "Momo VI", "Momo VII", 
                        "Momo VIII", "Momo IX", "Momo X"
                    ],
                    "Donga Mantung": [
                        "Donga Mantung I", "Donga Mantung II", "Donga Mantung III", "Donga Mantung IV", 
                        "Donga Mantung V", "Donga Mantung VI", "Donga Mantung VII", 
                        "Donga Mantung VIII", "Donga Mantung IX", "Donga Mantung X"
                    ]
                }
            },
             "Adamawa Region": {
                "towns": {
                    "Ngaoundéré": [
                        "Wakwa", "Bengui", "Belabo", "Djarengol"
                    ],
                    "Banyo": [
                        "Banyaga", "Baldé", "Djohong", "Ngog"
                    ],
                    "Meiganga": [
                        "Bari", "Koulfe", "Kongou", "Mbouda"
                    ],
                    "Tignere": [
                        "Goura", "Goulfey", "Bonguen", "Nkolnema"
                    ],
                    "Djerem": [
                        "Mendong", "Tibati", "Yagou", "Bikoro"
                    ],
                    "Lafon": [
                        "Baka", "Madou", "Ngoro", "Bokito"
                    ]
                }
            },
                  "Far North Region": {
                "towns": {
                    "Maroua": [
                        "Djado", "Poussari", "Ngalim", "Gobo"
                    ],
                    "Mokolo": [
                        "Koza", "Mogode", "Mayo", "Boko"
                    ],
                    "Kolofata": [
                        "Diba", "Ngoshe", "Mile 5", "Waza"
                    ],
                    "Kousséri": [
                        "Mokolo", "Waza", "Kona", "Mayo"
                    ],
                    "Bogo": [
                        "Bongo", "Kolofata", "Ngalim", "Guirvidig"
                    ],
                    "Goulfey": [
                        "Foulassi", "Mayo", "Nkolng", "Mouda"
                    ]
                }
            },
            "North Region": {
                "towns": {
                    "Garoua": [
                        "Ngong", "Goubé", "Poulou", "Madagali", 
                        "Kousseri", "Pitoa", "Mokolo", "Lomé", 
                        "Lagdo", "Tibati"
                    ],
                    "Maroua": [
                        "Bogo", "Mogodé", "Guérawa", "Moutourwa", 
                        "Yagoua", "Mokolo", "Pouss", "Pitoa", 
                        "Moussoro", "Logone"
                    ],
                    "Ngong": [
                        "Ngong I", "Ngong II", "Ngong III", "Ngong IV", 
                        "Ngong V", "Ngong VI", "Ngong VII", 
                        "Ngong VIII", "Ngong IX", "Ngong X"
                    ],
                    "Bogo": [
                        "Bogo I", "Bogo II", "Bogo III", "Bogo IV", 
                        "Bogo V", "Bogo VI", "Bogo VII", 
                        "Bogo VIII", "Bogo IX", "Bogo X"
                    ],
                    "Maroua": [
                        "Maroua I", "Maroua II", "Maroua III", "Maroua IV", 
                        "Maroua V", "Maroua VI", "Maroua VII", 
                        "Maroua VIII", "Maroua IX", "Maroua X"
                    ],
                    "Mokolo": [
                        "Mokolo I", "Mokolo II", "Mokolo III", "Mokolo IV", 
                        "Mokolo V", "Mokolo VI", "Mokolo VII", 
                        "Mokolo VIII", "Mokolo IX", "Mokolo X"
                    ],
                    "Yagoua": [
                        "Yagoua I", "Yagoua II", "Yagoua III", "Yagoua IV", 
                        "Yagoua V", "Yagoua VI", "Yagoua VII", 
                        "Yagoua VIII", "Yagoua IX", "Yagoua X"
                    ],
                    "Logone": [
                        "Logone I", "Logone II", "Logone III", "Logone IV", 
                        "Logone V", "Logone VI", "Logone VII", 
                        "Logone VIII", "Logone IX", "Logone X"
                    ]
                }
            }
        }

        # Loop through each region and its towns and quarters
        for region_name, region_info in data.items():
            region, created = Region.objects.get_or_create(name=region_name)
            for town_name, quarters in region_info["towns"].items():
                town, created = Town.objects.get_or_create(name=town_name, region=region)
                for quarter_name in quarters:
                    Quarter.objects.get_or_create(name=quarter_name, town=town)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with initial data.'))
