import sys
import requests
import json
from datetime import date
import re
import csv


#Specify your API key (note, this is not an actual key)
APIKEY = '854u5jf993hn50320'


#querys dell's endpoint using the api key
def get_warr_from_dell(URL, service_tags_list, output_file):
    #uses python's request library to build a url and retrieve the information
    dell_response = requests.get(URL)

    #converts the dell xml response into json data
    data = dell_response.json()

    #iterating through the responses with the respective service tags to compile the machine's information
    for x in range(0, len(service_tags_list)):
        Model = data["AssetWarrantyResponse"][x]["AssetHeaderData"]["MachineDescription"]
        responseTag = data["AssetWarrantyResponse"][x]["AssetHeaderData"]["ServiceTag"]
        ship_date = data["AssetWarrantyResponse"][x]["AssetHeaderData"]["ShipDate"]
        service = data["AssetWarrantyResponse"][x]["AssetEntitlementData"][0]["ServiceLevelDescription"]
        warranty_end = data["AssetWarrantyResponse"][x]["AssetEntitlementData"][0]["EndDate"]
        machine_name = get_key(responseTag)

        #opening the output file, writing the response information to it, separating the items by a comma
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([machine_name, Model, responseTag, ship_date, warranty_end, service])


#function that splits a single list into 3 separate lists. You can change how many sub lists are created by
#changing the 3 to some number or you can even change it to be an arbitrary value say n and pass this value as a
#parameter to which the function could look like split_input(some_list, n)
def split_input(some_list):
    k, m = divmod(len(some_list), 3)
    return (some_list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(0, 3))

#looks up a key in the dictionary using the value, i.e. looks up the machine name using the service tag
def get_key(val):
    for key, value in computer_information_dictionary.items():
         if val == value:
             return key

    return "key doesn't exist"

#adds the service tags and the API key to the URL so that we can actually query it
def build_endpoint_url(service_tags):
    result = ','.join(service_tags)
    endpoint = 'https://api.dell.com/support/assetinfo/v4/getassetwarranty/'+result+"?apikey=" + APIKEY

    print('Accessing endpoint: ', endpoint)
    print('\n')
    return endpoint


#main function, opens the CSV file, converts it into something python can play with, extracts the service tags, builds URLs, queries those URLS, and the spits out the
#warranty information into a csv file
if __name__ == '__main__':

    #allows the user to specify the input file of service tags to use for this query as well as the output file with all of the data
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        #opens and reads the file with the computer information
        with open(input_file, newline='') as csvfile:
            filereader = csv.reader(csvfile)

        #putting the information in the list and dictionary data structures
            computer_information_list = list(filereader)
            computer_information_dictionary = dict(computer_information_list)

    except ValueError:
        print('Something went wrong importing and converting your file.. Are you sure your file is formatted correctly?\n')

    # extracts the service tags from the list
    svc_tags_from_file = []
    for x in range(0, len(computer_information_list)):
        svc_tags_from_file.append(computer_information_list[x][1])

    #splits the service tags into three groups (sub-lists) to perform 3 separate queries
    service_tags_group_1, service_tags_group_2, service_tags_group_3 = split_input(svc_tags_from_file)

    list_grouping = []
    #building a list of all of the lists of service tags, yes a list of lists..
    list_grouping.append(service_tags_group_1)
    list_grouping.append(service_tags_group_2)
    list_grouping.append(service_tags_group_3)

    #opening the output file to write the header information to it
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Machine name', 'Model', 'Service Tag', 'Ship Date', 'Warranty End Date', 'Service Type'])


    try:
        #Builds and queries 3 separate endpoints, the get warranty function writes the information to an output file
        for i in range(0, len(list_grouping)):
            endpoint = build_endpoint_url(list_grouping[i])
            get_warr_from_dell(endpoint, list_grouping[i], output_file)
    except IndexError:
        print('Something is wrong with the URL we are querying... You might have included non-Dell service tags or bad characters in the url..\n')

    print("API Query completed. You can find the warranty information in the output file.\n")
    print("Exiting.\n")
