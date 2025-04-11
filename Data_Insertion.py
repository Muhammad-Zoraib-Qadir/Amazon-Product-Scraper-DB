import pandas as pd
import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
import numpy as np
import mysql.connector
from mysql.connector import Error

# Loading JSON Data
with open('main_data.json', 'r') as file:
    data = json.load(file)

df = pd.json_normalize(data)

def get_color(color_list):
    if isinstance(color_list, list):
        # Return the entire list as the color information might be complete
        return color_list
    return 'NA'

df['Color'] = df['Color'].apply(get_color)

df.fillna(value=np.nan, inplace=True)

def list_duplicate(col):
    return df[col].duplicated(keep=False).any()

list_colors = [col for col in df.columns if df[col].dtype == object and list_duplicate(col)]

for col in list_colors:
    df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)

df.drop_duplicates(inplace=True)

df.dropna(subset=list_colors, inplace=True)

df.drop_duplicates(inplace=True)

df['Average_Review'] = df['Average_Review'].str.replace('[^\d\.]', '', regex=True).astype(float)


# NLP to clean text
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    cleaned_reviews = []
    for review in text:
        if isinstance(review, str):
            review = review.lower()
            review = ''.join([char for char in review if char not in string.punctuation])
            tokens = word_tokenize(review)
            tokens = [word for word in tokens if word not in stop_words]
            tokens = [lemmatizer.lemmatize(word) for word in tokens]
            cleaned_reviews.append(' '.join(tokens))
    return cleaned_reviews

df['cleaned_reviews'] = df['Reviews'].apply(lambda x: clean_text(x) if isinstance(x, list) else x)

# Function to extract image links
import json

df = pd.DataFrame(data)

import json

def extract_image_links(row):
    images= row['Color']
    image_links = []

    
    if isinstance(images, list):
        for color_info in images:
            if 'Images' in color_info and isinstance(color_info['Images'], dict):
                image_dict = color_info['Images']
                if 'Landing_Image' in image_dict:
                    image_links.append(image_dict['Landing_Image'])
                if 'Other Images' in image_dict and isinstance(image_dict['Other Images'], list):
                    image_links.extend(image_dict['Other Images'])
    
    elif isinstance(images, dict) and 'Images' in images and isinstance(images['Images'], dict):
        image_dict = images['Images']
        if 'Landing_Image' in image_dict:
            image_links.append(image_dict['Landing_Image'])
        if 'Other Images' in image_dict and isinstance(image_dict['Other Images'], list):
            image_links.extend(image_dict['Other Images'])
    
    return image_links

# Create a new column 'Image_Links'
df['Image_Links'] = df.apply(extract_image_links, axis=1)

# Display the DataFrame 
print(df[['Product_Title', 'Image_Links']])

# Connect to MySQL
mydb = None
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2102044***",
        database="amazon_data",
        auth_plugin='mysql_native_password'  # Specify the authentication plugin
    )

    if mydb.is_connected():
        cursor = mydb.cursor()

        for index, row in df.iterrows():
            cursor.execute("INSERT INTO Products (product_title, average_review) VALUES (%s, %s)",
                           (row['Product_Title'], row['Average_Review']))
            product_id = cursor.lastrowid

            for color in row['Color']:
                cursor.execute("INSERT INTO Colors (color_name) VALUES (%s)", (color['Color'],))
                color_id = cursor.lastrowid
                cursor.execute("INSERT INTO Product_Colors (product_id, color_id) VALUES (%s, %s)",
                               (product_id, color_id))

            for image_link in row['Image_Links']:
                cursor.execute("INSERT INTO Images (image_link) VALUES (%s)", (image_link,))
                image_id = cursor.lastrowid
                cursor.execute("INSERT INTO Products_Images (product_id, image_id) VALUES (%s, %s)",
                               (product_id, image_id))

        mydb.commit()
        print("Data inserted successfully")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if mydb is not None and mydb.is_connected():
        cursor.close()
        mydb.close()
        print("MySQL connection is closed")