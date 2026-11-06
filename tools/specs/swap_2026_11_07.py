T = lambda n, *a: (n, list(a))

# Replacements for off-topic questions (SNL hosts, anthem singers, refs, staff jobs...) on Nov 7 - Nov 23.
# Players wanted real football trivia. Keys are question ids; WHERE says which (date, q#) each one replaces.

WHERE = {"heishof": ("2026-11-07", 2), "kcgb": ("2026-11-07", 4), "celebs2": ("2026-11-10", 5), "rb1": ("2026-11-12", 3),
         "te1": ("2026-11-14", 3), "qb1": ("2026-11-15", 1), "broncqb": ("2026-11-21", 4), "qb2010": ("2026-11-22", 2),
         "nfl100": ("2026-11-23", 4)}

PAGE = {"Tim Brown": "Tim Brown (American football)", "Daniel Jones": "Daniel Jones (American football)",
        "Anthony Richardson": "Anthony Richardson (American football)", "Cam Ward": "Cam Ward (American football)",
        "Brandon Allen": "Brandon Allen (American football)", "Jim Brown": "Jim Brown", "Bobby Bell": "Bobby Bell",
        "Stone Johnson": "Stone Johnson", "Emmitt Thomas": "Emmitt Thomas", "Charles Woodson": "Charles Woodson"}
WIKI_ONLY = {"Stone Johnson", "Brandon Allen", "Zach Wilson", "Mac Jones", "Bobby Bell", "Emmitt Thomas", "Jordan Love", "Cam Ward"}

SPEC = {
 "heishof": [("Ten Heisman Trophy winners are in the Pro Football Hall of Fame. Name one.", [
   T("Barry Sanders"), T("Charles Woodson"), T("O. J. Simpson", "OJ Simpson", "O.J. Simpson", "OJ", "The Juice"), T("Tony Dorsett"), T("Earl Campbell"),
   T("Marcus Allen"), T("Roger Staubach"), T("Tim Brown"), T("Paul Hornung"), T("Doak Walker")])],
 "kcgb": [("Name a player whose number is retired by the Kansas City Chiefs or Green Bay Packers.", [
   T("Brett Favre"), T("Bart Starr"), T("Reggie White"), T("Ray Nitschke"), T("Don Hutson"), T("Tony Canadeo"),
   T("Len Dawson"), T("Derrick Thomas"), T("Jan Stenerud"), T("Willie Lanier"), T("Bobby Bell"), T("Buck Buchanan"),
   T("Emmitt Thomas"), T("Abner Haynes"), T("Mack Lee Hill"), T("Stone Johnson")])],
 "rb1": [("Name a running back drafted in the first round from 2015 through 2025.", [
   T("Todd Gurley"), T("Melvin Gordon"), T("Ezekiel Elliott", "Zeke Elliott", "Zeke"), T("Leonard Fournette"), T("Christian McCaffrey", "CMC"),
   T("Saquon Barkley", "Saquon"), T("Rashaad Penny"), T("Sony Michel"), T("Josh Jacobs"), T("Clyde Edwards-Helaire", "Clyde Edwards Helaire"),
   T("Najee Harris"), T("Travis Etienne"), T("Bijan Robinson", "Bijan"), T("Jahmyr Gibbs"), T("Ashton Jeanty"), T("Omarion Hampton")])],
 "te1": [("Name a tight end drafted in the first round from 2010 through 2025.", [
   T("Jermaine Gresham"), T("Tyler Eifert"), T("Eric Ebron"), T("O. J. Howard", "OJ Howard", "O.J. Howard"), T("Evan Engram"),
   T("David Njoku"), T("Hayden Hurst"), T("T. J. Hockenson", "TJ Hockenson", "T.J. Hockenson"), T("Noah Fant"), T("Kyle Pitts"),
   T("Dalton Kincaid"), T("Brock Bowers"), T("Colston Loveland"), T("Tyler Warren")])],
 "qb1": [("Name a quarterback drafted in the first round from 2020 through 2025.", [
   T("Joe Burrow"), T("Tua Tagovailoa", "Tua"), T("Justin Herbert"), T("Jordan Love"), T("Trevor Lawrence"), T("Zach Wilson"),
   T("Trey Lance"), T("Justin Fields"), T("Mac Jones"), T("Kenny Pickett"), T("Bryce Young"), T("C. J. Stroud", "CJ Stroud", "C.J. Stroud"),
   T("Anthony Richardson"), T("Caleb Williams"), T("Jayden Daniels"), T("Drake Maye"), T("Michael Penix Jr.", "Michael Penix"),
   T("J. J. McCarthy", "JJ McCarthy", "J.J. McCarthy"), T("Bo Nix"), T("Cam Ward"), T("Jaxson Dart")])],
 "broncqb": [("Name a quarterback who started a regular-season game for the Denver Broncos from 2016 through 2025 (after Peyton Manning).", [
   T("Trevor Siemian"), T("Paxton Lynch"), T("Brock Osweiler"), T("Case Keenum"), T("Joe Flacco"), T("Drew Lock"),
   T("Brandon Allen"), T("Jeff Driskel"), T("Brett Rypien"), T("Kendall Hinton"), T("Teddy Bridgewater"), T("Russell Wilson", "Russ Wilson"),
   T("Jarrett Stidham"), T("Bo Nix")])],
 "qb2010": [("Name a quarterback drafted in the first round from 2010 through 2016.", [
   T("Sam Bradford"), T("Tim Tebow"), T("Cam Newton"), T("Jake Locker"), T("Blaine Gabbert"), T("Christian Ponder"),
   T("Andrew Luck"), T("Robert Griffin III", "RG3", "RGIII", "Robert Griffin"), T("Ryan Tannehill"), T("Brandon Weeden"), T("EJ Manuel", "E. J. Manuel"),
   T("Blake Bortles"), T("Johnny Manziel"), T("Teddy Bridgewater"), T("Jameis Winston"), T("Marcus Mariota"), T("Jared Goff"),
   T("Carson Wentz"), T("Paxton Lynch")])],
 "nfl100": [("Name a quarterback or running back on the NFL 100 All-Time Team (picked in 2019).", [
   T("Tom Brady"), T("Peyton Manning"), T("Joe Montana"), T("John Elway"), T("Dan Marino"), T("Brett Favre"), T("Johnny Unitas"),
   T("Roger Staubach"), T("Otto Graham"), T("Sammy Baugh"), T("Jim Brown"), T("Walter Payton"), T("Barry Sanders"),
   T("Emmitt Smith"), T("Eric Dickerson"), T("Earl Campbell"), T("Gale Sayers"), T("O. J. Simpson", "OJ Simpson", "O.J. Simpson", "OJ", "The Juice"),
   T("Marion Motley"), T("Lenny Moore"), T("Steve Van Buren"), T("Dutch Clark")])],
}

