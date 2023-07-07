#The essence of this code is to acquire data from the American Bureau of Statistics
#We will use all the available pieces of data kept on the BLS platform
#The time frame we will use for this will be from 1980 to 2022, giving us a reach pool of data

import requests
import json
import prettytable
import openai
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CUUR0000SA0', 'SUUR0000SA0', 'LNS11000000', 'CES0500000007', 'CES0500000003', 'MPU4910012'
                                'LNS13000000', 'LNS12000000', 'CES0000000001', 'CES0500000002', 'PRS85006092', 'PRS85006152'
                                'LNS14000000', 'CES0500000008', 'PRS85006112', 'CUUR0000AA0', 'CWUR0000SA0', 'CUUR0000SA0L1E',
                                'WPSFD4', 'WPUFD4', 'WPUFD49104', 'WPUFD49116', 'WPUFD49207', 'EIUIR', ' EIUIQ', 'CIU1010000000000A',
                                ' CIU2010000000000A', 'CIU2020000000000A'
                                ], "startyear": "1980", "endyear": "2023"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)

# Prompt the user for a query
query = input("Enter your Question ")

# Prepare the data for the OpenAI GPT-3 model
documents = []
for series in json_data['Results']['series']:
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes = ""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            document = f"{seriesId} {year} {period} {value} {footnotes}"
            documents.append(document)

# Join the documents with new lines
documents_text = "\n".join(documents)


# Use the OpenAI GPT-3 model to answer the query
response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=query,
    max_tokens=50,
    temperature=0.7,
    n=1,
    stop=None
)
# Print the answer
print(response.choices[0].text)
