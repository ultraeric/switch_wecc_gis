import re
import csv
import pandas as pd
from mechanize import Browser, Item
import os


# https://www.arb.ca.gov/emfac/2014/combobox.php?_id=geo_level&_name=geo_level&_value=county
counties = [{"Alameda":"Alameda"},{"Alpine":"Alpine"},{"Amador":"Amador"},{"Butte":"Butte"},{"Calaveras":"Calaveras"},{"Colusa":"Colusa"},{"Contra Costa":"Contra Costa"},{"Del Norte":"Del Norte"},{"El Dorado":"El Dorado"},{"Fresno":"Fresno"},{"Glenn":"Glenn"},{"Humboldt":"Humboldt"},{"Imperial":"Imperial"},{"Inyo":"Inyo"},{"Kern":"Kern"},{"Kings":"Kings"},{"Lake":"Lake"},{"Lassen":"Lassen"},{"Los Angeles":"Los Angeles"},{"Madera":"Madera"},{"Marin":"Marin"},{"Mariposa":"Mariposa"},{"Mendocino":"Mendocino"},{"Merced":"Merced"},{"Modoc":"Modoc"},{"Mono":"Mono"},{"Monterey":"Monterey"},{"Napa":"Napa"},{"Nevada":"Nevada"},{"Orange":"Orange"},{"Placer":"Placer"},{"Plumas":"Plumas"},{"Riverside":"Riverside"},{"Sacramento":"Sacramento"},{"San Benito":"San Benito"},{"San Bernardino":"San Bernardino"},{"San Diego":"San Diego"},{"San Francisco":"San Francisco"},{"San Joaquin":"San Joaquin"},{"San Luis Obispo":"San Luis Obispo"},{"San Mateo":"San Mateo"},{"Santa Barbara":"Santa Barbara"},{"Santa Clara":"Santa Clara"},{"Santa Cruz":"Santa Cruz"},{"Shasta":"Shasta"},{"Sierra":"Sierra"},{"Siskiyou":"Siskiyou"},{"Solano":"Solano"},{"Sonoma":"Sonoma"},{"Stanislaus":"Stanislaus"},{"Sutter":"Sutter"},{"Tehama":"Tehama"},{"Trinity":"Trinity"},{"Tulare":"Tulare"},{"Tuolumne":"Tuolumne"},{"Ventura":"Ventura"},{"Yolo":"Yolo"},{"Yuba":"Yuba"}]

year = '2015'

if not os.path.exists('EMFAC2014_County/'):
    os.makedirs('EMFAC2014_County/')

if not os.path.exists('EMFAC2014_County/' + year):
    os.makedirs('EMFAC2014_County/' + year)

for county in counties:
    br = Browser()
    response = br.open("https://www.arb.ca.gov/emfac/2014/")
    print br.title()
    forms_list = []
    for f in br.forms():
        forms_list.append(f)
    # print(forms_list[1])

    br.select_form(nr=1)

    br.form['geo_level'] = ['county']
    region = br.find_control('region')
    # inject the current county into form because javascript blocks them
    item = Item(region, {"contents": county.keys()[0], "value": county.keys()[0]})
    # now set the region to the injected county
    br.form['region'] = [county.keys()[0]]

    br.form['cal_year[]'] = [year]
    br.form['season'] = ['annual']
    br.form['veh_cat_type'] = ['emfac2011']

    # https://www.arb.ca.gov/emfac/2014/combobox.php?_id=veh_cat_type&_name=veh_cat_type&_value=emfac2011
    veh_cat_option = br.find_control('veh_cat_option')
    # inject veh category
    item = Item(veh_cat_option, {"contents": "All", "value": "all"})
    # select injected veh category
    br.form['veh_cat_option'] = ['all']

    br.form['model_year'] = ['all']
    br.form['speed'] = ['all']
    br.form['fuel'] = ['All']

    # print d[0].keys()[0]
    # print d[0].values()[0]


    # print(br.form)
    print(br.form['region'][0])
    filename = br.form['region'][0] + '_' +\
            br.form['cal_year[]'][0] + '_' +\
            br.form['season'][0] + '_' +\
            br.form['veh_cat_type'][0] + '_' +\
            br.form['veh_cat_option'][0]
    # print filename

    response2 = br.submit()
    df = pd.read_csv(response2, skiprows=7) # skip the header, which looks like:
            # EMFAC2014 (v1.0.7) Emissions Inventory
            # Region Type: County
            # Region: Alameda
            # Calendar Year: 2015
            # Season: Annual
            # Vehicle Classification: EMFAC2011 Categories
            # Units: miles/day for VMT, trips/day for Trips, tons/day for Emissions, 1000 gallons/day for Fuel Consumption
    print df.head()
    # print df.shape
    # df = df.to_csv('EMFAC2014_County/' + year + '/' + filename + '.csv', index=False)
