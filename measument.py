#Reference of list of Common US Measurements
#https://en.wikibooks.org/wiki/Cookbook:Units_of_measurement
#https://en.wikipedia.org/wiki/Cooking_weights_and_measures
#http://startcooking.com/measurement-and-conversion-charts
#https://www.macmillandictionary.com/us/thesaurus-category/american/prepare-food-for-cooking-or-eating


list_of_abbrev_mesurement = {'pn':'pinch','ds':'dash','ssp':'saltspoon','csp':'coffeespoon','fl.dr.':'fluid dram','tsp':'teaspoon',
	                             't':'teaspoon','C':'cup','pt':'pint','qt':'quart','pot':'pottle','gal':'gallon','fl oz':'fluid ounce',
	                             'oz':'ounce'}


list_of_measurement = ['cup', 'cups', 'ounce', 'ounces', 'tablespoon', 'teaspoon', 'pound', 'pounds',
	                        'tablespoons','teaspoons','fluid ounce','fluid ounces','quart','quarts','liter','liters',
	                        'pint','pints','ounce','ounces','gram','grams','gallon','gallons','package','packages',
	                        'dessertspoon','dessertspoons', 'can','cans', 'needed','dash','pinch','sprig','sprigs'
                          ]

list_of_descriptors = ['bone-in','fresh','dried','extra-virgin','ground','whole wheat','whole grain','low sodium','skinless','fat-free','boneless','low-fat','nonfat',
                       'smooth','frozen','plain','Italian-style','Italian','all-purpose','dry','condensed','sour','white','cold','bulk','with juice','drained']

list_of_preparations = ['cooking','cooked','cook','baked','baking','bake','slicing','slice','sliced','diced','minced','mincing','mince','basted','baste','basting','beated','beating','beat',
                       'bind','bound','bingding','blanching','blanched','blanch','blend','blent','blending','boiling','boil','boned','bone','braised',
                       'braising','braise','bread','broiled','broiling','broil','browning','brown','browned','brush','brushing','brushed','caramelizing',
                       'caramelize','caramelized','chilling','chill','chilled','chop','chopping','chopped','clarified','clarifying','clarify','coating',
                       'coated','coat','peeling','peeled','peel','poach','poaching','poached','mix','mixed','mixing','shred','shredded','shreding','steamed','steam','steaming',
                       'toast','toasted','toasting','dipped','dipping','dip','discarrd','discarding','discarding','seeded','seed','seeding']
stop_words = ['and','taste','needed','to',',','or','(',')','e.g','such','.','as']


cooking_verbs = {'boil' : 'pot', 'stir' : 'wooden spoon', 'chop': 'knife', 'drain': 'colander', 'grate':'grater', 'simmer': 'pot',
          'fry': 'pan', 'slice': 'knife', 'cut': 'knife', 'dice': 'knife', 'flip': 'spatula', 'roll': 'rolling pin', 'mince': 'knife',
          'mix': 'wooden spoon', 'saut': 'pan', 'saute': 'pan', 'barbecue': 'grill', 'baste': 'baster', 'broil': 'broiler',
          'beat': 'electric mixer/whisk', 'grill': 'grill', 'peel': 'peeler', 'poach': 'pot', 'puree': 'food processor',
          'toast': 'toaster/oven', 'whip': 'electric mixer/whisk', 'roast': '', 'knead': '', 'marinate': '',
          'sift': '', 'steam': '', 'toss': '', 'bake': '', 'microwave': ''}


tools_dict = {'pot', 'press', 'baster', 'bowl', 'bottle opener', 'can opener', 'knife', 'tray', 'sheet', 'pan', 'skillet',
        'slicer', 'cheesecloth', 'cleaver', 'colander', 'cracker', 'cutting board', 'flour sifter', 'funnel', 'garlic press',
        'ladle', 'cup', 'spoon', 'thermometer', 'grater', 'blender', 'masher', 'shears', 'scissors', 'rolling pin',
        'scoop', 'spatula', 'tongs', 'whisk', 'fork', 'skewer', 'timer', 'processor', 'saucepan', 'griddle'}

    