HAND = {
 "celebs2": ("Name a famous NFL touchdown celebration, dance or postgame tradition.", [
   ("Lambeau Leap", 2, []), ("Gatorade shower", 2, ["Gatorade bath", "Gatorade dump", "Gatorade"]), ("Spike", 2, ["The Spike", "Spiking the ball"]),
   ("Griddy", 5, ["The Griddy", "Hit the Griddy"]), ("Ickey Shuffle", 5, ["Ickey Woods shuffle"]), ("Dirty Bird", 8, ["The Dirty Bird"]),
   ("Mile High Salute", 8, []), ("Discount Double Check", 8, []), ("Gronk Spike", 8, []), ("Dab", 8, ["The Dab", "Dabbing"]),
   ("Superman", 11, ["Superman celebration"]), ("Sack dance", 11, ["Sack Exchange dance"]), ("Sharpie", 14, ["Sharpie celebration", "TO Sharpie"]),
   ("Fun Bunch", 17, ["Fun Bunch high five"])]),
}

LEVEL = {"heishof": "M", "kcgb": "H", "celebs2": "E", "rb1": "M", "te1": "H", "qb1": "E", "broncqb": "M", "qb2010": "M", "nfl100": "H"}
OVERRIDE = {  # hand fixes where page views mislead (rookies, scandals, the obvious answer scoring low)
 "heishof": {"Barry Sanders": 2, "O. J. Simpson": 5},
 "te1": {"Kyle Pitts": 2, "Colston Loveland": 8, "Tyler Warren": 8, "Evan Engram": 8},
 "qb1": {"Joe Burrow": 2, "Justin Herbert": 5, "Trevor Lawrence": 5, "Tua Tagovailoa": 5, "Jayden Daniels": 5, "C. J. Stroud": 8, "Jaxson Dart": 8, "Mac Jones": 11},
 "broncqb": {"Bo Nix": 2, "Joe Flacco": 5, "Drew Lock": 5, "Jarrett Stidham": 14, "Trevor Siemian": 11},
 "qb2010": {"Andrew Luck": 2, "Tim Tebow": 5, "Jared Goff": 5, "Robert Griffin III": 5, "Johnny Manziel": 8, "Jameis Winston": 8},
 "nfl100": {"Joe Montana": 2, "Peyton Manning": 2, "O. J. Simpson": 8, "Walter Payton": 5, "Barry Sanders": 5, "Emmitt Smith": 5, "Jim Brown": 5},
}
