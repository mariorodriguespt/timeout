from __future__ import print_function, unicode_literals

import dirtyjson
from pprint import pprint
from PyInquirer import prompt
from examples import custom_style_2


PERFECT = 0
NO_DRINKS = 1
NO_FOOD = 2

suitable_places = []
places_to_avoid = {}
drinks = []

try:
    with open('users.json') as json_file:
        input_users = dirtyjson.load( json_file )

    with open('venues.json') as venues_file:
        venues = dirtyjson.load(venues_file)
except:
    print("Invalid JSON input, please check you files")
    exit(1)
    
all_users = []
for user in input_users:
    #Users who don't drink, eat or have a name won't be considered            
    if user.has_key('drinks') and user.has_key("drinks") and user.has_key("name"):
        all_users.append( user )

questions = [
    {
        'type': 'checkbox',        
        'message': 'Select the team members (enter to finish)',
        'name': 'members',
        'choices':  all_users,
        'validate': lambda answer: 'You must choose at least 1 member.' \
            if len(answer) == 0 else True
    }
]

members = prompt(questions, style=custom_style_2)

users=[]
for member in members['members']:
    for user in all_users:
        if member == user['name']:
            users.append( user )

def satisfy_user( venue , user ):
    if not len( set( user['drinks'] ).intersection( set( venue['drinks'] ) ) ):
        return NO_DRINKS

    if not len( set( venue['food'] ).difference( user['wont_eat'])):
        return NO_FOOD

    return PERFECT

for venue in venues:
    is_perfect = True

    if not venue.has_key("drinks") or not venue.has_key("food"):
        #Venues without food or drinks won't be considered
        continue

    for user in users:        
        response = satisfy_user( venue, user )
        if response != PERFECT:
            is_perfect = False
            item = "drink" if response == NO_DRINKS else "eat"

            if not places_to_avoid.has_key( venue['name'] ):
                places_to_avoid[ venue['name'] ] = { "users" : ["There is nothing for " + user['name'] + " to " + item ]}
            else:
                places_to_avoid[ venue['name'] ][ 'users' ].append( "There is nothing for " + user['name'] + " to " + item  )

    if is_perfect:
        suitable_places.append( venue['name'] )



print("Places to go:")        
for place in suitable_places :
    print( "\t" + place )

print("\nPlaces to avoid:")
for name , data in places_to_avoid.items():
    print( name )
    for user in data['users']:
        print( "\t" + user)