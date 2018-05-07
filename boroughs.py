#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""opens and reads  files found on the local filesystem"""


import json


GRADES = {'A':'1.0','B':'0.9','C':'0.8','D':'0.7','F':'0.6'}

                        
def get_score_summary(filename):
    """Takes a filename as a string and returns
    a summarized version of the data.

    Args:
        filename:  A CSV file.

    Return:
        A dictionary with summarized version of the data.

    Example:

        >>> get_score_summary('inspection_results.csv')
        {'BRONX': (156, 0.9762820512820514),
         'BROOKLYN': (417, 0.9745803357314144),
         'STATEN ISLAND': (46, 0.9804347826086955),
         'MANHATTAN': (748, 0.9771390374331528),
         'QUEENS': (414, 0.9719806763285019)}
        >>>
    """

    fhandler = open (filename,'r')
    counter = 0
    new_dict = {}
    for line in fhandler:
        read_fhandler = line.split(',')
        CAMIS = read_fhandler[0]
        if CAMIS != 'CAMIS':
            GRADE = read_fhandler[10]
            BORO = read_fhandler[1]
            if len(GRADE) > 0:
                if GRADE != 'P':
                    new_dict.update({CAMIS:(GRADE, BORO)})
        counter += 1
        
        
    fhandler.close()
    
    Bronx_sum = 0
    Manhattan_sum = 0
    Brooklyn_sum = 0
    Staten_island_sum = 0
    Queens_sum = 0
    Bronx_count = 0
    Manhattan_count = 0
    Brooklyn_count = 0
    Staten_Island_count = 0
    Queens_count =0
    num_sum_rest = {}
    for key in new_dict:
        if new_dict[key][1] == 'BRONX':
            Bronx_count += 1
            Bronx_sum += float(GRADES[new_dict[key][0]])
        elif new_dict[key][1] == 'MANHATTAN':
            Manhattan_count += 1
            Manhattan_sum += float(GRADES[new_dict[key][0]])
        elif new_dict[key][1] == 'QUEENS':
            Queens_count += 1
            Queens_sum += float(GRADES[new_dict[key][0]])
        elif new_dict[key][1] == 'BROOKLYN':
            Brooklyn_count +=1
            Brooklyn_sum += float(GRADES[new_dict[key][0]])
        elif new_dict[key][1] == 'STATEN ISLAND':
            Staten_Island_count += 1
            Staten_island_sum += float(GRADES[new_dict[key][0]])

            
        
    num_sum_rest = {'BRONX':(Bronx_count, Bronx_sum / Bronx_count),
                    'BROOKLYN':(Brooklyn_count, Brooklyn_sum / Brooklyn_count),
                    'STATEN ISLAND':(Staten_Island_count, Staten_island_sum / Staten_Island_count),
                    'MANHATTAN':(Manhattan_count, Manhattan_sum / Manhattan_count),
                    'QUEENS':(Queens_count, Queens_sum / Queens_count)
}
    return num_sum_rest
                                


def get_market_density(Filename):
    """Opens a file descriptor for a JSON file.
    Returns a dictionary with number of green markets x borough.

    Args:
        Filename:  A JSON file with  Green Markets data.

    Return:
        A dictionary of the number of green markets per borough.

    Example:
        >>> get_market_density('green_markets.json')
        {'BRONX': 32, 'BROOKLYN': 48,
         'STATEN ISLAND': 2, 'MANHATTAN': 39, 'QUEENS': 16}
        >>>
    """
    fh=open(Filename,'r')
    loaded_json=json.load(fh)
    fh.close
    Bronx_MarketCounter = 0
    Queens_MarketCounter = 0
    SI_MarketCounter = 0
    Brooklyn_MarketCounter = 0
    Manhattan_MarketCounter = 0
    for x in range(len(loaded_json["data"])) :
        if (loaded_json["data"][x][8].strip()) == 'Bronx':
                Bronx_MarketCounter += 1
        elif (loaded_json["data"][x][8].strip()) == 'Queens':
                Queens_MarketCounter += 1
        elif (loaded_json["data"][x][8].strip()) == 'Manhattan':
                Manhattan_MarketCounter += 1
        elif (loaded_json["data"][x][8].strip()) == 'Brooklyn':
                Brooklyn_MarketCounter += 1
        elif (loaded_json["data"][x][8].strip()) == 'Staten Island':
                SI_MarketCounter += 1
      
        x += 1
  
    Market_dict={'BRONX':Bronx_MarketCounter,
                'BROOKLYN':Brooklyn_MarketCounter,
                'STATEN ISLAND':SI_MarketCounter,
                'MANHATTAN':Manhattan_MarketCounter,
                'QUEENS':Queens_MarketCounter
               }
   
    return Market_dict
    

def correlate_data(file1,file2,output_file):
    """Use the previous two functions to get
    aggregate market and restaurant score data per-borough.

    Args:
        file1: Name of a file with restaurant scores data
        file2: Name of a JSON file with green_market data
        output_file: Filenam that will contain the output
                     of this function.

    Return:
        A dictionary with the borough food score and the
        percentage density of green markets to restaurateurs.

    Example:
        {'BRONX': [0.9762820512820514, 0.1702127659574468],
         'BROOKLYN': [0.9745803357314144, 0.1032258064516129],
         'STATEN ISLAND': [0.9804347826086955, 0.041666666666666664],
         'MANHATTAN': [0.9771390374331528, 0.04955527318932656],
         'QUEENS': [0.9719806763285019, 0.037209302325581395]}
    """
        
    restaurants = get_score_summary(file1)
    markets = get_market_density(file2)
    restaurants_markets ={'BRONX':[restaurants['BRONX'][1],
                          (float(markets['BRONX'])/float((restaurants['BRONX'][0]+ markets['BRONX'])))],
                          'BROOKLYN':[restaurants['BROOKLYN'][1],
                          (float(markets['BROOKLYN'])/float((restaurants['BROOKLYN'][0]+ markets['BROOKLYN'])))],
                          'STATEN ISLAND':[restaurants['STATEN ISLAND'][1],
                          (float(markets['STATEN ISLAND'])/float((restaurants['STATEN ISLAND'][0]+ markets['STATEN ISLAND'])))],
                          'MANHATTAN':[restaurants['MANHATTAN'][1],
                          (float(markets['MANHATTAN'])/float((restaurants['MANHATTAN'][0]+ markets['MANHATTAN'])))],
                          'QUEENS':[restaurants['QUEENS'][1],
                          (float(markets['QUEENS'])/float((restaurants['QUEENS'][0]+ markets['QUEENS'])))],
}
                          
    filepath = output_file
    fhandler = open(filepath,'w')
    
    jdata = json.dumps(restaurants_markets)
    fhandler.write(jdata)
    
    fhandler.close()
