from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

from static_variables import *
from helpers.file_helpers import *

import os
import json
from typing import Dict

class HomeMatchAI:
    
    llm: ChatOpenAI
    """Language model instance for generating and processing real estate listings."""

    embedding_model: OpenAIEmbeddings
    """Embeddings instance for processing text and generating embeddings."""
    
    db: Chroma
    """Chroma vector store instance for storing and retrieving real estate listings."""

    __LISTINGS_FILE_PATH: str = './listings.json'
    """File path for saving and loading real estate listings."""
    
    listings: list[Document]
    """List of Document objects representing the real estate listings."""


    def __init__(self, temp: float = 0.0, max_tokens: int = 3000, embedding_model_name: str = 'text-embedding-3-small', num_listings: int = 10) -> None:
        """
        This function initializes the HomeMatchAI class by setting up the API key, generating and loading
        real estate listings, initializing the chat model, setting up embeddings, and initializing the database.
        Parameters:
         - num_listings (int): The number of listings to generate. Default is 10.
         - temp (float): The temperature setting for the chat model. Default is 0.0.
         - max_tokens (int): The maximum number of tokens for the chat model. Default is 3000.
         - embedding_model (str): The model to use for embeddings. Default is 'text-embedding-3-small'.
        """
        
        os.environ['OPENAI_API_KEY'] = 'voc-338851266126677430740968d3fb3551e100.82453590'
        os.environ['OPENAI_API_BASE'] = 'https://openai.vocareum.com/v1'
        
        if num_listings is None or num_listings <= 0:
            num_listings = 10

        self.__setup_chat_model(temp=temp, tokens=max_tokens)
        self.__setup_embeddings(model_name=embedding_model_name)
        self.__generate_and_load_listings(num_listings=num_listings)
        self.__setup_database()


    def __setup_chat_model(self, temp: float = 0.0, tokens: int = 3000) -> None:
        """
        This function initializes the ChatOpenAI model with the specified temperature and maximum tokens.
        Parameters:
         - temp (float): The temperature setting for the chat model. Default is 0.0.
         - tokens (int): The maximum number of tokens for the chat model. Default is 3000.
        """

        self.llm = ChatOpenAI(temperature=temp, max_tokens=tokens)
    
    
    def __setup_embeddings(self, model_name: str = 'text-embedding-3-small') -> None:
        """
        This function initializes the OpenAIEmbeddings instance with the specified model name.
        Parameters:
         - model_name (str): The model to use for embeddings. Default is 'text-embedding-3-small'.
        """

        self.embedding_model = OpenAIEmbeddings(model=model_name)
        
    def __setup_database(self) -> None:
        """
        This function initializes the Chroma vector store database using the generated listings and embedding model.
        """

        self.db = Chroma.from_documents(documents=self.listings, embedding=self.embedding_model)


    def __generate_and_load_listings(self, num_listings: int = 10) -> None:
        """
        This function generates and loads real estate listings.
        Parameters:
         - num_listings (int): The number of listings to generate. Default is 10.
        """
        
        self.__generate_and_save_listings(num_listings)
        self.listings = self.__load_listings()
    

    def __generate_and_save_listings(self, num_listings: int) -> None:
        """
        This function generates and saves real estate listings to a JSON file if the file does not already exist.
        Parameters:
         - num_listings (int): The number of listings to generate.
        """

        if not os.path.exists(self.__LISTINGS_FILE_PATH):
           messages = [
               SystemMessage(content=GEN_PROMPT),
               HumanMessage(content=PromptTemplate(
                    input_variables=['num_listings'],
                    template='Generate exactly {num_listings} real estate listings in JSON format.'
                ).format(num_listings=num_listings))
            ]
           
           content = self.llm.invoke(input=messages).content
           process_llm_json_response(content=content, output_file_path=self.__LISTINGS_FILE_PATH)


    def __load_listings(self) -> list[Document]:
        """
        This function loads real estate listings from a JSON file and converts them into a list of Document objects.
        Returns:
         - list[Document]: A list of Document objects representing the real estate listings.
        """
        
        try:
            with open(self.__LISTINGS_FILE_PATH, 'r', encoding='utf-8') as file:
                data = json.load(file)
                listings: list[Dict[str, str]] = data.get('listings', data) if isinstance(data, dict) else data
        except FileNotFoundError:
            raise FileNotFoundError(f"Listings file not found: {self.__LISTINGS_FILE_PATH}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in listings file: {self.__LISTINGS_FILE_PATH}")
        except Exception as e:
            raise RuntimeError(f"Error loading listings: {e}")
            
        return [
            Document(
                page_content=listing.get('description', ''),
                metadata={
                    'neighborhood': listing.get('neighborhood', ''),
                    'price': listing.get('price', ''),
                    'bedrooms': listing.get('bedrooms', ''),
                    'bathrooms': listing.get('bathrooms', ''),
                    'house_size': listing.get('house_size', ''),
                    'neighborhood_description': listing.get('neighborhood_description', '')
                }
            ) for listing in listings
        ]
        
    def retrieve_property_recommendations(self, answers: str, k: int = 3) -> AIMessage:
        """
        This function recommends real estate listings based on a given query by performing a similarity search.
        Parameters:
         - query (str): The query string containing user preferences.
         - k (int): The number of similar listings to retrieve. Default is 3.
        Returns:
         - AIMessage: The AI message containing the recommended listings.
        """
        

        similar_listings = self.db.similarity_search(query=retrieval_query+answers, k=k)
        prompt = PromptTemplate(
            template='{query}\nContext: {listings_to_personalize}',
            input_variables=['query', 'listings_to_personalize']
        )
        return self.llm.invoke(prompt.format(query=query+answers, listings_to_personalize=similar_listings))