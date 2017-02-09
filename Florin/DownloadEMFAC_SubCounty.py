import re
import csv
import pandas as pd
from mechanize import Browser, Item
import os


# https://www.arb.ca.gov/emfac/2014/combobox.php?_id=geo_level&_name=geo_level&_value=sub_area
# counties = [{"Alameda":"Alameda"},{"Alpine":"Alpine"},{"Amador":"Amador"},{"Butte":"Butte"},{"Calaveras":"Calaveras"},{"Colusa ":"Colusa "},{"Contra Costa":"Contra Costa"},{"Del Norte":"Del Norte"},{"El Dorado":"El Dorado"},{"Fresno":"Fresno"},{"Glenn":"Glenn"},{"Humboldt":"Humboldt"},{"Imperial":"Imperial"},{"Inyo":"Inyo"},{"Kern":"Kern"},{"Kings":"Kings"},{"Lake":"Lake"},{"Lassen":"Lassen"},{"Los Angeles":"Los Angeles"},{"Madera":"Madera"},{"Marin":"Marin"},{"Mariposa":"Mariposa"},{"Mendocino":"Mendocino"},{"Merced":"Merced"},{"Modoc":"Modoc"},{"Mono":"Mono"},{"Monterey":"Monterey"},{"Napa":"Napa"},{"Nevada":"Nevada"},{"Orange":"Orange"},{"Placer":"Placer"},{"Plumas":"Plumas"},{"Riverside":"Riverside"},{"Sacramento":"Sacramento"},{"San Benito":"San Benito"},{"San Bernardino":"San Bernardino"},{"San Diego":"San Diego"},{"San Francisco":"San Francisco"},{"San Joaquin":"San Joaquin"},{"San Luis Obispo":"San Luis Obispo"},{"San Mateo":"San Mateo"},{"Santa Barbara":"Santa Barbara"},{"Santa Clara":"Santa Clara"},{"Santa Cruz":"Santa Cruz"},{"Shasta":"Shasta"},{"Sierra":"Sierra"},{"Siskiyou":"Siskiyou"},{"Solano":"Solano"},{"Sonoma":"Sonoma"},{"Stanislaus":"Stanislaus"},{"Sutter":"Sutter"},{"Tehama":"Tehama"},{"Trinity":"Trinity"},{"Tulare":"Tulare"},{"Tuolumne":"Tuolumne"},{"Ventura":"Ventura"},{"Yolo":"Yolo"},{"Yuba":"Yuba"}]
# sub_counties = [{"Alameda (SF)":"Alameda (SF)"},{"Alpine (GBV)":"Alpine (GBV)"},{"Amador (MC)":"Amador (MC)"},{"Butte (SV)":"Butte (SV)"},{"Calaveras (MC)":"Calaveras (MC)"},{"Colusa (SV)":"Colusa (SV)"},{"Contra Costa (SF)":"Contra Costa (SF)"},{"Del Norte (NC)":"Del Norte (NC)"},{"El Dorado (LT)":"El Dorado (LT)"},{"El Dorado (MC)":"El Dorado (MC)"},{"Fresno (SJV)":"Fresno (SJV)"},{"Glenn (SV)":"Glenn (SV)"},{"Humboldt (NC)":"Humboldt (NC)"},{"Imperial (SS)":"Imperial (SS)"},{"Inyo (GBV)":"Inyo (GBV)"},{"Kern (MD)":"Kern (MD)"},{"Kern (SJV)":"Kern (SJV)"},{"Kings (SJV)":"Kings (SJV)"},{"Lake (LC)":"Lake (LC)"},{"Lassen (NEP)":"Lassen (NEP)"},{"Los Angeles (MD)":"Los Angeles (MD)"},{"Los Angeles (SC)":"Los Angeles (SC)"},{"Madera (SJV)":"Madera (SJV)"},{"Marin (SF)":"Marin (SF)"},{"Mariposa (MC)":"Mariposa (MC)"},{"Mendocino (NC)":"Mendocino (NC)"},{"Merced (SJV)":"Merced (SJV)"},{"Modoc (NEP)":"Modoc (NEP)"},{"Mono (GBV)":"Mono (GBV)"},{"Monterey (NCC)":"Monterey (NCC)"},{"Napa (SF)":"Napa (SF)"},{"Nevada (MC)":"Nevada (MC)"},{"Orange (SC)":"Orange (SC)"},{"Placer (LT)":"Placer (LT)"},{"Placer (MC)":"Placer (MC)"},{"Placer (SV)":"Placer (SV)"},{"Plumas (MC)":"Plumas (MC)"},{"Riverside (MD\/MDAQMD)":"Riverside (MD\/MDAQMD)"},{"Riverside (MD\/SCAQMD)":"Riverside (MD\/SCAQMD)"},{"Riverside (SC)":"Riverside (SC)"},{"Riverside (SS)":"Riverside (SS)"},{"Sacramento (SV)":"Sacramento (SV)"},{"San Benito (NCC)":"San Benito (NCC)"},{"San Bernardino (MD)":"San Bernardino (MD)"},{"San Bernardino (SC)":"San Bernardino (SC)"},{"San Diego (SD)":"San Diego (SD)"},{"San Francisco (SF)":"San Francisco (SF)"},{"San Joaquin (SJV)":"San Joaquin (SJV)"},{"San Luis Obispo (SCC)":"San Luis Obispo (SCC)"},{"San Mateo (SF)":"San Mateo (SF)"},{"Santa Barbara (SCC)":"Santa Barbara (SCC)"},{"Santa Clara (SF)":"Santa Clara (SF)"},{"Santa Cruz (NCC)":"Santa Cruz (NCC)"},{"Shasta (SV)":"Shasta (SV)"},{"Sierra (MC)":"Sierra (MC)"},{"Siskiyou (NEP)":"Siskiyou (NEP)"},{"Solano (SF)":"Solano (SF)"},{"Solano (SV)":"Solano (SV)"},{"Sonoma (NC)":"Sonoma (NC)"},{"Sonoma (SF)":"Sonoma (SF)"},{"Stanislaus (SJV)":"Stanislaus (SJV)"},{"Statewide Totals":"Statewide Totals"},{"Sutter (SV)":"Sutter (SV)"},{"Tehama (SV)":"Tehama (SV)"},{"Trinity (NC)":"Trinity (NC)"},{"Tulare (SJV)":"Tulare (SJV)"},{"Tuolumne (MC)":"Tuolumne (MC)"},{"Ventura (SCC)":"Ventura (SCC)"},{"Yolo (SV)":"Yolo (SV)"},{"Yuba (SV)":"Yuba (SV)"}]
# sub_counties = [{"Alameda (SF)":"Alameda (SF)"}]
#note: for some reason errors on ones with / in name
sub_counties = [{"Riverside (SC)":"Riverside (SC)"},{"Riverside (SS)":"Riverside (SS)"},{"Sacramento (SV)":"Sacramento (SV)"},{"San Benito (NCC)":"San Benito (NCC)"},{"San Bernardino (MD)":"San Bernardino (MD)"},{"San Bernardino (SC)":"San Bernardino (SC)"},{"San Diego (SD)":"San Diego (SD)"},{"San Francisco (SF)":"San Francisco (SF)"},{"San Joaquin (SJV)":"San Joaquin (SJV)"},{"San Luis Obispo (SCC)":"San Luis Obispo (SCC)"},{"San Mateo (SF)":"San Mateo (SF)"},{"Santa Barbara (SCC)":"Santa Barbara (SCC)"},{"Santa Clara (SF)":"Santa Clara (SF)"},{"Santa Cruz (NCC)":"Santa Cruz (NCC)"},{"Shasta (SV)":"Shasta (SV)"},{"Sierra (MC)":"Sierra (MC)"},{"Siskiyou (NEP)":"Siskiyou (NEP)"},{"Solano (SF)":"Solano (SF)"},{"Solano (SV)":"Solano (SV)"},{"Sonoma (NC)":"Sonoma (NC)"},{"Sonoma (SF)":"Sonoma (SF)"},{"Stanislaus (SJV)":"Stanislaus (SJV)"},{"Statewide Totals":"Statewide Totals"},{"Sutter (SV)":"Sutter (SV)"},{"Tehama (SV)":"Tehama (SV)"},{"Trinity (NC)":"Trinity (NC)"},{"Tulare (SJV)":"Tulare (SJV)"},{"Tuolumne (MC)":"Tuolumne (MC)"},{"Ventura (SCC)":"Ventura (SCC)"},{"Yolo (SV)":"Yolo (SV)"},{"Yuba (SV)":"Yuba (SV)"}]
if not os.path.exists('EMFAC2014_SubCounty/'):
    os.makedirs('EMFAC2014_SubCounty/')

for county in sub_counties:
    br = Browser()
    response = br.open("https://www.arb.ca.gov/emfac/2014/")
    print br.title()
    forms_list = []
    for f in br.forms():
        forms_list.append(f)
    # print(forms_list[1])

    br.select_form(nr=1)

    # print br.form

    br.form['geo_level'] = ['sub_area']
    region = br.find_control('region')
    # inject the current subcounty into form because javascript blocks them
    item = Item(region, {"contents": county.keys()[0], "value": county.keys()[0]})
    # now set the region to the injected county
    br.form['region'] = [county.keys()[0]]

    br.form['cal_year[]'] = ['2016']
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

    response2 = br.submit()
    df = pd.read_csv(response2, skiprows=7) # skip the header, which looks like:
            # EMFAC2014 (v1.0.7) Emissions Inventory
            # Region Type: County
            # Region: Alameda
            # Calendar Year: 2015
            # Season: Annual
            # Vehicle Classification: EMFAC2011 Categories
            # Units: miles/day for VMT, trips/day for Trips, tons/day for Emissions, 1000 gallons/day for Fuel Consumption
    # print df.head()
    # print df.shape
    df = df.to_csv('EMFAC2014_SubCounty/' + filename + '.csv', index=False)
