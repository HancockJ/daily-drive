T = lambda n, *a: (n, list(a))

# College football questions, 1-2 per day from Nov 8 on (the NFL questions they displace roll onto later days).
# Keys are question ids. LEVEL: E = easy, M = medium, H = hard. Q5 = wildcard-style lists. GROUPS = keep 4+ days apart.

PAGE = {"Tim Brown": "Tim Brown (American football)", "Jason White": "Jason White (American football)", "Larry Smith": "Larry Smith (American football coach)",
        "Mike Shula": "Mike Shula", "Bill Curry": "Bill Curry", "Joe Kines": "Joe Kines", "Bryan McClendon": "Bryan McClendon",
        "Larry Scott": "Larry Scott (American football)", "Jeff Stoutland": "Jeff Stoutland", "Mark Ingram II": "Mark Ingram II",
        "Kent Baer": "Kent Baer", "Jim Mackenzie": "Jim Mackenzie (American football)", "Gary Gibbs": "Gary Gibbs", "John Blake": "John Blake (American football)",
        "Chris Olave": "Chris Olave", "Garrett Wilson": "Garrett Wilson (American football)", "Evan Neal": "Evan Neal", "Jameson Williams": "Jameson Williams",
        "Donovan Jackson": "Donovan Jackson", "Josh Simmons": "Josh Simmons (American football)", "Tyleik Williams": "Tyleik Williams",
        "Damon Arnette": "Damon Arnette", "Dallas Turner": "Dallas Turner", "John Parker Wilson": "John Parker Wilson", "Greg McElroy": "Greg McElroy",
        "Blake Sims": "Blake Sims", "Jake Coker": "Jake Coker", "Cardale Jones": "Cardale Jones", "Chris Leak": "Chris Leak", "Matt Flynn": "Matt Flynn (American football)",
        "Will Howard": "Will Howard (American football)", "Stetson Bennett": "Stetson Bennett", "Vince Young": "Vince Young", "Charles White": "Charles White (American football)",
        "Mike Garrett": "Mike Garrett", "Billy Sims": "Billy Sims", "Steve Owens": "Steve Owens (American football)", "Billy Vessels": "Billy Vessels",
        "Troy Smith": "Troy Smith", "Leon Hart": "Leon Hart", "Larry Coker": "Larry Coker", "Les Miles": "Les Miles", "Gene Chizik": "Gene Chizik",
        "Butch Davis": "Butch Davis", "Al Golden": "Al Golden", "Mark Richt": "Mark Richt", "Manny Diaz": "Manny Diaz (American football)",
        "Randy Shannon": "Randy Shannon", "Odell Haggins": "Odell Haggins", "Willie Taggart": "Willie Taggart", "Mike Norvell": "Mike Norvell",
        "Ray Goff": "Ray Goff", "Jim Donnan": "Jim Donnan", "Ray Perkins": "Ray Perkins", "Mike DuBose": "Mike DuBose",
        "Dennis Franchione": "Dennis Franchione", "Gene Stallings": "Gene Stallings", "Fred Akers": "Fred Akers", "David McWilliams": "David McWilliams",
        "John Mackovic": "John Mackovic", "Charlie Strong": "Charlie Strong", "Tom Herman": "Tom Herman", "Ted Tollner": "Ted Tollner",
        "Paul Hackett": "Paul Hackett (American football)", "Donte Williams": "Donte Williams", "Clay Helton": "Clay Helton", "Gerry Faust": "Gerry Faust",
        "Bob Davie": "Bob Davie", "Tyrone Willingham": "Tyrone Willingham", "Charlie Weis": "Charlie Weis", "Brian Kelly": "Brian Kelly (American football coach)",
        "Marcus Freeman": "Marcus Freeman", "Dan Devine": "Dan Devine", "John Robinson": "John Robinson (American football coach)", "Earle Bruce": "Earle Bruce",
        "John Cooper": "John Cooper (American football)", "Gary Moeller": "Gary Moeller", "Rich Rodriguez": "Rich Rodriguez", "Brady Hoke": "Brady Hoke",
        "Sherrone Moore": "Sherrone Moore", "Luke Fickell": "Luke Fickell", "Ed Orgeron": "Ed Orgeron", "Jalen Milroe": "Jalen Milroe", "AJ McCarron": "AJ McCarron"}
WIKI_ONLY = set()

