from amadeus import Client,ResponseError
from dotenv import load_dotenv 
load_dotenv()

from dataclasses import dataclass
from langchain_core.messages import AIMessage

@dataclass
class HotelToolsConfig:
    pass

class HotelTools:
    def __init__(self):
        self.hotel_tool_config = HotelToolsConfig()

    def get_hotel_list_by_city(cityCode:str):
        '''This function give the hotel list based on the citycode'''

        amadeus_hotel_list = Client()

        hotel_list = amadeus_hotel_list.reference_data.locations.hotels.by_city.get(cityCode= cityCode)


        return hotel_list.data[0:10]
    

    def get_hotel_details_by_hotelID(hotelId: str, adults: int):
        """This function provide the details of the hotel based on the hotelIds"""

        amadeus_hotel_details = Client()

        hotel_detail = amadeus_hotel_details.shopping.hotel_offers_search.get(hotelIds=hotelId, adults=adults)

        return hotel_detail.data
    

    def final_confirmation_node(name: str, age: int, emailId:str):
        '''This function give confirm the cutomer details before booking the hotel'''
        msg = f"Confirming hotel booking for \nname: {name}\nage: {age}\nemailId: {emailId} "
    
        return { 'messages': AIMessage(content=msg) }

    
    def book_hotel_comfirmation():
        '''This function give the final confirmation of hotel booking'''
        return { 'messages': AIMessage(content="Your hotel has been booked successfully!") }
    

    

