from home_match_ai import *

home_match_ai = HomeMatchAI()

if input('Use predefined answers? (y/n): ') == 'n':
  for question in questions:
    query += "\n - " + input(question + "\n - ")
else:
  for answer in predefined_answers:
    query += "\n - " + answer
  
print(query)
  
output = home_match_ai.retrieve_property_recommendations(query=query, k=1)
print(f'\n{output.content}')