SPEC = {
 "titlecoach": [("Name a head coach who won a college football national title from the 1995 through 2024 seasons (AP poll, coaches' poll, BCS or CFP).", [
   T("Nick Saban"), T("Urban Meyer"), T("Dabo Swinney"), T("Kirby Smart"), T("Pete Carroll"), T("Jim Harbaugh"), T("Ryan Day"), T("Les Miles"),
   T("Bobby Bowden"), T("Steve Spurrier"), T("Mack Brown"), T("Jimbo Fisher"), T("Ed Orgeron", "Coach O"), T("Tom Osborne"), T("Jim Tressel"),
   T("Bob Stoops"), T("Gene Chizik"), T("Lloyd Carr"), T("Phillip Fulmer", "Phil Fulmer"), T("Larry Coker")])],
 "heistitle": [("Name a Heisman Trophy winner whose team won the national title that same season (1970 through 2024).", [
   T("Tony Dorsett"), T("Charlie Ward"), T("Danny Wuerffel"), T("Charles Woodson"), T("Matt Leinart"), T("Mark Ingram II", "Mark Ingram"),
   T("Cam Newton"), T("Jameis Winston"), T("Joe Burrow"), T("DeVonta Smith", "Devonta Smith")])],
 "titleqb": [("Name a quarterback who played for the winning team in a BCS or CFP national title game (2005 through 2024 seasons).", [
   T("Vince Young"), T("Chris Leak"), T("Tim Tebow"), T("Matt Flynn"), T("Greg McElroy"), T("Cam Newton"), T("AJ McCarron", "A. J. McCarron"),
   T("Jameis Winston"), T("Cardale Jones"), T("Jake Coker"), T("Deshaun Watson"), T("Jalen Hurts"), T("Tua Tagovailoa", "Tua"),
   T("Trevor Lawrence"), T("Joe Burrow"), T("Mac Jones"), T("Stetson Bennett"), T("J. J. McCarthy", "JJ McCarthy", "J.J. McCarthy"), T("Will Howard")])],
 "bamaqb": [("Name a quarterback who was Alabama's main starter for a season under Nick Saban (2007-2023).", [
   T("John Parker Wilson"), T("Greg McElroy"), T("AJ McCarron", "A. J. McCarron"), T("Blake Sims"), T("Jake Coker"), T("Jalen Hurts"),
   T("Tua Tagovailoa", "Tua"), T("Mac Jones"), T("Bryce Young"), T("Jalen Milroe")])],
 "heisouusc": [("Name a Heisman Trophy winner from Oklahoma or USC (through 2024).", [
   T("Billy Vessels"), T("Steve Owens"), T("Billy Sims"), T("Jason White"), T("Sam Bradford"), T("Baker Mayfield"), T("Kyler Murray"),
   T("Mike Garrett"), T("O. J. Simpson", "OJ Simpson", "O.J. Simpson", "OJ"), T("Charles White"), T("Marcus Allen"), T("Carson Palmer"),
   T("Matt Leinart"), T("Reggie Bush"), T("Caleb Williams")])],
 "heisbig": [("Name a Heisman Trophy winner from Ohio State, Notre Dame or Alabama (through 2024).", [
   T("Les Horvath"), T("Vic Janowicz"), T("Howard Cassady", "Hopalong Cassady"), T("Archie Griffin"), T("Eddie George"), T("Troy Smith"),
   T("Angelo Bertelli"), T("Johnny Lujack"), T("Leon Hart"), T("Johnny Lattner"), T("Paul Hornung"), T("John Huarte"), T("Tim Brown"),
   T("Mark Ingram II", "Mark Ingram"), T("Derrick Henry"), T("DeVonta Smith", "Devonta Smith"), T("Bryce Young")])],
 "osumich": [("Name an Ohio State or Michigan head football coach from 1969 through 2024.", [
   T("Woody Hayes"), T("Earle Bruce"), T("John Cooper"), T("Jim Tressel"), T("Luke Fickell"), T("Urban Meyer"), T("Ryan Day"),
   T("Bo Schembechler"), T("Gary Moeller"), T("Lloyd Carr"), T("Rich Rodriguez", "Rich Rod"), T("Brady Hoke"), T("Jim Harbaugh"), T("Sherrone Moore")])],
 "ndusc": [("Name a Notre Dame or USC head football coach from 1976 through 2024 (interim coaches count).", [
   T("Dan Devine"), T("Gerry Faust"), T("Lou Holtz"), T("Bob Davie"), T("Tyrone Willingham"), T("Kent Baer"), T("Charlie Weis"), T("Brian Kelly"),
   T("Marcus Freeman"), T("John Robinson"), T("Ted Tollner"), T("Larry Smith"), T("Paul Hackett"), T("Pete Carroll"), T("Lane Kiffin"),
   T("Ed Orgeron", "Coach O"), T("Clay Helton"), T("Steve Sarkisian", "Sark"), T("Donte Williams"), T("Lincoln Riley")])],
 "texou": [("Name a Texas or Oklahoma head football coach from 1966 through 2024.", [
   T("Darrell Royal"), T("Fred Akers"), T("David McWilliams"), T("John Mackovic"), T("Mack Brown"), T("Charlie Strong"), T("Tom Herman"),
   T("Steve Sarkisian", "Sark"), T("Jim Mackenzie"), T("Chuck Fairbanks"), T("Barry Switzer"), T("Gary Gibbs"), T("Howard Schnellenberger"),
   T("John Blake"), T("Bob Stoops"), T("Lincoln Riley"), T("Brent Venables")])],
 "bamauga": [("Name an Alabama or Georgia head football coach from 1964 through 2024 (interim coaches count).", [
   T("Bear Bryant", "Paul Bryant", "Paul \"Bear\" Bryant"), T("Ray Perkins"), T("Bill Curry"), T("Gene Stallings"), T("Mike DuBose"),
   T("Dennis Franchione"), T("Mike Shula"), T("Joe Kines"), T("Nick Saban"), T("Kalen DeBoer"), T("Vince Dooley"), T("Ray Goff"),
   T("Jim Donnan"), T("Mark Richt"), T("Bryan McClendon"), T("Kirby Smart")])],
 "fsumia": [("Name a Florida State or Miami (FL) head football coach from 1979 through 2024 (interim coaches count).", [
   T("Bobby Bowden"), T("Jimbo Fisher"), T("Odell Haggins"), T("Willie Taggart"), T("Mike Norvell"), T("Howard Schnellenberger"),
   T("Jimmy Johnson"), T("Dennis Erickson"), T("Butch Davis"), T("Larry Coker"), T("Randy Shannon"), T("Jeff Stoutland"), T("Al Golden"),
   T("Larry Scott"), T("Mark Richt"), T("Manny Diaz"), T("Mario Cristobal")])],
 "bama1st": [("Name an Alabama player drafted in the first round of the NFL Draft from 2020 through 2024.", [
   T("Henry Ruggs III", "Henry Ruggs"), T("Jedrick Wills Jr.", "Jedrick Wills"), T("Jerry Jeudy"), T("Tua Tagovailoa", "Tua"), T("Alex Leatherwood"),
   T("DeVonta Smith", "Devonta Smith"), T("Jaylen Waddle"), T("Mac Jones"), T("Najee Harris"), T("Patrick Surtain II", "Patrick Surtain"),
   T("Evan Neal"), T("Jameson Williams"), T("Bryce Young"), T("Jahmyr Gibbs"), T("Will Anderson Jr.", "Will Anderson"),
   T("Dallas Turner"), T("JC Latham", "J. C. Latham"), T("Terrion Arnold")])],
 "cfpcoach": [("Name the head coach of a team in the 12-team College Football Playoff (2024 season).", [
   T("Kirby Smart"), T("Ryan Day"), T("Dabo Swinney"), T("Steve Sarkisian", "Sark"), T("Marcus Freeman"), T("James Franklin"), T("Dan Lanning"),
   T("Josh Heupel"), T("Curt Cignetti"), T("Kenny Dillingham"), T("Rhett Lashlee"), T("Spencer Danielson")])],
 "osu1st": [("Name an Ohio State player drafted in the first round of the NFL Draft from 2020 through 2025.", [
   T("Chase Young"), T("Jeff Okudah"), T("Damon Arnette"), T("Justin Fields"), T("Garrett Wilson"), T("Chris Olave"), T("C. J. Stroud", "CJ Stroud", "C.J. Stroud"),
   T("Jaxon Smith-Njigba", "JSN", "Jaxon Smith Njigba"), T("Paris Johnson Jr.", "Paris Johnson"), T("Marvin Harrison Jr.", "Marvin Harrison"),
   T("Emeka Egbuka"), T("Donovan Jackson"), T("Tyleik Williams"), T("Josh Simmons")])],
}

