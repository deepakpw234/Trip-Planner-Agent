from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

from amadeus import Client, ResponseError
from amadeus import Location

import requests
import os
from dataclasses import dataclass

@dataclass
class AllToolsConfig:
    pass


class AllTools:
    def __init__(self):
        self.all_tools_config = AllToolsConfig()

    def get_flight_details(originLocation: str, distinationLocation: str, date: str, adults: int):
        '''This function provide the details of the flights'''

        amadeus_flight = Client()

        response = amadeus_flight.shopping.flight_offers_search.get(
            originLocationCode=originLocation,
            destinationLocationCode=distinationLocation,
            departureDate=date,
            adults=adults
        )

        return response.data[0:2]
    

    def get_cheapest_flight_details(origin: str, destination: str):
        '''This function provide the cheapest dates to travel from one city to another city'''

        amadeus_cheapest_flight_client = Client()

        cheapest_response = amadeus_cheapest_flight_client.shopping.flight_dates.get(origin=origin,destination=destination)

        return cheapest_response
    

    def get_airport_code(city:str):
        '''This function provide the airport code based on given city'''

        amadues_code = Client()
        
        code_repoonse = amadues_code.reference_data.locations.get(keyword='LON', subType=Location.ANY)

        return code_repoonse


    def curreny_converter(base_curreny:str, target_currency:str):
        '''this function convert curreny from EUR(base currency) to INR(target curreny)'''

        url_currency = f"https://v6.exchangerate-api.com/v6/2daabdcbf5800f70d4db2aef/pair/{base_curreny}/{target_currency}"

        currency_response = requests.get(url=url_currency)
        
        return currency_response.json()
    
    def collect_user_information(name: str, age: int, emailID: str):
        '''This function collect the user information for booking the flight'''
        return {'messages': f"name is {name}, age is {age}, emailID is {emailID}"}
    

    def book_flight_comfirmation():
        '''This function give the final confirmation of flight booking'''
        return { 'messages': AIMessage(content="Your flight has been booked successfully!") }