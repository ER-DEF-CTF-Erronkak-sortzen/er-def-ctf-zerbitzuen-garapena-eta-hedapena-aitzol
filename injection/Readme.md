- Zerbitzuak

    Erronka honetan bi zerbitzu erabiltzen dira, alde batetik web zerbitzari bat eta beste alde batetik web aplikazio bat.

    Web zerbitzaria nginx-ekin konfiguratuta dago eta eskaera guztiak reverse proxy bidez bigarren zerbitzura bideratzen ditu. Bigarren zerbitzu hau flask-en (python web framework bat) garatutako web aplikazio bat da.

    Web zerbitzariak ez dauka batere inplementazio zailtasunik, berau garatzeko konfigurazio fitxategi bat zehaztu behar da bakarrik.

    Web aplikazioaren garapenerako oinarri gisa https://github.com/realsidg/sqlInjection repositorioan zehaztutako flask aplikazio erasogarria erabili da, eta gure CTF inguruneko falg-ak kudeatzeko beharrezko elementuak gehitu zaizkio. Web aplikazioa inplementatzeko python:3.13-alpine irudia erabili da eta beharrezkoak dituen dependentziak ezarri ondoren web aplikazioa martxan jartzen de supervisor erabiliz.Supervisor konfigurazioak kontenedorearen barruko web aplikazioaren rekarga egitea baimentzen du. Hau egitea behjarrezkoa da eraso bektorea ezabatzeko beharrezkoa delako iturburua aldatu eta web aplikazioa berrabiaraztea.

- Checkerra

    Aplikazioaren egoera txekeatzeko sistemak eskaintzen duen BaseChecker erabiltzen da. Klase honek beharrezko diren metodoak gainidaztera behartzen gaiut eta gero erronkako kudeaketako loop nagusian klase hori inplementatzen duten checker desberdinen metodo zehatzetara deituko da.

    Metodo hauetako bakoitzean egiten da erronkaren egoera txekeatzeko beharrezko den guztia. Bi metodo nagusi daude check_flag, check_service eta place_flag.

-- check_flag

    Zerbitzuetan flag-ak ondo ezarrita dauden begiratzen du. Erronka honen kasuan webapp zerbitzuaren /tmp/flag.txt fitxategian ezartzen da flag-a hortaz, begiratzen dena da ea fitxategi horren barruan ondo definituta dagoen flag-a.

-- check_service

    Erronka OK markatzeko web zerbitzua eta flask zerbitzua martxan egon behar dira. Check hau dagozkion portuetan request bat eginda aztertzen da

-- place_flag

    Tick bakoitzean sistematik flag-a eskuratu eta dagokion tokira eramaten du. Web aplikazioan /tmp/flag.txt fitxategira kopiatuko du, paramiko python ssh bezeroa erabiliz

- Exploita

    Exploitak erasoa simulatzen du, horretarako azpian web zerbitzuak egiten duen API eskaera erabiltzen du flag-a eskuragarri dagoen ikusteko. API-ak JSON formatuan erantzuten du, hortaz erraxa da aztertzea ea request egokia eginda autentikazioa lortuko genukeen edo ez.