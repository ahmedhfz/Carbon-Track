import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder

def organizer(data):
    # Filling the nan values with "None"
    data.replace(np.nan, "None", inplace=True)

    # Ordinal Encoding
    ordinal_data = ["Body Type", "Diet", "How Often Shower", "Heating Energy Source",
                    "Transport", "Vehicle Type", "Social Activity", "Frequency of Traveling by Air",
                    "Waste Bag Size", "Energy efficiency"]
    
    ordinal_data_order = {
        'Body Type': ['underweight', 'normal', 'overweight', 'obese'],
        'Diet': ['vegan', 'vegetarian', 'pescatarian', 'omnivore'],
        'How Often Shower': ['less frequently', 'daily', 'twice a day', 'more frequently'],
        'Heating Energy Source': ['electricity', 'wood', 'natural gas', 'coal'],
        'Transport': ['walk/bicycle', 'public', 'private'],
        'Vehicle Type': ['None', 'electric', 'hybrid', 'lpg', 'petrol', 'diesel'],
        'Social Activity': ['never', 'sometimes', 'often'],
        'Frequency of Traveling by Air': ['never', 'rarely', 'frequently', 'very frequently'],
        'Waste Bag Size': ['small', 'medium', 'large', 'extra large'],
        'Energy efficiency': ['Yes', 'Sometimes', 'No']
    }

    
    categories = list(ordinal_data_order.values())
    ordinal_encoder = OrdinalEncoder(categories=categories)
    data[ordinal_data] = ordinal_encoder.fit_transform(data[ordinal_data])

    # One hot encoding
    Genders = ["female","male"]
    for gender in Genders:
        data[f"Sex_{gender}"] = data["Sex"].apply(lambda x: 1 if gender in x else 0)
    
    data = data.drop(columns=['Sex'])



   
    data['Cooking_With'] = data['Cooking_With'].apply(eval) # Turning the string into a list
    Cooking_materials = ['Airfryer', 'Grill', 'Microwave', 'Oven', 'Stove']
    for material in Cooking_materials:
        data[material] = data['Cooking_With'].apply(lambda x: 1 if material in x else 0)

    data = data.drop(columns=['Cooking_With'])
    
    data['Recycling'] = data['Recycling'].apply(eval)
    Recycling_materials = ['Glass', 'Metal', 'Paper', 'Plastic']
    for material in Recycling_materials:
        data[material] = data['Recycling'].apply(lambda x: 1 if material in x else 0)

    

    data = data.drop(columns=['Recycling'])
    
    
    
    return data 

