import sys
import requests
import json
from datetime import date
import re
import csv


#SAIT's current API key as of March 2019. Available to us until March 2020
APIKEY = '5c1ec485-e481-4e63-8838-2d55f6101b18'


#querys dell's endpoint using the api key
def get_warr_from_dell(URL, service_tags_list):
    #res = requests.get('https://api.dell.com/support/assetinfo/v4/getassetwarranty/35TTP22,F3S9732,1HJ31Q2?apikey=5c1ec485-e481-4e63-8838-2d55f6101b18')
    dell_response = requests.get(URL)

    #Error checking the respones from Dell
    if dell_response.status_code != 200:
        print(dell_response.text)
        sys.stderr.write('Error with response code: .\n' % (URL, dell_response.status_code))
        sys.stderr.write('Unable to get details for given service tag \n')
        return False

    #converts the dell xml response into json data
    data = dell_response.json()

    #opening the output file to eventually write the response information to it
    #output_file = open('output.csv', 'a')
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # writer.writeheader()
        writer.writerow(['Machine name', 'Model', 'Service Tag' ])



    #iterating through the responses with the respective service tags to compile the machine's information
    for x in range(0, len(service_tags_list)):
        Model = data["AssetWarrantyResponse"][x]["AssetHeaderData"]["MachineDescription"]
        responseTag = data["AssetWarrantyResponse"][x]["AssetHeaderData"]["ServiceTag"]
        ship_date = data["AssetWarrantyResponse"][x]["AssetHeaderData"]["ShipDate"]
        service = data["AssetWarrantyResponse"][x]["AssetEntitlementData"][0]["ServiceLevelDescription"]
        warranty_end = data["AssetWarrantyResponse"][x]["AssetEntitlementData"][0]["EndDate"]
        machine_name = get_key(responseTag)

        with open('output.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # writer.writeheader()
            writer.writerow([machine_name, Model, responseTag ])



        #printing the information to the console
        # print('Machine Name: ', machine_name)
        # print('Service Tag: ', responseTag)
        # print('Machine Model:' , Model)
        # print('Ship Date: ', ship_date)
        # print('Service Type: ', service)
        # print('Warranty End Date: ', warranty_end)
        # print('\n')


        #writing the information to a file
        # output_file.write('Machine Name: ' + machine_name + '\n')
        # output_file.write('Service Tag: ' + responseTag + '\n')
        # output_file.write('Machine Model: ' + Model + '\n')
        # output_file.write('Ship Date: ' + ship_date + '\n')
        # output_file.write('Service Type: '+ service + '\n')
        # output_file.write('Warranty End Date: ' + warranty_end + '\n')
        # output_file.write('\n')





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
    return endpoint


if __name__ == '__main__':

    #opens and reads the file with the computer information
    with open('CREC.csv', newline='') as csvfile:
        filereader = csv.reader(csvfile)

    #putting the information in the list and dictionary data structures
        computer_information_list = list(filereader)
        computer_information_dictionary = dict(computer_information_list)

    # extracts the service tags from the list
    svc_tags_from_file = []
    for x in range(0, len(computer_information_list)):
        svc_tags_from_file.append(computer_information_list[x][1])

    print('The service tags for this query: ', svc_tags_from_file)

    #splits the service tags into three groups (sub-lists)
    service_tags_group_1, service_tags_group_2, service_tags_group_3 = split_input(svc_tags_from_file)
    list_grouping = []

    #building a list of all of the lists of service tags
    list_grouping.append(service_tags_group_1)
    list_grouping.append(service_tags_group_2)
    list_grouping.append(service_tags_group_3)

    #Builds and queries 3 separate endpoints, the get warranty function writes the information to an output file
    for i in range(0, len(list_grouping)):
        endpoint = build_endpoint_url(list_grouping[i])
        get_warr_from_dell(endpoint, list_grouping[i])