HAND = {
 "joined": ("Name a school that joined the Big Ten or the SEC from 2010 through 2024.", [
   ("Texas", 2, ["UT"]), ("Oklahoma", 2, ["OU"]), ("USC", 2, ["Southern California", "Southern Cal"]), ("UCLA", 5, []), ("Oregon", 5, []),
   ("Texas A&M", 5, ["Texas A and M", "TAMU", "A&M"]), ("Washington", 8, ["UW"]), ("Nebraska", 8, []), ("Missouri", 8, ["Mizzou"]),
   ("Rutgers", 11, []), ("Maryland", 11, [])]),
 "pac12left": ("Name one of the 10 schools that left the Pac-12 in 2024.", [
   ("USC", 2, ["Southern California", "Southern Cal"]), ("UCLA", 2, []), ("Oregon", 2, []), ("Washington", 5, ["UW"]), ("Colorado", 5, []),
   ("Utah", 8, []), ("Arizona", 8, []), ("Arizona State", 11, ["ASU"]), ("Stanford", 11, []), ("California", 14, ["Cal", "Berkeley", "Cal Berkeley"])]),
 "titlegame": ("Name a school that played in a BCS or CFP national championship game (1998 through 2024 seasons).", [
   ("Alabama", 2, ["Bama"]), ("Ohio State", 2, []), ("Georgia", 2, ["UGA"]), ("Clemson", 2, []), ("LSU", 5, []), ("Florida", 5, []),
   ("Oklahoma", 5, ["OU"]), ("Texas", 5, ["UT"]), ("Michigan", 5, []), ("Notre Dame", 5, []), ("Florida State", 8, ["FSU"]),
   ("USC", 8, ["Southern California", "Southern Cal"]), ("Oregon", 8, []), ("Auburn", 8, []), ("Miami", 8, ["Miami (FL)", "The U"]),
   ("Tennessee", 11, []), ("Washington", 11, ["UW"]), ("TCU", 14, []), ("Nebraska", 14, []), ("Virginia Tech", 17, [])]),
 "titles80": ("Name a school that won a college football national title (AP or coaches' poll) from 1980 through 1994.", [
   ("Miami", 2, ["Miami (FL)", "The U"]), ("Alabama", 2, ["Bama"]), ("Notre Dame", 5, []), ("Nebraska", 5, []), ("Florida State", 5, ["FSU"]),
   ("Penn State", 5, []), ("Oklahoma", 8, ["OU"]), ("Georgia", 8, ["UGA"]), ("Clemson", 11, []), ("Colorado", 11, []),
   ("Washington", 14, ["UW"]), ("BYU", 14, ["Brigham Young"]), ("Georgia Tech", 17, [])]),
 "confs": ("Name a major college football conference, current or former (FBS / Division I-A).", [
   ("SEC", 2, ["Southeastern Conference", "Southeastern"]), ("Big Ten", 2, ["Big 10"]), ("Big 12", 2, ["Big Twelve"]), ("ACC", 2, ["Atlantic Coast Conference", "Atlantic Coast"]),
   ("Pac-12", 2, ["Pac 12", "Pac-10", "Pac 10", "Pac-8", "Pacific-12"]), ("Big East", 5, []), ("Mountain West", 8, ["MWC"]),
   ("Mid-American", 8, ["MAC", "Mid American"]), ("Sun Belt", 8, []), ("Conference USA", 11, ["C-USA", "CUSA"]),
   ("American Athletic", 11, ["AAC", "The American", "American"]), ("Big Eight", 11, ["Big 8"]), ("Southwest Conference", 14, ["SWC"]),
   ("WAC", 14, ["Western Athletic", "Western Athletic Conference"]), ("Big West", 17, []), ("Southern Conference", 20, ["SoCon"]), ("Ivy League", 20, ["Ivy"])]),
 "big12": ("Name a school that won or shared a Big 12 football title (1996 through 2024).", [
   ("Oklahoma", 2, ["OU"]), ("Texas", 2, ["UT"]), ("Baylor", 5, []), ("Oklahoma State", 8, ["OK State", "Okie State"]), ("Kansas State", 8, ["K-State", "K State"]),
   ("TCU", 8, []), ("Nebraska", 11, []), ("Texas A&M", 11, ["Texas A and M", "TAMU", "A&M"]), ("Colorado", 14, []), ("Arizona State", 14, ["ASU"])]),
 "oldbowls": ("Name a college bowl game still played today that was first played before 1976.", [
   ("Rose Bowl", 2, ["Rose"]), ("Sugar Bowl", 2, ["Sugar"]), ("Orange Bowl", 2, ["Orange"]), ("Cotton Bowl", 2, ["Cotton"]), ("Fiesta Bowl", 5, ["Fiesta"]),
   ("Peach Bowl", 5, ["Peach"]), ("Gator Bowl", 8, ["Gator"]), ("Citrus Bowl", 8, ["Citrus", "Tangerine Bowl"]), ("Sun Bowl", 11, ["Sun"]), ("Liberty Bowl", 11, ["Liberty"])]),
 # wildcards (Q5)
 "rivnick": ("Name a college football rivalry game nickname.", [
   ("Iron Bowl", 2, []), ("The Game", 2, []), ("Red River Rivalry", 2, ["Red River Shootout", "Red River Showdown", "Red River"]), ("Egg Bowl", 5, []),
   ("Apple Cup", 5, []), ("Holy War", 8, []), ("Backyard Brawl", 8, []), ("Bedlam", 8, []), ("Civil War", 8, []), ("Big Game", 11, []),
   ("Territorial Cup", 11, []), ("World's Largest Outdoor Cocktail Party", 11, ["Cocktail Party", "Worlds Largest Outdoor Cocktail Party"]),
   ("Third Saturday in October", 14, []), ("Palmetto Bowl", 14, []), ("Lone Star Showdown", 14, []), ("Border War", 17, []),
   ("Deep South's Oldest Rivalry", 17, ["Deep Souths Oldest Rivalry"]), ("Clean, Old-Fashioned Hate", 17, ["Clean Old Fashioned Hate"])]),
 "rivtrophy": ("Name a college football rivalry trophy.", [
   ("Little Brown Jug", 5, []), ("Paul Bunyan's Axe", 5, ["Paul Bunyans Axe"]), ("Commander-in-Chief's Trophy", 5, ["Commander in Chief's Trophy", "Commander in Chief Trophy", "Commander-in-Chief Trophy"]),
   ("Old Oaken Bucket", 8, []), ("Floyd of Rosedale", 8, ["Floyd"]), ("Governor's Cup", 8, ["Governors Cup"]), ("Golden Egg", 11, ["Egg Bowl trophy"]),
   ("Jeweled Shillelagh", 11, ["Shillelagh"]), ("Victory Bell", 11, []), ("Stanford Axe", 11, ["The Axe"]), ("Paul Bunyan Trophy", 14, []),
   ("Land Grant Trophy", 14, []), ("Megaphone Trophy", 14, []), ("Golden Boot", 14, []), ("Old Brass Spittoon", 17, []), ("Golden Hat", 17, []),
   ("Bronze Boot", 17, []), ("Keg of Nails", 20, [])]),
 "traditions": ("Name a famous college football gameday tradition.", [
   ("12th Man", 2, ["Twelfth Man"]), ("Tailgating", 2, ["Tailgate"]), ("Hook 'em Horns", 2, ["Hook em Horns", "Hook em"]), ("Dotting the i", 5, ["Script Ohio", "Dotting the I"]),
   ("Toomer's Corner", 5, ["Rolling Toomer's", "Rolling Toomers", "Toomers Corner"]), ("War Chant", 5, ["Tomahawk Chop", "Seminole War Chant"]), ("Jump Around", 5, []),
   ("Gator Chomp", 5, []), ("White Out", 5, ["Whiteout"]), ("Howard's Rock", 8, ["Howards Rock", "Running down the Hill"]), ("Sooner Schooner", 8, []),
   ("Ralphie's Run", 8, ["Ralphie Run", "Ralphies Run"]), ("Enter Sandman", 8, []), ("Play Like a Champion Today", 8, ["Play Like a Champion"]),
   ("Woo Pig Sooie", 8, ["Calling the Hogs", "Hog Call"]), ("Iowa Wave", 11, ["Hawkeye Wave", "The Wave", "Kinnick Wave"]), ("Rammer Jammer", 11, []),
   ("Touch the Banner", 11, ["Go Blue banner", "The Banner"]), ("The Grove", 11, ["Grove"]), ("Midnight Yell", 14, []), ("Tiger Walk", 14, []), ("Mr. Two Bits", 17, ["Mister Two Bits", "Two Bits"])]),
 "plays": ("Name a famous college football play with a nickname.", [
   ("Kick Six", 2, ["Kick-Six"]), ("Hail Flutie", 5, []), ("The Play", 5, []), ("Prayer at Jordan-Hare", 8, ["Prayer at Jordan Hare"]),
   ("Bush Push", 8, []), ("Statue of Liberty", 8, []), ("2nd and 26", 11, ["Second and 26", "2nd and 26 touchdown"]), ("Bluegrass Miracle", 11, []),
   ("Wide Right", 11, []), ("Fifth Down", 14, ["5th Down", "Fifth Down Game"]), ("Puntrooskie", 14, []), ("Miracle at Michigan", 14, []),
   ("Flea Kicker", 17, ["Immaculate Deflection"]), ("Miracle in Miami", 17, [])]),
 "mascots": ("Name a college football live animal mascot (by its name).", [
   ("Uga", 2, []), ("Mike the Tiger", 2, ["Mike"]), ("Bevo", 2, []), ("Ralphie", 5, []), ("Smokey", 5, []), ("Reveille", 8, []), ("War Eagle", 8, []),
   ("Bill the Goat", 8, ["Bill"]), ("Renegade", 11, []), ("Traveler", 11, ["Traveller"]), ("Tusk", 14, []), ("Cam the Ram", 17, ["Cam"]),
   ("Boomer and Sooner", 17, ["Boomer", "Sooner"]), ("Handsome Dan", 20, [])]),
}
NOT = {"Washington": ["Washington State"], "Oregon": ["Oregon State"], "Oklahoma": ["Oklahoma State"], "Texas": ["Texas Tech", "Texas State"],
       "Kansas State": ["Kansas"], "Arizona": ["Arizona State"], "Florida": ["Florida State"], "Georgia": ["Georgia Tech"]}

