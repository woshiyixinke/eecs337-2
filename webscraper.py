# Install BeautifulSoup if you haven't already, also use Python3

import urllib.request
import PIL.ImageTk
import PIL.Image
from bs4 import BeautifulSoup
import nltk
import re
from tkinter import ttk
from tkinter import *
from measument import *




def getContentFromUrl(url):  
    content = urllib.request.urlopen(url)  
    content = BeautifulSoup(content, from_encoding='ascii')  
    return content

def showTools(window, tools):
	window.insert('end', "**TOOLS:\n")
	for tool in tools:
		window.insert('end', "-"+tool.title()+"\n")

def showMethods(window, methods):
	window.insert('end', "**Methods:\n")
	for method in methods:
		window.insert('end', "-"+method.title() + "\n")

def showDirections(window, directions):
	window.insert('end', "***** DIRECTIONS *****\n")
	i = 0
	for direction in directions:
		window.insert('end', "Step " + str(i+1) + ": " + direction + "\n\n")
		i += 1
#GUI Function
def insert_url(t, returned_var):
	t.insert('end', "***** INGREDIENTS *****\n")
	for ingrrr in returned_var["ingredients"]:
		t.insert('end', "Ingredient: "+ingrrr["name"] + ", ")
		t.insert('end','Preparations: ')
		p = ''
		for ppp in ingrrr['preparations']:
			p = p + ', '+ppp
		p = p[1:]
		t.insert('end',p)
		t.insert('end', '| Descriptors: ')
		d = ''
		for ddd in ingrrr['descriptors']:
			d = d + ', ' + ddd
		d = d[1:]
		t.insert('end', d)
		t.insert('end', " \n" )
		t.insert('end', "Measurement:"+ ingrrr["measurement"]+", Quantity:" + ingrrr["quantity"]+"\n")
		t.insert('end', '\n')

#quote_page = 'https://www.allrecipes.com/recipe/12009/cajun-chicken-pasta/'


# Function to get the details of each ingredient (name, quantity, measurement). Feed it one line of the ingredients list with
# ntlk tags. Deals with ingredients with multiple descriptors like 1 (14.5 ounce) package. Some ingredients only have a quantity,
# like '1 large onion'

def have_two_and_above_preparations(preparation):
	ts = nltk.word_tokenize(preparation)
	cnt = 0
	for t in ts:
		if t in list_of_preparations:
			cnt += 1
		if cnt > 1:
			return True
	return False


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
			quantity = 'to taste'
		else:
			quantity = '1'
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
					if descriptor.lower() not in descriptors:
						if descriptor.lower() in ingredient.lower():
							descriptors.append(token.lower())
					delete_words.append(token.lower())
			if token.lower() in list_of_preparations:
				indexStart = ingredient.index(token)
				prepa = ingredient[indexStart:]
				if ',' in prepa:	
					prepas = prepa.split(',')
					for p in prepas:
						preparations.append(p.lower())
						ts = nltk.word_tokenize(prepa)
						for t in ts:
							delete_words.append(t.lower())
						
				else:
					#preparations.append(prepa.lower())
					if(have_two_and_above_preparations(prepa)):
						ts = nltk.word_tokenize(prepa)
						for t in ts:
							if t.lower() in list_of_preparations and t.lower() not in preparations:
								preparations.append(t.lower())
							delete_words.append(t.lower())
					else:
						preparations.append(prepa.lower())
						ts = nltk.word_tokenize(prepa)
						for t in ts:
							delete_words.append(t.lower())


	for token in tokens:
		if token.lower() not in delete_words and token not in stop_words and token not in qty:
			name.append(token)
	names = ''
	for n in name:
		names = names + ' ' + n

	names = names.strip()
	

	if names is '':
		preparations = []
		descriptors = []
		delete_words = []
		for token in tokens:
			if token.lower() in measurement or token.lower() in list_of_abbrev_mesurement.keys():
				delete_words.append(token.lower())
			elif token.lower() not in measurement and token.lower() not in list_of_abbrev_mesurement.keys():
				for descriptor in list_of_descriptors:
					if token.lower() in descriptor.lower():
						if descriptor.lower() not in descriptors:
							descriptors.append(descriptor.lower())
						delete_words.append(token.lower())
				if token.lower() in list_of_preparations and token.lower() not in preparations:
					preparations.append(token.lower())
					delete_words.append(token.lower())

		for token in tokens:
			if token.lower() not in delete_words and token not in stop_words and token not in qty:
				name.append(token.lower())
		for n in name:
			names = names + ' ' + n

	names = names.strip()
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



