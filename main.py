from home_match_ai import *

home_match_ai = HomeMatchAI(temp=1)

answers = ""
if input('Use predefined answers? (y/n): ') == 'n':
  for question in questions:
    answers += "\n - " + input(question + "\n - ")
else:
  for answer in predefined_answers:
    answers += "\n - " + answer

print("\n================== User Answers =================")
print(answers)

output = home_match_ai.retrieve_property_recommendations(answers=answers, k=1)

print("\n================== Listing Recommendations =================")
print(f'\n{output.content}')