LEVEL = {"titlecoach": "E", "heistitle": "M", "titleqb": "M", "bamaqb": "E", "heisouusc": "M", "heisbig": "H", "osumich": "M", "ndusc": "H",
         "texou": "H", "bamauga": "M", "fsumia": "H", "bama1st": "M", "osu1st": "M", "joined": "M", "pac12left": "E", "titlegame": "E",
         "titles80": "H", "confs": "E", "big12": "H", "oldbowls": "M", "rivnick": "E", "rivtrophy": "H", "traditions": "E", "plays": "M", "mascots": "E", "cfpcoach": "M"}
Q5 = {"rivnick", "rivtrophy", "traditions", "plays", "mascots", "oldbowls"}
GROUPS = [{"titlecoach", "heistitle", "titleqb", "titlegame", "titles80"}, {"heisouusc", "heisbig"}, {"osumich", "ndusc", "texou", "bamauga", "fsumia"},
          {"bama1st", "osu1st", "bamaqb"}, {"joined", "pac12left", "big12", "confs"}]
OVERRIDE = {  # hand fixes where page views mislead (recent news, the obvious answer scoring low)
 "titlecoach": {"Urban Meyer": 2, "Ryan Day": 8, "Bobby Bowden": 8, "Mack Brown": 11, "Phillip Fulmer": 17},
 "heistitle": {"Charlie Ward": 14},
 "titleqb": {"Tua Tagovailoa": 5, "Tim Tebow": 5},
 "bamaqb": {"Tua Tagovailoa": 2, "AJ McCarron": 8},
 "heisouusc": {"Reggie Bush": 5},
 "heisbig": {"Archie Griffin": 5},
 "osumich": {"Sherrone Moore": 8, "Ryan Day": 5, "Woody Hayes": 5, "Bo Schembechler": 8, "Luke Fickell": 11},
 "ndusc": {"Lou Holtz": 2},
 "texou": {"Darrell Royal": 8, "Barry Switzer": 5, "Bob Stoops": 5, "Mack Brown": 5},
 "bamauga": {"Bear Bryant": 2, "Mike Shula": 11},
 "fsumia": {"Bobby Bowden": 2, "Jimmy Johnson": 5, "Mario Cristobal": 5, "Mark Richt": 11},
 "bama1st": {"Henry Ruggs III": 11, "DeVonta Smith": 5, "Jaylen Waddle": 8, "Jerry Jeudy": 8, "Najee Harris": 8, "Will Anderson Jr.": 8},
 "cfpcoach": {"Kirby Smart": 2, "Ryan Day": 5, "Dabo Swinney": 5, "Steve Sarkisian": 8, "Curt Cignetti": 8, "James Franklin": 8},
 "osu1st": {"Chase Young": 5, "Garrett Wilson": 8, "Marvin Harrison Jr.": 5, "Josh Simmons": 17},
}
