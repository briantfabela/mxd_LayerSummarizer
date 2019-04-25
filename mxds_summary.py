import csv, os, arcpy # modules

os.chdir("N:\\MXD") # go to MXD folder in N drive
text_string = '' # we will save all theinformation we get to this string
unique_lyrs_Str = '' # str will contain txt with all unique layers per mxd

# metadata variables
local_connections = 0
sde_connections = 0

# this list will maintain all the unique layer throughout the mxds
# it will also print at the end of the csv file
unique_layers=[] # will be store 'lyr.name' strings in tuples

for mxd_file in os.listdir(os.getcwd()): # iterate through mxds in folder

    mxd = arcpy.mapping.MapDocument(mxd_file)  # get mxd
    df = arcpy.mapping.ListDataFrames(mxd)  # get datafames in that mxd

    # get the mxd filename and the number of dataframes in it
    text_string+="File: {} (with {} Dataframes)\n".format(mxd_file, len(df))
    unique_lyrs_Str+="UNIQUE LAYERS FOR : {} \n".format(mxd_file) # UNIQUE LAYERS FOR: <MXD>
    start_index = len(unique_layers) # get start index, iteration will begin at this index
    end_index = start_index

    for d in df: # for each data frame in the mxd file
        text_string+="Data Frame: {}\nLayer, Source, Location\n".format(d.name)
        layers = arcpy.mapping.ListLayers(mxd, "", d)
        for lyr in layers: # for each layer in the data frame:

            text_string+="      {},".format(lyr.name) # get layer name

            # if the layer has a data source, list it
            if lyr.supports("DATASOURCE"):

                local_connections+=1
                source_type="Local" # set 'Local' as default dta source location
                # change data source location to SDE if path leads to SDE connection
                if "sql2.sde" in lyr.dataSource: # if layer is from SDE...
                    local_connections-=1
                    sde_connections+=1
                    source_type="SDE"
                text_string+=" {}, {}\n".format(lyr.dataSource, source_type)

                # once 'source_type' has been defined we can fill layer, Source, and Location
                for index in range(len(unique_layers)):
                    # if layer name already in list, break the loop
                    if unique_layers[index][0] == lyr.name:
                        break
                    else:
                        # add layer ('name', source+","+location) to list
                        unique_layers.append((lyr.name, lyr.dataSource+", "+source_type))
                        end_index+=1

            else: text_string+=" N/A, N/A \n"
        # END OF LAYER FOR-LOOP
    # END OF DATA FRAME FOR-LOOP

    text_string+="\n\n" # end each mxd file with a double enter

    # HERE YOU NEEED TO ITERATE THRU 'unique_layers' & ADD NEW LAYERS TO 'unique_lyrs_Str'
    if end_index - start_index > 0: # if there were any new unique layers in the mxd file
        for i in range(start_index, end_index):
            unique_lyrs_Str += unique_layers[0]+","+unique_layers[1]+"\n"
        unique_lyrs_Str+="\n"
# END OF MXD FOR-LOOP

# add some metadata at end of this file loop
text_string+="\nTask Completed Successfully!\n"
text_string+="TOTAL CONNECTIONS: {}".format(str(local_connections+sde_connections))
text_string+="Local Connections: {}".format(str(local_connections))
text_string+="SDE Connections: {}\n\n\n".format(str(sde_connections))


## ADD UNIQUE LAYERS LIST HERE ##
text_string+=unique_lyrs_Str 
#################################

text_file = open("MXDs_Summary.txt", "w")
text_file.write(text_string)
text_file.close()

# define files for the csv module to work with
txt_file = r"MXDs_Summary.txt"
csv_file = r"MXDs_LayerSummary.csv"
# open the files
in_txt = csv.reader(open(txt_file, "rb"), delimiter = ',')
out_csv = csv.writer(open(csv_file, 'wb'))

out_csv.writerows(in_txt)
del out_csv # clean both variables for the files to close
del in_txt

print("Task Completed Successfully!\n")
print("TOTAL CONNECTIONS: "+str(local_connections+sde_connections))
print("Local Connections: "+str(local_connections))
print("SDE Connections: "+str(sde_connections))
