import os

GEN_PROMPT = '''
  You are a helpful real estate listing generator.
  You generate highly descriptive close approximations to realistic listings using fake made up data.
  Here is the data every generated listing should have:
  - neighborhood
  - price
  - bedrooms
  - bathrooms
  - house_size
  - description
  - neighborhood_description
  
  Ensure the generated data is purely and strictly plain text and in JSON format. No code blocks or any other kind of block. PURELY PLAIN JSON
  Always include the unit of measure for house size.
  Generate valid, complete JSON only. Do not truncate the response.
  Use the South African Rands and Metric units of measurement.
  
  Stick strictly to this template:
  [
  {
    "neighborhood": "...",
    "price": "...",
    "bedrooms": ...,
    "bathrooms": ...,
    "house_size": "...",
    "description": "...",
    "neighborhood_description": "..."
  },
  {...}
]
'''

questions = [
  "How big do you want your house to be?", 
  "What are 3 most important things for you in choosing this property?", 
  "Which amenities would you like?", 
  "Which transportation options are important to you?",
  "How urban do you want your neighborhood to be?",   
]

retrieval_query = """ 
Find the listing that best matches these user preferences:

"""

query = """
Based on the questions and answers below, tell me the one listing that best suits these preferences.
Personalize the description of the listings to the specified preferences but make sure the description is still factual and based entirely on the given listings.
When a listing does not perfectly match the user's preferences, do not focus on its shortcomings.
Instead, recommend the next best alternative or describe how to refine the search to find a better match.
"""

predefined_answers = [
  "A comfortable three-bedroom house with a spacious kitchen and a cozy living room.",
  "A quiet neighborhood, good local schools, and convenient shopping options.",
  "A backyard for gardening, a two-car garage, and a modern, energy-efficient heating system.",
  "Easy access to a reliable bus line, proximity to a major highway, and bike-friendly roads.",
  "A balance between suburban tranquility and access to urban amenities like restaurants and theaters."
]