#Wrapper for ECHAIM

#
# A: Measured AE index was not available. A synthetic AE index based on PC index has been used instead for these data points if available.
# B: PC index is not available. Synthetic AE index is generated using PC = 0.0 for these data points.
# C: Data requested is beyond or prior to the IG index record. IG12 has been used if available.
# E: These requested data periods are for a time past the maximum time stamp of the NOAA F10.7 flux forecast.
# F: Measured F10.7 index was not available. The corresponding output was generated using a NOAA forecast of F10.7 flux if available.
# G: Data requested is beyond IG12 index record.
# H: Warning - Requested location is below the lower boundary of the model (50N geomagnetic). Since MLat is above 45N geomagnetic output is still provided.
#    Output should be interpreted with caution.
# I: Warning - Requested location is below 45N geomagnetic latitude. Output has been forced to NAN.
# J: Requested period is beyond or prior to the times available in the ap reference database. ap has been set to the all-time median (9.1)
# K: Requested period is beyond or prior to the times available in the dst reference database. dst has been set to the all-time median (-10.2)
#

def getECHAIMProfile(lat,lon,year,month,day,hour,minute,second):
    import subprocess as subp
    import numpy as np
    #turn off storm and precip and see difference DONE
    #solar miximum years
    #sunset and sunrise on the plot
    #bin by kp index
    #grid plot with # of data points
    #thursday ask about membership with AGU
    #thusday ask about using using madrigal data , PHIL
    storm = 0
    precip = 0
    dregion = 0
    command = ["./echaimpy",str(lat),str(lon),str(year),str(month),str(day),str(hour),str(minute),str(second),str(storm),str(precip),str(dregion)]
    #print(command)
    process = subp.Popen(command, shell=False, stdout=subp.PIPE, stderr=subp.STDOUT)
    output = process.communicate()[0]
    exitCode = process.returncode
    # file1 = open("echaimpyerrors.txt", "r")
    # s = file1.read()
    # #print(s)
    # file1.close()
    #print(output)
    arr = list(map(float,output.split()))

    return np.array(arr)

#Wrapper for IRI-2016
def getIRI2016Profile(lat,lon,yyyy,mmdd,hour):
    import subprocess as subp
    import numpy as np
    #,str(lat),str(lon),str(yyyy),str(mmdd),str(hour)
    fname = 'iripyinputs'
    # with open(fname, 'w') as f:
    #     f.write( "{:8.2f}  Transmitter latitude (degrees N)\n".format( lat ) )
    #     f.write( "{:8.2f}  Transmitter Longitude (degrees E)\n".format( lon ) )
    #     f.write( "{:8d}  Year (yyyy)\n".format( yyyy ) )
    #     f.write( "{:8d}  Month and day (mmdd)\n".format( mmdd ) )
    #     f.write( "{:8.2f}  hour (add 25 for UT) (begin)\n".format( hour + 25 ) )
    #     f.write( "None"+"\n" ) # DaViTpy install path

    command = ["./IRIpy",str(lat),str(lon),str(yyyy),str(mmdd),str(hour + 25)]
    #print(command)
    process = subp.Popen(command, shell=False, stdout=subp.PIPE, stderr=subp.STDOUT)
    output = process.communicate()[0]
    exitCode = process.returncode
    arr = list(map(float,output.split()))
    #print(arr)
    return np.array(arr)