# Find cooking verbs (and associated tools) and cooking tools explicitly mentioned and add them to the methods dictionary and tools
# dictionary, respectively.
def findToolsMethods(lineTokens):
	for word in lineTokens:
		if word[1] in {'JJ', 'JJR', 'JJS', 'NN', 'NNP', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}:
			key = word[0].lower()
			if key in tools_dict and key not in tools:
				tools.append(key)

			if key in cooking_verbs_2 and cooking_verbs_2[key] not in tools:
				if cooking_verbs_2[key] != '':
					tools.append(cooking_verbs_2[key])
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

def request_from_url(quote_page):
	# Dictionary of units of measurement
	#units_measure = {'cup', 'cups', 'ounce', 'ounces', 'tablespoon', 'teaspoon', 'pound', 'pounds'}
	#global content
	page = urllib.request.urlopen(quote_page)

	# Reads in HTML from AllRecipes.com
	soup = BeautifulSoup(page, 'html.parser')
	# Use HTML tags to grab the sections we want. This assumes all AllRecipes.com pages use the same tags.
	ingredients_section = soup.find_all('span', attrs={'class': 'recipe-ingred_txt added'})
	directions_section = soup.find_all('span', attrs={'class': 'recipe-directions__list--item'})
	recipe_name = soup.find_all('h1', attrs={'class': 'recipe-summary__h1'})
	photo_src = soup.find_all('img', attrs = {'class', 'rec-photo'})
	photo_src = photo_src[0].attrs['src'] 
	#print(photo_src)
	i = 1
	urllib.request.urlretrieve(photo_src, '%s.jpg' % i)
	global path
	path = './1.jpg'
	#content = getContentFromUrl(photo_src)
	#print(content)
	#print(photos)
	# Dictionary of cooking verbs with associated cooking tools.  Example: if I find the verb 'dice', I know that I need a knife.
	# NOTE: at the ends of the dictionary, we have cooking verbs with no associated tool

	for ingredient in ingredients_section:
		
		parsedIngredient = ingredientParser(ingredient.get_text())
		ingredients.append(parsedIngredient)
		


	ingre = {}
	ingre["ingredients"] = ingredients



	print('RECIPE: ' + recipe_name[0].text + '\n')


	# transform = input("Would you like to transform the recipe? \n0: No transformation, 1: Vegetarian, 2: Healthy, 3: Vegan, 4: Japanese\nType your answer:")
	transform = '0'

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
	neww = []
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
			neww.append(new_directions)
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
	return neww, tools, methods, ingre


def main():

	global ingredients
	global quantities 
	global directions 
	global tools 
	global methods 
	global window
	global photo

	ingredients = []
	quantities = []
	directions = []
	tools = []
	methods = []

	quote_page = 'https://www.allrecipes.com/recipe/12009/cajun-chicken-pasta/'
	directions, tools, methods, ingre = request_from_url(quote_page)
	im = PIL.Image.open(path)
	#print(path)
	im.thumbnail((200,150))
	
	window = Tk()
	window.title('Team 5 Recipe')
	window.resizable(0, 0)

	window.geometry('800x600')

	fm1 = Frame(window, width = 80, height = 12)
	photo = PIL.ImageTk.PhotoImage(im)
	l = Label(fm1, image = photo)
	l.photo = photo
	l.pack(side = 'left')
	toolsText = Text(fm1, width = 40, height = 7.5, bg = 'grey')
	toolsText.pack(side = 'left')
	fm2 = Frame(fm1, width = 40, height = 6)
	comvalue = StringVar()
	comboxlist = ttk.Combobox(fm2, textvariable= comvalue)
	comboxlist["values"]=("Vegetarian","Healthy","Vegan","Japanese", "Chinese") 
	comboxlist.current(0)
	comboxlist.pack(side = 'top')
	methodsText = Text(fm1, width = 20, height = 7.5, bg = 'grey')
	methodsText.pack(side = 'left')
	b1 = Button(fm2, text = 'transform', width = 10, height = 2)
	b1.pack(side = 'top')
	fm2.pack(side = 'left')
	fm1.pack(side = 'top')


	#b1 = Button(window, text = 'URL Request', width = 10, height = 2, command = lambda: insert_url(e,t))
	#b1.pack()
	ingredientText = Text(window, width = 120, height = 16, fg = 'black', bg = 'grey')
	#t.place(x = 400, y = 100)
	ingredientText.pack(side = 'top')
	directionsText = Text(window, width = 120, height = 18, bg = 'grey')
	directionsText.pack(side = 'top')
	showDirections(directionsText, directions)
	insert_url(ingredientText, ingre)
	showTools(toolsText, tools)
	showMethods(methodsText, methods)
	window.mainloop()


if __name__ == '__main__':
	main()


