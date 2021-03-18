import requests, json

def Weather(city):
    api_address='https://restcountries.eu/rest/v2/name/'
    url = api_address + city
    json_data = requests.get(url)
    temp = json_data.content
    json_data_temp = json.loads(temp)
    return FormatJson(json_data_temp[0])

def FormatJson(json):
    str_result = "Information of {} is: \n".format(json['name'])
    str_result += "Top level domain is: {}\n".format(json["topLevelDomain"])
    str_result += "Alpha 2 code : {}\n".format(json["alpha2Code"])
    str_result += "Alpha 3 code : {}\n".format(json["alpha3Code"])
    str_result += "Calling code : {}\n".format(json["callingCodes"])
    str_result += "Capital : {}\n".format(json["capital"])
    str_result += "Region : {}\n".format(json["region"])
    str_result += "Population : {}\n".format(json["population"])
    str_result += "And so on..."
    return str_result

# print(Weather("vietnam"))