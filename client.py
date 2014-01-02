'''
Created on 8 Dec 2013

@author: rk
'''
import urllib
import urllib2

def post(url, post_data_dictionary):
    http_headers = {'User-Agent':'OWN'}
    post_data_encoded = urllib.urlencode(post_data_dictionary)
    request_object = urllib2.Request(url, post_data_encoded,http_headers)
    response = urllib2.urlopen(request_object)
    print response

def prepare_data( dataList ):
    fieldNames = ["track", "driver", "carClass", "carName", "sector1", "sector2", "sector3", "lapTime", "date", "total"]
    post_data_dictionary = {}
    for field in range(len(dataList)):
        if fieldNames[field] == "date":
            temp = dataList[field].split('-')
            date_string = '%(year)s-%(month)s-%(day)s' % {"year":temp[2], "month":temp[1], "day":temp[0]}
        else:
            post_data_dictionary[fieldNames[field]] = datalist[field]

    return post_data_dictionary

if __name__ == '__main__':

    url = "http://localhost:12080/"

    post_data_dictionary = {"track":"Hedge End SupoerStores", 
                            "driver":"Neil Ricketts",
                            "carClass":"Hot hatch",
                            "carName":"Vauxhall Astra", 
                            "sector1": '30', 
                            "sector2": '60', 
                            "sector3": '90', 
                            "lapTime": '180',
                            "date":"1999-12-31", 
                            "total":180
                            }

    post (url, post_data_dictionary)
