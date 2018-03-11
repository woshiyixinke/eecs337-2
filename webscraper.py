# Install BeautifulSoup if you haven't already, also use Python3

import urllib.request
from bs4 import BeautifulSoup
import nltk
import re
from measument import list_of_measurement, list_of_abbrev_mesurement, list_of_descriptors, list_of_preparations, stop_words

quote_page = 'https://www.allrecipes.com/recipe/12009/cajun-chicken-pasta/'

ingredients = []
quantities = []
directions = []
tools = []
methods = []

# Dictionary of cooking tools
tools_dict = {'pot', 'press', 'baster', 'bowl', 'bottle opener', 'can opener', 'knife', 'tray', 'sheet', 'pan', 'skillet',
				'slicer', 'cheesecloth', 'cleaver', 'colander', 'cracker', 'cutting board', 'flour sifter', 'funnel', 'garlic press',
				'ladle', 'cup', 'spoon', 'thermometer', 'grater', 'blender', 'masher', 'shears', 'scissors', 'rolling pin',
				'scoop', 'spatula', 'tongs', 'whisk', 'fork', 'skewer', 'timer', 'processor', 'saucepan', 'griddle'}

# Dictionary of cooking verbs with associated cooking tools.  Example: if I find the verb 'dice', I know that I need a knife.
# NOTE: at the ends of the dictionary, we have cooking verbs with no associated tool
cooking_verbs = {'boil' : 'pot', 'stir' : 'wooden spoon', 'chop': 'knife', 'drain': 'colander', 'grate':'grater', 'simmer': 'pot',
					'fry': 'pan', 'slice': 'knife', 'cut': 'knife', 'dice': 'knife', 'flip': 'spatula', 'roll': 'rolling pin', 'mince': 'knife',
					'mix': 'wooden spoon', 'saut': 'pan', 'saute': 'pan', 'barbecue': 'grill', 'baste': 'baster', 'broil': 'broiler',
					'beat': 'electric mixer/whisk', 'grill': 'grill', 'peel': 'peeler', 'poach': 'pot', 'puree': 'food processor',
					'toast': 'toaster/oven', 'whip': 'electric mixer/whisk', 'roast': '', 'knead': '', 'marinate': '',
					'sift': '', 'steam': '', 'toss': '', 'bake': '', 'microwave': ''} #removed grease

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

# Dictionary of units of measurement
#units_measure = {'cup', 'cups', 'ounce', 'ounces', 'tablespoon', 'teaspoon', 'pound', 'pounds'}
page = urllib.request.urlopen(quote_page)

# Reads in HTML from AllRecipes.com
soup = BeautifulSoup(page, 'html.parser')
# Use HTML tags to grab the sections we want. This assumes all AllRecipes.com pages use the same tags.
ingredients_section = soup.find_all('span', attrs={'class': 'recipe-ingred_txt added'})
directions_section = soup.find_all('span', attrs={'class': 'recipe-directions__list--item'})
recipe_name = soup.find_all('h1', attrs={'class': 'recipe-summary__h1'})

# Function to get the details of each ingredient (name, quantity, measurement). Feed it one line of the ingredients list with
# ntlk tags. Deals with ingredients with multiple descriptors like 1 (14.5 ounce) package. Some ingredients only have a quantity,
# like '1 large onion'

def ingredientParser(ingredient):
	quantity = ''
	measurement = []
	#inParen = False
	#getMeasure = False
	#quantityFound = False
	descriptors = []
	preparations = []
	result = {}
	name = []
	ingredient = ingredient.strip()
	tokens = nltk.word_tokenize(ingredient)
	########################
    #find quantity, for some expressions like 1 (14.5 ounces) package,
    #we will only use 14.5 ounces as its quantity and measurement
    ########################
	regex = re.compile("[0-9]*\.[0-9]+|[0-9]+\s[0-9/]+|[0-9/]+|[0-9]+")
	qty = re.findall(regex, ingredient)
	if len(qty) == 0:
		if 'to taste' in ingredient:
			qty = 'to taste'
		else:
			qty = '1'
	elif len(qty) > 1:
		quantity = qty[1]
	else:
		quantity = qty[0]

	#if it has comma, we consider the second part as descriptor.
	#words = ingredient.split(",")
	tokens = nltk.word_tokenize(ingredient)

	#how to deal with comma and if there

	#Measurement Done, Preparation 50% done.
	delete_words = []
	#if preparation is not '':
	#	delete_words.append(preparation)
	for token in tokens:
		if(token.lower() in list_of_measurement or token.lower() in list_of_abbrev_mesurement.keys()):
			if(token.lower() not in list_of_measurement):
				measurement.append(list_of_abbrev_mesurement[word.lower()])
			else:
				measurement.append(token.lower())
			delete_words.append(token.lower())
		else:
			for descriptor in list_of_descriptors:
				if token.lower() in descriptor.lower():
					if token.lower() not in descriptors:
						descriptors.append(token.lower())
					delete_words.append(token.lower())
			if token.lower() in list_of_preparations:
				preparations.append(token.lower())
				delete_words.append(token.lower())

	for token in tokens:
		if token.lower() not in delete_words and token not in stop_words and token not in qty:
			name.append(token)
	names = ''
	for n in name:
		names = names + ' ' + n
	names = names.strip()
	#print(names)
	#print(descriptors)
	if len(measurement) == 0:
		measurement = "unit"
	else:
		measurement = measurement[0]

	if len(descriptors) == 0:
		descriptors.append('None')
	if len(preparations) == 0:
		preparations.append('None')
	result['name'] = names
	result['measurement'] = measurement
	result['quantity'] = quantity
	result['descriptors'] = descriptors
	result['preparations'] = preparations

	return(result)
	#print(names)
