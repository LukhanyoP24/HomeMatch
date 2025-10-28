from home_match_ai import *

home_match_ai = HomeMatchAI()

questions = [
  "How big do you want your house to be?", 
  "What are 3 most important things for you in choosing this property?", 
  "Which amenities would you like?", 
  "Which transportation options are important to you?",
  "How urban do you want your neighborhood to be?",   
]

query = """
Based on the questions and answers below, tell me the one listing that best suits these preferences.
Personalize the description of the listings to the specified preferences but make sure the description is still factual and based entirely on the given listings.
"""

predefined_answers = [
  "A comfortable three-bedroom house with a spacious kitchen and a cozy living room.",
  "A quiet neighborhood, good local schools, and convenient shopping options.",
  "A backyard for gardening, a two-car garage, and a modern, energy-efficient heating system.",
  "Easy access to a reliable bus line, proximity to a major highway, and bike-friendly roads.",
  "A balance between suburban tranquility and access to urban amenities like restaurants and theaters."
]

if input('Use predefined answers? (y/n): ') == 'n':
  for question in questions:
    query += "\n - " + input(question + "\n - ")
else:
  for answer in predefined_answers:
    query += "\n - " + answer
  
print(query)
  
output = home_match_ai.retrieve_property_recommendations(query=query, k=1)
print(f'\n{output.content}')