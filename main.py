from home_match_ai import *

home_match_ai = HomeMatchAI(temp=1)

user_preferences = ""
if input('Use predefined answers? (y/n): ') == 'n':
  for question in questions:
    user_preferences += "\n - " + input(question + "\n - ")
else:
  for answer in predefined_answers:
    user_preferences += "\n - " + answer

print("\n================== User Preferences =================")
print(user_preferences)

retrieval_query += user_preferences
print("\n================== Retrieval Query =================")
print(retrieval_query)

similar_listings = home_match_ai.db.similarity_search(query=retrieval_query, k=1)
print("\n================== Similar Listings Retrieved =================")
print(similar_listings)

output = home_match_ai.augment_recommended_listing(similar_listings[0], user_preferences)

print("\n================== Augmented Listing Recommendation =================")
print(f'\n{output.content}')