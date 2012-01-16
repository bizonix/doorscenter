# coding=utf8
import random

def GetRandomLocation():
    '''Случайным образом выбираем город/штат/страну из списка'''
    return random.choice(citiesList).strip()

citiesList = '''United States
Great Britain
Canada
Switzerland
France
Italy
Belgium
Germany
Spain
Netherlands
Australia
Singapore
New Zealand
Norway
Sweden
Mexico
Ireland
Japan
Hong Kong
Alabama
Alaska
American Samoa
Arizona
Arkansas
California
Colorado
Connecticut
Delaware
District of Columbia
Florida
Georgia
Guam
Hawaii
Idaho
Illinois
Indiana
Iowa
Kansas
Kentucky
Louisiana
Maine
Maryland
Massachusetts
Michigan
Minnesota
Mississippi
Missouri
Montana
Nebraska
Nevada
New Hampshire
New Jersey
New Mexico
New York
North Carolina
North Dakota
Ohio
Oklahoma
Oregon
Pennsylvania
Puerto Rico
Rhode Island
South Carolina
South Dakota
Tennessee
Texas
Utah
Vermont
Virginia
Virgin Islands
Washington
West Virginia
Wisconsin
Wyoming
New York
Los Angeles
Chicago
Houston
Philadelphia
Phoenix
San Antonio
San Diego
Dallas
San Jose
Jacksonville
Indianapolis
San Francisco
Austin
Columbus
Fort Worth
Charlotte
Detroit
El Paso
Memphis
Baltimore
Boston
Seattle
Washington
Nashville
Denver
Louisville
Milwaukee
Portland
Las Vegas
Oklahoma City
Albuquerque
Tucson
Fresno
Sacramento
Long Beach
Kansas City
Mesa
Virginia Beach
Atlanta
Colorado Springs
Omaha
Raleigh
Miami
Cleveland
Tulsa
Oakland
Minneapolis
Wichita
Arlington
Bakersfield
New Orleans
Honolulu
Anaheim
Tampa
Aurora
Santa Ana
Saint Louis
Pittsburgh
Corpus Christi
Riverside
Cincinnati
Lexington
Anchorage
Stockton
Toledo
Saint Paul
Newark
Greensboro
Buffalo
Plano
Lincoln
Henderson
Fort Wayne
Jersey City
Saint Petersburg
Chula Vista
Norfolk
Orlando
Chandler
Laredo
Madison
Winston-Salem
Lubbock
Baton Rouge
Durham
Garland
Glendale
Reno
Hialeah
Chesapeake
Scottsdale
North Las Vegas
Irving
Fremont
Irvine
Birmingham
Rochester
San Bernardino
Spokane
Gilbert
Arlington
Montgomery
Boise
Richmond
Des Moines
Modesto
Fayetteville
Shreveport
Akron
Tacoma
Aurora
Oxnard
Fontana
Yonkers
Augusta
Mobile
Little Rock
Moreno Valley
Glendale
Amarillo
Huntington Beach
Columbus
Grand Rapids
Salt Lake City
Tallahassee
Worcester
Newport News
Huntsville
Knoxville
Providence
Santa Clarita
Grand Prairie
Brownsville
Jackson
Overland Park
Garden Grove
Santa Rosa
Chattanooga
Oceanside
Fort Lauderdale
Rancho Cucamonga
Port Saint Lucie
Ontario
Vancouver
Tempe
Springfield
Lancaster
Eugene
Pembroke Pines
Salem
Cape Coral
Peoria
Sioux Falls
Springfield
Elk Grove
Rockford
Palmdale
Corona
Salinas
Pomona
Pasadena
Joliet
Paterson
Kansas City
Torrance
Syracuse
Bridgeport
Hayward
Fort Collins
Escondido
Lakewood
Naperville
Dayton
Hollywood
Sunnyvale
Alexandria
Mesquite
Hampton
Pasadena
Orange
Savannah
Cary
Fullerton
Warren
Clarksville
McKinney
McAllen
New Haven
Sterling Heights
West Valley City
Columbia
Killeen
Topeka
Thousand Oaks
Cedar Rapids
Olathe
Elizabeth
Waco
Hartford
Visalia
Gainesville
Simi Valley
Stamford
Bellevue
Concord
Miramar
Coral Springs
Lafayette
Charleston
Carrollton
Roseville
Thornton
Beaumont
Allentown
Surprise
Evansville
Abilene
Frisco
Independence
Santa Clara
Springfield
Vallejo
Victorville
Athens
Peoria
Lansing
Ann Arbor
El Monte
Denton
Berkeley
Provo
Downey
Midland
Norman
Waterbury
Costa Mesa
Inglewood
Manchester
Murfreesboro
Columbia
Elgin
Clearwater
Miami Gardens
Rochester
Pueblo
Lowell
Wilmington
Arvada
San Buenaventura
Ventura
Westminster
West Covina
Gresham
Fargo
Norwalk
Carlsbad
Fairfield
Cambridge
Wichita Falls
High Point
Billings
Green Bay
West Jordan
Richmond
Murrieta
Burbank
Palm Bay
Everett
Flint
Antioch
Erie
South Bend
Daly City
Centennial
Temecula
London
Birmingham
Glasgow
Liverpool
Leeds
Sheffield
Edinburgh
Bristol
Manchester
Leicester
Coventry
Kingston upon Hull
Bradford
Cardiff
Belfast
Stoke-on-Trent
Wolverhampton
Nottingham
Plymouth
Southampton
Reading
Derby
Dudley
Newcastle upon Tyne
Northampton
Portsmouth
Luton
Preston
Aberdeen
Milton Keynes
Sunderland
Norwich
Walsall
Swansea
Bournemouth
Southend-on-Sea
Swindon
Dundee
Huddersfield
Poole
Oxford
Middlesbrough
Blackpool
Bolton
Ipswich
Telford
York
West Bromwich
Peterborough
Stockport
Brighton
Slough
Gloucester
Watford
Rotherham
Newport
Cambridge
Exeter
Eastbourne
Sutton Coldfield
Blackburn
Colchester
Oldham
St Helens
Woking
Crawley
Chelmsford
Basildon
Cheltenham
Gillingham
Worthing
Rochdale
Solihull
Worcester
Derry
Southport
Basingstoke
Bath
Maidstone
Harlow
Grimsby
Darlington
Hartlepool
Lincoln
Hastings
Birkenhead
Halifax
Hemel Hempstead
South Shields
Bedford
St Albans
Stevenage
Wigan
Warrington
Chester
Stockton-on-Tees
Gateshead
Weston-super-Mare
High Wycombe
Wakefield
Redditch
Newcastle-under-Lyme
Paisley
East Kilbride
Chatham
Burnley
Salford
Scunthorpe
Hove
Carlisle
Tamworth
Barnsley
Harrogate
Lisburn
Bracknell
Nuneaton
Chesterfield
Mansfield
Guildford
Gosport
Aylesbury
Lowestoft
Doncaster
Crewe
Shrewsbury
Ellesmere Port
Cannock
Grays
Stafford
Waterlooville
Torquay
Kingswood
Bognor Regis
Newtownabbey
Rugby
Royal Leamington Spa
Bury
Royal Tunbridge Wells
Runcorn
Rhondda
Bootle
Ashford
Maidenhead
Wallasey
Margate
Bangor
Taunton
Aldershot
Great Yarmouth
Farnborough
Bebington
Dartford
Hereford
Fareham
Littlehampton
Widnes
Stourbridge
Kidderminster
Cheshunt
Halesowen
Loughborough
Sale
Dewsbury
Morley
Washington
Gravesend
Eastleigh
Crosby
Clacton-on-Sea
Kettering
Livingston
Dunstable
Macclesfield
Barry
Staines
La Tuque
Senneterre
Rouyn-Noranda
Val-d'Or
Greater Sudbury
Kawartha Lakes
Timmins
Ottawa
Queens
Gillam
Sept-Iles
Norfolk County
Leaf Rapids
Haldimand County
Snow Lake
Saguenay
Gaspe
Hamilton
Port-Cartier
Prince Edward County
Lynn Lake
County of Brant
Shawinigan
Calgary
Te'miscaming
Huntsville
Chibougamau
Elliot Lake
Caledon
Edmonton
Saint-Raymond
Laurentian Hills
Toronto
Bracebridge
Iroquois Falls
Mont-Laurier
De'gelis
Belleterre
Baie-Saint-Paul
Cochrane
South Bruce Peninsula
Lakeshore
Kearney
Blind River
Gravenhurst
Mississippi Mills
Quinte West
Mirabel
Fermont
Winnipeg
Greater Napanee
La Malbaie
Riviere-Rouge
Que'bec City
Kingston
Le'vis
St John's
Be'cancour
Perce
Amos
London
Chandler
Whitehorse
Gracefield
Baie Verte
Milton
Montre'al
Saint-Fe'licien
Abbotsford
Sherbrooke
Gatineau
Pohe'ne'gamook
Baie-Comeau
Thunder Bay
Plympton-Wyoming
Surrey
Prince George
Saint John
North Bay
Minto
Kamloops
Erin
Clarence-Rockland
Cookshire-Eaton
Dolbeau-Mistassini
Trois-Rivieres
Mississauga
Georgina
The Blue Mountains
Innisfil
Essex
Mono
Halton Hills
New Tecumseth
Vaughan
Brampton
Zurich
Geneva
Basel
Lausanne
Bern
Winterthur
St Gallen
Lucerne
Lugano
Biel
Bienne
Thun
Koniz
La Chaux-de-Fonds
Fribourg
Schaffhausen
Chur
Neuchatel
Vernier
Uster
Sion
Paris
Marseille
Lyon
Toulouse
Nice
Nantes
Strasbourg
Montpellier
Bordeaux
Lille
Rennes
Le Havre
Reims
Saint-E'tienne
Toulon
Grenoble
Angers
Dijon
Brest
Le Mans
Clermont-Ferrand
Amiens
Aix-en-Provence
Limoges
Nimes
Tours
Saint-Denis
Villeurbanne
Metz
Besancon
Caen
Orle'ans
Mulhouse
Rouen
Boulogne-Billancourt
Perpignan
Nancy
Roubaix
Fort-de-France
Argenteuil
Tourcoing
Montreuil
Saint-Paul
Avignon
Saint-Denis
Versailles
Nanterre
Poitiers
Cre'teil
Aulnay-sous-Bois
Vitry-sur-Seine
Calais
Colombes
La Rochelle
Asnieres-sur-Seine
Champigny-sur-Marne
Rueil-Malmaison
Saint-Maur-des-Fosse's
Bourges
Antibes
Dunkirk
Courbevoie
Be'ziers
Saint-Pierre
Cannes
Saint-Nazaire
Colmar
Villeneuve d'Ascq
Valence
Quimper
Aubervilliers
Les Abymes
Drancy
Me'rignac
Troyes
Le Tampon
La Seyne-sur-Mer
Antony
Neuilly-sur-Seine
Lorient
Saint-Quentin
Noisy-le-Grand
Sarcelles
Niort
Pessac
Ve'nissieux
Chambe'ry
Charleville-Me'zieres
Beauvais
Cergy
Levallois-Perret
Cholet
Ajaccio
Issy-les-Moulineaux
Montauban
Vannes
Hyeres
E'vreux
Maisons-Alfort
Ivry-sur-Seine
Laval
Fontenay-sous-Bois
Saint-Malo
Cayenne
Arles
Belfort
Annecy
Sartrouville
Clichy
Chalon-sur-Saone
Pantin
Chateauroux
E'vry
Meaux
La Roche-sur-Yon
Blois
Brive-la-Gaillarde
Clamart
Villejuif
Chalons-en-Champagne
Sevran
Le Blanc-Mesnil
Bondy
Fre'jus
Narbonne
E'pinay-sur-Seine
Tarbes
Albi
Saint-Brieuc
Chelles
Boulogne-sur-Mer
Bobigny
Carcassonne
Cagnes-sur-Mer
Grasse
Saint-Herblain
Mantes-la-Jolie
Meudon
Vincennes
Saint-Louis
Castres
Martigues
Saint-Andre
Angouleme
Douai
Wattrelos
Aubagne
Gennevilliers
Cherbourg-Octeville
Le Cannet
Montlucon
Valenciennes
Compiegne
Caluire-et-Cuire
Saint-Priest
Nevers
Thionville
Puteaux
Bourg-en-Bresse
Arras
Chartres
Bayonne
Garges-les-Gonesse
Saint-Ouen
Suresnes
Sete
Corbeil-Essonnes
Ales
Vaulx-en-Velin
Rosny-sous-Bois
Istres
Roanne
Saint-Germain-en-Laye
Le Port
Bastia
Auxerre
Montrouge
Massy
Saint-Chamond
Bron
Noisy-le-Sec
Livry-Gargan
Bagneux
Talence
Marcq-en-Baroeul
Salon-de-Provence
Vitrolles
Gagny
Joue'-les-Tours
Savigny-sur-Orge
Alfortville
Lens
Poissy
E'pinal
Saint-Martin-d'Heres
Melun
Reze
Le Lamentin
La Courneuve
Anglet
Dieppe
Macon
Choisy-le-Roi
Chatellerault
Marignane
Tremblay-en-France
Villepinte
Cambrai
Maubeuge
Franconville
Lie'vin
Pontault-Combault
Stains
Draguignan
E'chirolles
Neuilly-sur-Marne
Six-Fours-les-Plages
Romans-sur-Isere
Bagnolet
Haguenau
Vandoeuvre-les-Nancy
Dreux
Les Mureaux
La Ciotat
Saint-Benoit
Monte'limar
Plaisir
Saint-Dizier
Schiltigheim
Creil
Saint-Raphael
Chatenay-Malabry
Aurillac
Saint-Joseph
Viry-Chatillon
Pe'rigueux
Agen
Le Perreux-sur-Marne
Biarritz
Vienne
Saumur
Vierzon
L'Hay-les-Roses
Houilles
Sotteville-les-Rouen
Mont-de-Marsan
Soissons
Athis-Mons
Malakoff
Saint-Martin
Palaiseau
Alencon
Thonon-les-Bains
Menton
Trappes
Chatillon
Chatou
Colomiers
Le Chesnay
Rillieux-la-Pape
Clichy-sous-Bois
Thiais
Nogent-sur-Marne
Saint-Cloud
Lambersart
Draveil
Meyzieu
Orange
Be'thune
Montbe'liard
Villenave-d'Ornon
Ermont
Pontoise
Yerres
Goussainville
Annemasse
Saint-Laurent-du-Var
Villemomble
Sens
Le Grand-Quevilly
E'lancourt
Villiers-sur-Marne
Charenton-le-Pont
Sainte-Marie
Vichy
Le Creusot
Laon
Bezons
Villiers-le-Bel
Carpentras
Bergerac
Chaumont
Taverny
E'pernay
Pierrefitte-sur-Seine
Rochefort
Les Ulis
Vallauris
Aix-les-Bains
Vigneux-sur-Seine
Saintes
Vanves
Le Gosier
Sannois
La Garde
Saint-Leu
Armentieres
Fresnes
Oullins
He'nin-Beaumont
Guyancourt
Dole
Cachan
Sucy-en-Brie
Rambouillet
Gonesse
Abbeville
Cavaillon
Champs-sur-Marne
Grigny
Ris-Orangis
De'cines-Charpieu
Oyonnax
Coudekerque-Branche
Montfermeil
La Garenne-Colombes
Vernon
Bruay-la-Buissiere
Bois-Colombes
Romainville
Le Kremlin-Bicetre
Rodez
Brunoy
Orvault
Fontenay-aux-Roses
Montigny-les-Metz
Baie-Mahault
Saint-Pol-sur-Mer
Fontaine
Grande-Synthe
Sarreguemines
Lisieux
Herblay
Mons-en-Baroeul
La Teste-de-Buch
Bourgoin-Jallieu
Eaubonne
Forbach
Villeneuve-sur-Lot
Tournefeuille
Saint-Die'-des-Vosges
Sevres
Miramas
Begles
Le Bouscat
La Madeleine
Lunel
Villeneuve-la-Garenne
Savigny-le-Temple
Le Petit-Quevilly
Gradignan
Beaune
Montgeron
La Possession
Lanester
Moulins
Maisons-Laffitte
E'tampes
Auch
Fougeres
Libourne
La Valette-du-Var
Bre'tigny-sur-Orge
Le Plessis-Robinson
Torcy
La Celle-Saint-Cloud
Hazebrouck
Gif-sur-Yvette
Lormont
Millau
Villeparisis
Cenon
Mont-Saint-Aignan
Le Robert
Le Me'e-sur-Seine
Sainte-Foy-les-Lyon
Fe'camp
Combs-la-Ville
Pointe-a-Pitre
Loos
Schoelcher
Le Moule
Muret
Ozoir-la-Ferriere
Fleury-les-Aubrais
Dammarie-les-Lys
Croix
Montceau-les-Mines
Montmorency
Blagnac
Sedan
Petit-Bourg
Le Puy-en-Velay
Orly
Sainte-Anne
Saint-Michel-sur-Orge
Denain
Ve'lizy-Villacoublay
Vertou
Les Lilas
Lune'ville
Deuil-la-Barre
Sainte-Marie
Saint-Lo
Cahors
Rome
Milan
Naples
Turin
Palermo
Genoa
Bologna
Florence
Bari
Catania
Venice
Verona
Messina
Padua
Trieste
Brescia
Taranto
Prato
Parma
Reggio Calabria
Modena
Reggio Emilia
Perugia
Livorno
Ravenna
Cagliari
Foggia
Rimini
Salerno
Ferrara
Sassari
Syracuse
Pescara
Monza
Latina
Bergamo
Forli
Giugliano in Campania
Trento
Vicenza
Terni
Novara
Bolzano
Piacenza
Ancona
Arezzo
Andria
Udine
Cesena
Lecce
La Spezia
Pesaro
Alessandria
Barletta
Catanzaro
Pistoia
Brindisi
Pisa
Torre del Greco
Como
Lucca
Guidonia Montecelio
Pozzuoli
Treviso
Marsala
Grosseto
Busto Arsizio
Varese
Sesto San Giovanni
Casoria
Caserta
Gela
Asti
Cinisello Balsamo
Ragusa
LAquila
Cremona
Quartu Sant'Elena
Lamezia Terme
Pavia
Fiumicino
Massa
Trapani
Aprilia
Cosenza
Altamura
Imola
Carpi
Potenza
Carrara
Viareggio
Fano
Afragola
Vigevano
Viterbo
Vittoria
Savona
Benevento
Crotone
Pomezia
Matera
Caltanissetta
Molfetta
Marano di Napoli
Agrigento
Legnano
Cerignola
Moncalieri
Foligno
Faenza
Manfredonia
Sanremo
Tivoli
Bitonto
Avellino
Bagheria
Acerra
Olbia
Cuneo
Anzio
San Severo
Modica
Teramo
Bisceglie
Ercolano
Siena
Chieti
Portici
Trani
Velletri
Cava de' Tirreni
Acireale
Rovigo
Civitavecchia
Gallarate
Pordenone
Aversa
Montesilvano
Mazara del Vallo
Ascoli Piceno
Battipaglia
Campobasso
Scafati
Casalnuovo di Napoli
Chioggia
Scandicci
Collegno
Antwerp
Ghent
Charleroi
Liege
Brussels
Bruges
Schaerbeek
Namur
Anderlecht
Leuven
Mons
Sint-Jans-Molenbeek
Mechelen
Ixelles
Aalst
La Louviere
Uccle
Kortrijk
Hasselt
Sint-Niklaas
Ostend
Tournai
Genk
Seraing
Roeselare
Verviers
Mouscron
Woluwe-Saint-Lambert
Forest
Beveren
Saint-Gilles
Jette
Dendermonde
Etterbeek
Beringen
Turnhout
Dilbeek
Heist-op-den-Berg
Woluwe-Saint-Pierre
Sint-Truiden
Lokeren
Vilvoorde
Herstal
Braine-l'Alleud
Brasschaat
Maasmechelen
Ninove
Waregem
Chatelet
Geel
Halle
Ypres
Grimbergen
Knokke-Heist
Evere
Lier
Schoten
Mol
Wavre
Binche
Menen
Evergem
Lommel
Tienen
Geraardsbergen
Heusden-Zolder
Sint-Pieters-Leeuw
Wevelgem
Bilzen
Houthalen-Helchteren
Berlin
Hamburg
Munchen
Koln
Frankfurt
Essen
Dortmund
Stuttgart
Dusseldorf
Bremen
Hannover
Duisburg
Nurnberg
Leipzig
Dresden
Bochum
Wuppertal
Bielefeld
Bonn
Mannheim
Karlsruhe
Gelsenkirchen
Wiesbaden
Munster
Monchengladbach
Chemnitz
Augsburg
Braunschweig
Aachen
Krefeld
Halle
Kiel
Magdeburg
Oberhausen
Lubeck
Freiburg
Hagen
Erfurt
Kassel
Rostock
Mainz
Hamm
Saarbrucken
Herne
Mulheim
Solingen
Osnabruck
Ludwigshafen
Leverkusen
Oldenburg
Neuss
Paderborn
Heidelberg
Darmstadt
Potsdam
Wurzburg
Gottingen
Regensburg
Recklinghausen
Bottrop
Wolfsburg
Heilbronn
Ingolstadt
Remscheid
Pforzheim
Bremerhaven
Offenbach
Furth
Reutlingen
Salzgitter
Siegen
Gera
Koblenz
Moers
Bergisch Gladbach
Cottbus
Hildesheim
Witten
Zwickau
Erlangen
Iserlohn
Trier
Kaiserslautern
Jena
Schwerin
Gutersloh
Marl
Lunen
Esslingen
Velbert
Ratingen
Duren
Ludwigsburg
Wilhelmshaven
Hanau
Minden
Flensburg
Dessau
Madrid
Barcelona
Valencia
Sevilla
Zaragoza
Malaga
Murcia
Palma de Mallorca
Bilbao
Valladolid
Cordoba
Alicante
Vigo
Gijon
A Coruna
Granada
Vitoria
Oviedo
Badalona
Elche
Mostoles
Madrid
Barcelona
Valencia
Alicante
Sevilla
Ma'laga
Murcia
Ca'diz
Biscay
La Coruna
Asturias
Las Palmas
Pontevedra
Balearic Islands
Zaragoza
Granada
Co'rdoba
Guipu'zcoa
Badajoz
Jae'n
Tarragona
Girona
Navarra
Toledo
Almeri'a
Cantabria
Castello'n
Valladolid
Leo'n
Ciudad Real
Huelva
Ca'ceres
Albacete
Lleida
Lugo
Burgos
Salamanca
Ourense
A'lava
La Rioja
Huesca
Cuenca
Zamora
Guadalajara
Palencia
A'vila
Segovia
Teruel
Soria
Ceuta
Melilla
Amsterdam
Rotterdam
The Hague
Utrecht
Eindhoven
Tilburg
Almere
Groningen
Breda
Nijmegen
Apeldoorn
Enschede
Haarlem
Arnhem
Amersfoort
Dordrecht
Zoetermeer
Zwolle
Leiden
Maastricht
Hertogenbosch
Venlo
Sydney
Melbourne
Brisbane
Perth
Adelaide
Gold Coast-Tweed
Newcastle
Canberra-Queanbeyan
Canberra
Wollongong
Sunshine Coast
Greater Hobart
Geelong
Townsville
Cairns
Toowoomba
Darwin
Launceston
Albury-Wodonga
Ballarat
Bendigo
Mandurah
Mackay
Burnie-Devonport
Latrobe Valley
Rockhampton
Bundaberg
Bunbury
Hervey Bay
Wagga Wagga
Coffs Harbour
Gladstone
Mildura
Shepparton
Tamworth
Port Macquarie
Orange
Dubbo
Geraldton
Nowra-Bomaderry
Bathurst
Warrnambool
Lismore
Kalgoorlie-Boulder
Auckland
Wellington
Christchurch
Hamilton
Napier-Hastings
Tauranga
Dunedin
Palmerston North
Nelson
Rotorua
New Plymouth
Whangarei
Invercargill
Whanganui
Wanganui
Gisborne
Oslo
Bergen
Trondheim
Stavanger
Baerum
Fredrikstad
Kristiansand
Drammen
Asker
Tromso
Stockholm
Goteborg
Gothenburg
Malmo
Uppsala
Vasteras
Orebro
Linkoping
Helsingborg
Jonkoping
Norrkoping
Lund
Umea
Gavle
Boras
Eskilstuna
Sodertalje
Karlstad
Taby
Vaxjo
Halmstad
Sundsvall
Lulea
Trollhattan
Ostersund
Borlange
Tumba
Upplands Vasby
Falun
Kalmar
Kristianstad
Karlskrona
Skovde
Skelleftea
Lidingo
Uddevalla
Landskrona
Nykoping
Motala
Vallentuna
Ornskoldsvik
Trelleborg
Akersberga
Varberg
Karlskoga
Lidkoping
Alingsas
Marsta
Angelholm
Sandviken
Pitea
Kungalv
Visby
Katrineholm
Vanersborg
Vastervik
Enkoping
Falkenberg
Mexico City
Ecatepec de Morelos
Tijuana
Puebla
Guadalajara
Leon
Ciudad Juarez
Zapopan
Monterrey
Nezahualco'yotl
Mexicali
Culiaca'n
Naucalpan de Jua'rez
Me'rida
Toluca
Chihuahua
Quere'taro
Aguascalientes
Acapulco
Hermosillo
San Luis Potosi
Morelia
Saltillo
Guadalupe
Tlalnepantla de Baz
Cancun
Villahermosa
Torreo'n
Chimalhuaca'n
Reynosa
Tlaquepaque
Durango
Tuxtla Gutie'rrez
Veracruz
Irapuato
Tultitla'n
Apodaca
Atizapa'n de Zaragoza
Matamoros
Tonala
Celaya
Ixtapaluca
Ensenada
Xalapa
Mazatla'n
Tlajomulco de Zu'niga
Los Mochis
Ciudad Obrego'n
Nuevo Laredo
Tepic
Nicola's Romero
Cuernavaca
Teca'mac
General Escobedo
Go'mez Palacio
Ciudad Victoria
Tapachula
Uruapan
Chalco
Coatzacoalcos
Tampico
Guasave
Tehuaca'n
Santa Catarina
Pachuca
Oaxaca
Salamanca
Campeche
Juarez
Puerto Vallarta
Los Reyes Acaquilpan
La Paz
Cardenas
Chetumal
Huixquilucan
San Juan del Rio
Chilpancingo
Los Cabos
Texcoco
Ciudad del Carmen
Nogales
Monclova
Metepec
Fresnillo
Altamira
Ocosingo
Ciudad Madero
Jiutepec
Co'rdoba
Poza Rica
Comalcalco
Chicoloapan
Zamora
Huimanguillo
San Luis Rio Colorado
La'zaro Ca'rdenas
Cuautla
Silao
Guanajuato
Ciudad Valles
Zinacantepec
Manzanillo
San Miguel de Allende
Manzanillo
Minatitla'n
Macuspana
Zinacantepec
Navojoa
Boca del Ri'o
Zumpango
Guadalupe
Papantla
Lerdo
Lagos de Moreno
Tuxpan
Allende
Cuautitla'n Izcalli
Almoloya de Jua'rez
Zacatecas
San Marti'n Texmelucan
Cuauhte'moc
Zita'cuaro
Tepatitla'n
Ixtlahuaca de Rayo'n
Guaymas
Cuautitla'n
Acuna
Colima
Dolores Hidalgo
Pe'njamo
Tulancingo
Delicias
El Salto
Navolato
Comita'n
Huejutla de Reyes
Corregidora
Iguala
Valle de Santiago
Tultepec
San Pedro Cholula
Chilapa de A'lvarez
Atlixco
Orizaba
Villa de A'lvarez
Cunduaca'n
Apatzinga'n
Lerma
Cosoleacaque
Ciudad Hidalgo
Chilo'n
El Mante
Ri'o Bravo
Palenque
Jose' Azueta
Tecate
Temixco
Parral
Matamoros
Tantoyuca
Las Margaritas
Temapache
San Luis de la Paz
Ciudad Guzma'n
Marti'nez de la Torre
Dublin
Cork
Limerick
Galway
Waterford
Drogheda
Dundalk
Swords
Bray
Navan
Ennis
Tralee
Kilkenny
Carlow
Naas
Sligo
Newbridge
Mullingar
Wexford
Letterkenny
Athlone
Celbridge
Clonmel
Balbriggan
Malahide
Leixlip
Portlaoise
Killarney
Greystones
Tullamore
Carrigaline
Castlebar
Arklow
Cobh
Maynooth
Ballina
Mallow
Wicklow
Midleton
Tramore
Enniscorthy
Skerries
Shannon
Portmarnock
Longford
Ashbourne
Dungarvan
Rush
Athy
Cavan
Nenagh
New Ross
Thurles
Kildare
Ratoath
Gorey
Tuam
Trim
Youghal
Monaghan
Ballinasloe
Portarlington
Buncrana
Carrick-on-Suir
Edenderry
Fermoy
Bandon
Dunboyne
Donabate
Westport
Kells
Lusk
Passage West
Newcastle West
Birr
Tipperary
Roscommon
Clane
Roscrea
Ardee
Loughrea
Carrickmacross
Listowel
Ballybofey-Stranorlar
Clonakilty
Kilcock
Kinsale
Mountmellick
Blessington
Sallins
Kinsealy-Drinan
Macroom
Oranmore
Dunshaughlin
Cahir
Mitchelstown
Bantry
Kilcoole
Duleek
Tokyo
Yokohama
Osaka
Nagoya
Sapporo
Ko-be
Kyoto
Fukuoka
Kawasaki
Saitama
Hiroshima
Sendai
Kitakyu-shu
Chiba
Sakai
Niigata
Hamamatsu
Kumamoto
Sagamihara
Shizuoka
Okayama
Funabashi
Kagoshima
Hachio-ji
Himeji
Matsuyama
Utsunomiya
Higashio-saka
Kawaguchi
Matsudo
Nishinomiya
Kurashiki
Ichikawa
O-ita
Kanazawa
Fukuyama
Amagasaki
Nagasaki
Machida
Toyama
Toyota
Takamatsu
Yokosuka
Gifu
Fujisawa
Hirakata
Kashiwa
Miyazaki
Toyonaka
Nagano
Toyohashi
Ichinomiya
Okazaki
Takasaki
Wakayama
Nara
Takatsuki
Suita
Asahikawa
Ko-chi
Kawagoe
Iwaki
Tokorozawa
Maebashi
Ko-riyama
O-tsu
Koshigaya
Akita
Naha
Yokkaichi
Kasugai
Kurume
Aomori
Morioka
Fukushima
Akashi
Nagaoka
Shimonoseki
Ichihara
Hakodate
Ibaraki
Mito
Kakogawa
Fukui
Tokushima
Sasebo
Hiratsuka
Fuchu
Yamagata
Fuji
So-ka
Matsumoto
Kure
Neyagawa
Saga
Hachinohe
Kasukabe
Chigasaki
Yamato
Takarazuka
Atsugi
Ageo
Cho-fu
O-ta
Tsukuba
Isesaki
Jo-etsu
Kumagaya
Numazu'''.split('\n')

if __name__ == '__main__':
    print(GetRandomLocation())