#	for word in lineTokens:
#		if quantityFound:
#			ingredient += word[0] + ' '
#		else:
#			if inParen:
#				if word[1] == ')':
#					quantity = quantity[:-1]
#					inParen = False
#

#				quantity += word[0] + ' '
#			elif word[1] in {'CD', '('}:
#				quantity += word[0] + ' '
#				if word[1] == '(':
#					inParen = True
#					quantity = quantity[:-1]
#			else:
#				quantityFound = True
#				if (word[0] in units_measure) or getMeasure:
#					measurement = word[0]
#				else:
#					ingredient += word[0] + ' '

#	return ingredient[:-1], quantity, measurement


# Find cooking verbs (and associated tools) and cooking tools explicitly mentioned and add them to the methods dictionary and tools
# dictionary, respectively.
def findToolsMethods(lineTokens):
	for word in lineTokens:
		if word[1] in {'JJ', 'JJR', 'JJS', 'NN', 'NNP', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}:
			key = word[0].lower()
			if key in tools_dict and key not in tools:
				tools.append(key)

			if key in cooking_verbs and cooking_verbs[key] not in tools:
				if cooking_verbs[key] != '':
					tools.append(cooking_verbs[key])
				if key not in methods:
					methods.append(key)

def transform_directions(tokens, ingredients, methods=None, tools=None):
	for i, word in enumerate(tokens):
		 # replace ingredients
		for original in ingredients.keys():
			if original in word:
				tokens[i] = ingredients[original]
		# optional: replace methods
		if(methods):
			for original_m in methods.keys():
				if original_m in word:
					tokens[i] = methods[original_m]
		# optional: replace tools
		if(tools):
			for original_t in tools.keys():
				if original_t in word:
					tokens[i] = tools[original_t]

	# print
	x = ' '.join(tokens)
	x = x.replace(' ,', ',').replace(' .', '.').replace(' ;', ';')
	return x

def transform_ingredients(ingre_list, replacements):
	for original in replacements:
		for ingredient in ingre_list['ingredients']:
			if original in ingredient['name']:
				ingredient['name'] = replacements[original]

def print_ingredients(ingre):
	for ingredient in ingre['ingredients']:
		readable_string = ingredient['quantity'] + " " + ingredient['measurement'] + " of " + ascii(ingredient['name']).replace('\'', '')
		print(readable_string)


def transform_tools(tools, new_tools): 
	for i, tool in enumerate(tools):
		if tool in new_tools:
			tools[i] = new_tools[tool]

def transform_methods(methods, new_methods): 
	for i, method in enumerate(methods):
		if method in new_methods:
			methods[i] = new_methods[method]

def print_tools(tools):
	for tool in tools:
		print("- " + tool.title())

def print_methods(methods):
	for method in methods:
		print("- " + method.title())



# PRINT RESULTS
# print("INGREDIENTS")
for ingredient in ingredients_section:
	#tokens = nltk.word_tokenize(ingredient.get_text())
	#tagged = nltk.pos_tag(tokens)
	#print(ingredient.get_text())
	parsedIngredient = ingredientParser(ingredient.get_text())
	ingredients.append(parsedIngredient)
	#ingredients.append(ingredient.get_text())
	#print("")
	#print("Ingredient as listed on AllRecipes.com: " + ingredient.get_text())
	#print("Name: " + ''.join(name) + "     Quantity: " + ''.join(quantity) + "     Measurement: " + ''.join(measurement))

# print("Ingredient as listed on AllRecipes.com")
ingre = {}
ingre["ingredients"] = ingredients
# print(ascii(ingre))

# print("")
# print("DIRECTIONS")
# for instruction in directions_section:
# 	directions.append(instruction.get_text())
# 	tokens = nltk.word_tokenize(instruction.get_text())
# 	tagged = nltk.pos_tag(tokens)
# 	print("")
# 	print(instruction.get_text())
# 	findToolsMethods(tagged)

# print("")
# print("TOOLS")
# print(tools)
# print("")
# print("METHODS")
# print(methods)

print('RECIPE: ' + recipe_name[0].text + '\n')


# transform = input("Would you like to transform the recipe? \n0: No transformation, 1: Vegetarian, 2: Healthy, 3: Vegan, 4: Japanese\nType your answer:")
transform = '4'

if transform == '1':
	transform_ingredients(ingre, vegetarian)
if transform == '2':
	transform_ingredients(ingre, healthy_ingr)
if transform == '3':
	transform_ingredients(ingre, vegan)
if transform == '4':
	transform_ingredients(ingre, japanese_ingr)



print("\n\n***** INGREDIENTS *****\n")
print_ingredients(ingre)

print("\n\n***** DIRECTIONS *****\n")
for i, instruction in enumerate(directions_section):
	directions.append(instruction.get_text())
	tokens = nltk.word_tokenize(instruction.get_text())
	tagged = nltk.pos_tag(tokens)
	if transform == '1':
		new_directions = transform_directions(tokens, vegetarian)
	elif transform == '2':
		new_directions = transform_directions(tokens, healthy_ingr, healthy_methods)
	elif transform == '3':
		new_directions = transform_directions(tokens, vegan)
	elif transform == '4':
		new_directions = transform_directions(tokens, japanese_ingr, japanese_methods, japanese_tools)
	else:
		new_directions = instruction.get_text()
	if(new_directions):
		print("Step " + str(i+1) + ": " + new_directions)
	findToolsMethods(tagged)

print("\n\n***** TOOLS *****\n")
if transform == '4':
	transform_tools(tools, japanese_tools)
print_tools(tools)

print("\n\n***** METHODS *****\n")
if transform == '2':
	transform_methods(methods, healthy_methods)
if transform == '4':
	transform_methods(methods, japanese_methods)
print_methods(methods)


