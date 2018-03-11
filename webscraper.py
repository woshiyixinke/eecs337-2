# Install BeautifulSoup if you haven't already, also use Python3

import urllib.request
from bs4 import BeautifulSoup
import nltk
import re
from measument import list_of_measurement, list_of_abbrev_mesurement, list_of_descriptors, list_of_preparations, stop_words

quote_page = 'https://www.allrecipes.com/recipe/78299/boilermaker-tailgate-chili/'

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

# Dictionary of units of measurement
#units_measure = {'cup', 'cups', 'ounce', 'ounces', 'tablespoon', 'teaspoon', 'pound', 'pounds'}
page = urllib.request.urlopen(quote_page)

# Reads in HTML from AllRecipes.com
soup = BeautifulSoup(page, 'html.parser')
# Use HTML tags to grab the sections we want. This assumes all AllRecipes.com pages use the same tags.
ingredients_section = soup.find_all('span', attrs={'class': 'recipe-ingred_txt added'})
directions_section = soup.find_all('span', attrs={'class': 'recipe-directions__list--item'})

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



# PRINT RESULTS
print("INGREDIENTS")
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

print("Ingredient as listed on AllRecipes.com")
ingre = {}
ingre["ingredients"] = ingredients
print(ingre)

print("")
print("DIRECTIONS")
for instruction in directions_section:
	directions.append(instruction.get_text())
	tokens = nltk.word_tokenize(instruction.get_text())
	tagged = nltk.pos_tag(tokens)
	print("")
	print(instruction.get_text())
	findToolsMethods(tagged)

print("")
print("TOOLS")
print(tools)
print("")
print("METHODS")
print(methods)


transform = input("Would you like to transform the recipe? Type 0 for no transformation, 1 for Vegetarian, 2 for Healthy: ")
print("transformed recipe")

if transform == '1':
	for protein in vegetarian.keys():
		for ingredient in ingre['ingredients']:
			if protein in ingredient['name']:
				ingredient['name'] = vegetarian[protein]
if transform == '2':
	for unhealthy in healthy_ingr.keys():
		for ingredient in ingre['ingredients']:
			if unhealthy in ingredient['name']:
				ingredient['name'] = healthy_ingr[unhealthy]

print("DIRECTIONS")
for instruction in directions_section:
	directions.append(instruction.get_text())
	tokens = nltk.word_tokenize(instruction.get_text())
	tagged = nltk.pos_tag(tokens)
	print("")
	if transform == '1':
		for i, word in enumerate(tokens):
			for protein in vegetarian.keys():
				if protein in word:
					tokens[i] = vegetarian[protein]
		for word in tokens:
			print(word, end=" ")
		x = ' '.join(tokens)
		x = x.replace(' ,',',').replace(' .','.')
		print(x)
	else:
		print(instruction.get_text())
	findToolsMethods(tagged)

print("")
print("TOOLS")
print(tools)
print("")
print("METHODS")
if transform == '2':
	for unhealthy in healthy_methods.keys():
		for i, method in enumerate(methods):
			if unhealthy in method:
				methods[i] = healthy_methods[unhealthy]
print(methods)
print("")


print(ingre)
