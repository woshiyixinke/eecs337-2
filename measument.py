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
                       'smooth','frozen','plain','Italian-style','Italian','all-purpose','dry','condensed','sour','white','cold','bulk','with juice','drained','heavy']

list_of_preparations = ['cooking','cooked','cook','baked','baking','bake','slicing','slice','sliced','diced','minced','mincing','mince','basted','baste','basting','beated','beating','beat',
                       'bind','bound','bingding','blanching','blanched','blanch','blend','blent','blending','boiling','boil','boned','bone','braised',
                       'braising','braise','bread','broiled','broiling','broil','browning','brown','browned','brush','brushing','brushed','caramelizing',
                       'caramelize','caramelized','chilling','chill','chilled','chop','chopping','chopped','clarified','clarifying','clarify','coating',
                       'coated','coat','peeling','peeled','peel','poach','poaching','poached','mix','mixed','mixing','shred','shredded','shreding','steamed','steam','steaming',
                       'toast','toasted','toasting','dipped','dipping','dip','discarrd','discarding','discarding','seeded','seed','seeding']
stop_words = ['and','taste','needed','to',',','or','(',')','e.g','such','.','as','into']


cooking_verbs = {'boil' : 'pot', 'stir' : 'wooden spoon', 'chop': 'knife', 'drain': 'colander', 'grate':'grater', 'simmer': 'pot',
          'fry': 'pan', 'slice': 'knife', 'cut': 'knife', 'cutting':'knife','dice': 'knife', 'flip': 'spatula', 'roll': 'rolling pin', 'mince': 'knife',
          'mix': 'wooden spoon', 'saut': 'pan', 'saute': 'pan', 'barbecue': 'grill', 'baste': 'baster', 'broil': 'broiler',
          'beat': 'electric mixer/whisk', 'grill': 'grill', 'peel': 'peeler', 'poach': 'pot', 'puree': 'food processor',
          'toast': 'toaster/oven', 'whip': 'electric mixer/whisk', 'roast': '', 'knead': '', 'marinate': '',
          'sift': '', 'steam': '', 'toss': '', 'bake': '', 'microwave': ''}

cooking_verbs_2 = {"cut": "knife", "cutting": "knife","chop": "knife","chopping": "knife","mince": "knife","minced": "knife","mincing": "knife","slice": "knife","sliced": "knife",
  "slicing": "knife","dice": "knife","diced": "knife","dicing": "knife","cube": "knife","cubed": "knife","cubing": "knife","bake": "oven","baked": "oven","baking": "oven",
  "microwave":"microwave","microwaved":"microwave","microwaving":"microwave","baste":"baster","basted":"baster","basting":"baster","grate":"grater","grated":"grater","grating":"grater",
  "shred":"grater","shredding":"grater","shredded":"grater","measure":"measuring cups","measured":"measuring cups","measuring":"measuring cups","peel":"peeler","peeled":"peeler",
  "peeling":"peeler","core":"paring knife","cored":"paring knife","pare":"paring knife","pared":"paring knife","paring":"paring knife","blend":"electric mixer",
  "blended":"electric mixer","blending":"electric mixer","skewer": "barbecue fork","skewered": "barbecue fork","skewering": "barbecue fork",
  "strain": "strainer","straining": "strainer","glaze": "pastry brush", "glazed": "pastry brush","glazing": "pastry brush","stir":"wooden spoon",
  "stirred":"wooden spoon","stirring":"wooden spoon","beat": "whisk","beating": "whisk","spoon":"spoon"}


tools_dict = {'pot', 'press', 'baster', 'bowl', 'bottle opener', 'can opener', 'knife', 'tray', 'sheet', 'pan', 'skillet',
        'slicer', 'cheesecloth', 'cleaver', 'colander', 'cracker', 'cutting board', 'flour sifter', 'funnel', 'garlic press',
        'ladle', 'cup', 'spoon', 'thermometer', 'grater', 'blender', 'masher', 'shears', 'scissors', 'rolling pin',
        'scoop', 'spatula', 'tongs', 'whisk', 'fork', 'skewer', 'timer', 'processor', 'saucepan', 'griddle','microwage'}

vegetarian = {'sausage':'tofu','chicken':'tofu', 'beef':'seitan', 'pork':'seitan', 'steak':'seitan', 'turkey':'tofu', 'ham':'tofu', 'bacon':'tofu',
        'chuck':'seitan'}

healthy_ingr = {'butter':'olive oil', 'oil':'olive oil', 'bacon':'turkey bacon', 'ice cream':'frozen yogurt','flour':'whole wheat flour', 'sugar':'stevia',
        'bread':'whole wheat bread', 'heavy cream':'milk', 'whole milk':'fat-free milk', 'ground beef':'ground turkey', 'egg':'egg whites',
        'syrup':'honey'}

healthy_methods = {'fry':'bake'}

vegan = {'sausage':'tofu','chicken':'tofu', 'beef':'seitan', 'pork':'seitan', 'steak':'seitan', 'turkey':'tofu', 'ham':'tofu', 'bacon':'tofu',
    'chuck':'seitan', 'cheese': 'soy cheese', 'eggs': 'tofu scramble', 'chicken stock': 'vegetable stock', 'beef stock': 'vegetable stock', 
    'butter': 'sunflower oil', 'yogurt': 'soy yogurt', 'yoghurt': 'soy yoghurt', 'sour cream': 'soy yogurt', 'mayonnaise': 'vegan mayo', 
    'mayo': 'vegan mayo', 'honey': 'agave', 'milk': 'soy milk', 'pasta': 'vegan pasta', 'noodles': 'vegan noodles', 'cream': 'soy yogurt'}

japanese_ingr = {'noodles': 'ramen', 'pasta': 'ramen', 'butter': 'teryaki sauce', 'potatoes': 'Ube purple potatoes', 'potato': 'Ube purple potato',
        'salt': 'Shio salt', 'cheese': 'Sakura cheese', 'mushrooms': 'shiitake mushrooms', 'onion': 'green onion'}

japanese_methods = {'fry': 'stir fry', 'saute': 'stir fry', 'sautee': 'stir fry'}

japanese_tools = {'skillet': 'wok', 'pan': 'wok', 'pot': 'clay pot', 'wooden': 'bamboo'}

    
