# Install BeautifulSoup if you haven't already, also use Python3

import urllib.request
from bs4 import BeautifulSoup
import nltk

quote_page = 'https://www.allrecipes.com/recipe/235357/chef-johns-penne-with-vodka-sauce/'

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
					'mix': 'wooden spoon', 'sauté': 'pan', 'saute': 'pan', 'barbecue': 'grill', 'baste': 'baster', 'broil': 'broiler',
					'beat': 'electric mixer/whisk', 'grill': 'grill', 'peel': 'peeler', 'poach': 'pot', 'puree': 'food processor',
					'purée': 'food processor', 'toast': 'toaster/oven', 'whip': 'electric mixer/whisk', 'roast': '', 'knead': '', 'marinate': '',
					'sift': '', 'steam': '', 'toss': '', 'bake': '', 'microwave': '', 'grease': ''}

vegetarian = {'chicken':'tofu', 'beef':'seitan', 'pork':'seitan', 'steak':'seitan', 'turkey':'tofu', 'ham':'tofu', 'bacon':'tofu'}






# Dictionary of units of measurement
units_measure = {'cup', 'cups', 'ounce', 'ounces', 'tablespoon', 'teaspoon', 'pound', 'pounds'}
page = urllib.request.urlopen(quote_page)

# Reads in HTML from AllRecipes.com
soup = BeautifulSoup(page, 'html.parser')
# Use HTML tags to grab the sections we want. This assumes all AllRecipes.com pages use the same tags.
ingredients_section = soup.find_all('span', attrs={'class': 'recipe-ingred_txt added'})
directions_section = soup.find_all('span', attrs={'class': 'recipe-directions__list--item'})

# Function to get the details of each ingredient (name, quantity, measurement). Feed it one line of the ingredients list with
# ntlk tags. Deals with ingredients with multiple descriptors like 1 (14.5 ounce) package. Some ingredients only have a quantity,
# like '1 large onion'
def ingredientParser(lineTokens):
	quantity = ''
	measurement = ''
	ingredient = ''
	inParen = False
	getMeasure = False
	quantityFound = False

	for word in lineTokens:
		if quantityFound:
			ingredient += word[0] + ' '
		else:
			if inParen:
				if word[1] == ')':
					quantity = quantity[:-1]
					inParen = False
					getMeasure = True

				quantity += word[0] + ' '
			elif word[1] in {'CD', '('}:
				quantity += word[0] + ' '
				if word[1] == '(':
					inParen = True
					quantity = quantity[:-1]
			else:
				quantityFound = True
				if (word[0] in units_measure) or getMeasure:
					measurement = word[0]
				else:
					ingredient += word[0] + ' '

	return ingredient[:-1], quantity, measurement


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
transform = input("Type 0 for no transformation. Type 1 for Vegetarian ")

print("INGREDIENTS")
for ingredient in ingredients_section:
	ingredients.append(ingredient.get_text())
	tokens = nltk.word_tokenize(ingredient.get_text())
	tagged = nltk.pos_tag(tokens)
	name, quantity, measurement = ingredientParser(tagged)
	if transform == "1":
		for meat in vegetarian:
			if meat in name:
				name = vegetarian[meat]
	print("")
	print("Ingredient as listed on AllRecipes.com: " + ingredient.get_text())
	print("Name: " + ''.join(name) + "     Quantity: " + ''.join(quantity) + "     Measurement: " + ''.join(measurement))

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
