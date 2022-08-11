import os
import matplotlib.pyplot as plt
import models
import numpy as np
import random
import math

from matplotlib import style

import matplotlib.dates

from datetime import datetime

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

showplots = True
usePercentError = True
#       YYYY        MON       DAY       HOUR      MIN       SEC
#data 1 2006         2        22        23         0         0
#data 2 2016        11        10        13        15         0
#data 3 2021        11         2        13        15         0

# year = 2016
# month = 11
# day = 10
# hour = 13
# minute = 15
# second = 0
#
# xpoints = models.getECHAIMProfile(42.6,288.5,year,month,day,hour,minute,second)
# xpoints2 = models.getIRI2016Profile(42.6,288.5,year,month*100 + day,hour + (minute/60.0))
# hourtime = hour + (minute/60.0)
#
# ypoints = np.arange(60,560,1)
kps = np.array([])
errors_echaim = np.array([])
errors_iri = np.array([])
dates_x = []
#pick time range
foldername = "/home/texasred/all_worldday/"
# and not file.startswith("mlh160121")
for file in os.listdir("/home/texasred/all_worldday/"):
    if file.startswith("mlh"):
        print(file)
        #import data
        real_alt = np.array([])
        real_lat = np.array([])
        real_lon = np.array([])
        real_year = np.array([])
        real_month = np.array([])
        real_day = np.array([])
        real_hour = np.array([])
        real_minute = np.array([])
        real_second = np.array([])
        real_kp = np.array([])
        real_ne = np.array([])
        real_dne = np.array([])
        real_nemax = np.array([])
        real_hmax = np.array([])

        with open("/home/texasred/all_worldday/" + file) as f:
            for _ in range(1):
                next(f)
            for line in f:
                data = line.split()
                real_alt = np.append(real_alt,[float(data[6])])
                real_lat = np.append(real_lat,[float(data[7])])
                real_lon = np.append(real_lon,[float(data[8])])
                real_year = np.append(real_year,[float(data[0])])
                real_month = np.append(real_month,[float(data[1])])
                real_day = np.append(real_day,[float(data[2])])
                real_hour = np.append(real_hour,[float(data[3])])
                real_minute = np.append(real_minute,[float(data[4])])
                real_second = np.append(real_second,[float(data[5])])
                real_kp = np.append(real_kp,[float(data[9])])
                real_ne = np.append(real_ne,[float(data[10])])
                real_dne = np.append(real_dne,[float(data[11])])
                #real_nemax = np.append(real_nemax,[float(data[12])])
                #real_hmax = np.append(real_hmax,[float(data[14])])

        parameters = np.array([real_year,real_month,real_day,real_hour,real_minute,real_second,real_lat,real_lon,real_kp,real_ne,real_dne,real_alt]).T

        #find runs of data where the time is the same
        runs_kp = []
        runs_dates = []
        runs_alt = []
        runs_ne = []
        runs_dne = []
        current_run_dne = np.array([])
        current_run_ne = np.array([])
        current_run_alt = np.array([])

        prev = parameters[0]

        for p in parameters:
            if p[6] == 42.62 and p[7] == 288.51:
                if not np.array_equal(p[0:5],prev[0:5]):
                    runs_kp.append(prev[8])
                    runs_dates.append((prev[0],prev[1],prev[2],prev[3],prev[4],prev[5]))

                    runs_ne.append(current_run_ne)
                    current_run_ne = np.array([])

                    runs_dne.append(current_run_dne)
                    current_run_dne = np.array([])

                    runs_alt.append(current_run_alt)
                    current_run_alt = np.array([])
                if not math.isnan(p[9]):
                    current_run_dne = np.append(current_run_dne,p[10])
                    current_run_ne = np.append(current_run_ne,p[9])
                    current_run_alt = np.append(current_run_alt,p[11])
            prev = p


        # print(("Year","Month","Day","Hour","Minute","Second"),"Kp","Data Points")
        # for  i,(date_time, kp,alt) in enumerate(zip(runs_dates, runs_kp,runs_alt)):
        #     print(i,date_time, kp, alt.shape)
        #
        # run_id =  int(input("Pick a Run:"))
        r = list(range(0, len(runs_dates)))
        random.shuffle(r)
        rlist = r[0:5]
        #overflow problem
        #range(0, len(runs_dates))
        #range(0, len(runs_dates) - 1)
        for run_id in rlist:
            print(run_id)
            year = int(runs_dates[run_id][0])
            month = int(runs_dates[run_id][1])
            day = int(runs_dates[run_id][2])
            hour = int(runs_dates[run_id][3])
            minute = int(runs_dates[run_id][4])
            second = int(runs_dates[run_id][5])

            kp = runs_kp[run_id]
            # if (kp < 5):
            #     continue

            xpoints = models.getECHAIMProfile(42.62,288.51,year,month,day,hour,minute,second)
            xpoints2 = models.getIRI2016Profile(42.62,288.51,year,month*100 + day,hour + (minute/60.0))
            hourtime = hour + (minute/60.0)

            ypoints = np.arange(60,560,1)

            #truncate altitudes to get rid of noisy bottom end
            #start data at 150
            target_altcutoff_ne = np.array([])
            target_altcutoff_alts = np.array([])
            predictions_iri = np.array([])
            predictions_echaim = np.array([])

            for i,alt in enumerate(runs_alt[run_id]):
                if alt >= 150:
                    target_altcutoff_ne = np.append(target_altcutoff_ne,runs_ne[run_id][i])
                    target_altcutoff_alts = np.append(target_altcutoff_alts,alt)

            for alt in target_altcutoff_alts:
                if len(ypoints) == len(xpoints2) and len(ypoints) == len(xpoints):
                    predictions_iri = np.append(predictions_iri,np.interp(alt,ypoints,xpoints2))
                    predictions_echaim = np.append(predictions_echaim,np.interp(alt,ypoints,xpoints))

            if (predictions_iri.shape == target_altcutoff_ne.shape and predictions_echaim.shape == target_altcutoff_ne.shape):
                if (usePercentError):
                    rmse_iri = (100 * np.abs(predictions_iri-target_altcutoff_ne) / target_altcutoff_ne).mean() # c1 is the reference
                    rmse_echaim = (100 * np.abs(predictions_echaim-target_altcutoff_ne) / target_altcutoff_ne).mean() # c1 is the reference
                    # rmse_iri = (predictions_iri != target_altcutoff_ne).sum()/float(predictions_iri.size)
                    # rmse_echaim = (predictions_echaim != target_altcutoff_ne).sum()/float(predictions_iri.size)
                else:
                    rmse_iri = np.sqrt(((predictions_iri - target_altcutoff_ne ) ** 2).mean())
                    rmse_echaim = np.sqrt(((predictions_echaim - target_altcutoff_ne) ** 2).mean())




            errors_iri = np.append(errors_iri,rmse_iri)
            errors_echaim = np.append(errors_echaim,rmse_echaim)
            dates_x.append(datetime(year,month,day,hour,minute,second))
            kps = np.append(kps,kp)
            #print("rmse_iri " + "{:.2f}".format(rmse_iri) +" rmse echaim " + "{:.2f}".format(rmse_echaim))
            if (showplots):
                print("rmse_iri " + "{:.2f}".format(rmse_iri) +" rmse echaim " + "{:.2f}".format(rmse_echaim))

                kp = runs_kp[run_id]
                plt.plot(runs_ne[run_id], runs_alt[run_id],label = 'Millstone Hill ISR',c = 'b')
                plt.errorbar(runs_ne[run_id],runs_alt[run_id],xerr = runs_dne[run_id],c = 'b',capsize = 2)

                plt.plot(xpoints, ypoints,label = 'ECHAIM', c= 'g',linestyle = 'dotted')
                plt.plot(xpoints2, ypoints,label = 'IRI-2016', c= 'r',linestyle = 'dashed')

                plt.title("ECHAIM vs IRI-2016 at Millstone Hill " + str(year) + ' ' + str(day) + '/' + str(month) + ' ' + str(hourtime) + " Kp: " + str(kp))
                plt.xlabel("Electron Density")
                plt.ylabel("Altitude")


                plt.legend()

                plt.show()


# print(kps)
# kps = kps / kps.max()
# kps = kps * 4
# kps = kps + 36
# print(kps)


dates = matplotlib.dates.date2num(dates_x)
years = []
months = []
hours = []


for dto in dates_x:
    years.append(dto.year)
    months.append(dto.month)
    hours.append(dto.hour )#+ dto.minute/60.0

yearmax = np.max(np.array(years))
yearmin = np.min(np.array(years))

echaim_num = 0
echaim_c = 0

grid_echaim = np.zeros(shape=(12 + 1, 25)) #yearmax - yearmin + 1
count_echaim = np.zeros(shape=(12 + 1, 25))
for i, (year, month, hour,error) in enumerate(zip(years,months,hours,errors_echaim)):
    if (not math.isnan(error)):
        echaim_num = echaim_num + error
        echaim_c = echaim_c + 1
    grid_echaim[month][hour] = grid_echaim[month][hour] + error
    count_echaim[month][hour] = count_echaim[month][hour] + 1

for i, (year, month, hour,error) in enumerate(zip(years,months,hours,errors_echaim)):
    grid_echaim[month][hour] = grid_echaim[month][hour]/count_echaim[month][hour]

echaim_num = echaim_num/echaim_c
# grid_echaim = grid_echaim/np.array(3.0)

iri_num = 0
iri_c = 0

grid_iri = np.zeros(shape=(12 + 1, 25))
count_iri = np.zeros(shape=(12 + 1, 25))
for i, (year, month, hour,error) in enumerate(zip(years,months,hours,errors_iri)):
    if (not math.isnan(error)):
        iri_num = iri_num + error
        iri_c = iri_c + 1


    grid_iri[month][hour] = grid_iri[month][hour] + error
    count_iri[month][hour] = count_iri[month][hour] + 1
# grid_iri = grid_iri/np.array(3.0)
for i, (year, month, hour,error) in enumerate(zip(years,months,hours,errors_echaim)):
    grid_iri[month][hour] = grid_iri[month][hour]/count_iri[month][hour]

iri_num = iri_num/iri_c

error_min = np.nanmin(np.fmin(grid_iri , grid_echaim))
error_max = 150# np.nanmax(np.fmax(grid_iri , grid_echaim))

print(str(iri_num) + ' ' + str(echaim_num))
#print(str(error_min) + ' ' + str(error_max))
# fig = plt.figure(figsize=(8,6))
# plt.subplot(211)
# im = plt.imshow(grid_echaim)
# plt.title("Echaim Error")
#
# plt.subplot(212)
# im = plt.imshow(grid_iri)
# plt.title("IRI Error")
#
# fig.tight_layout()
#
# fig.subplots_adjust(right=0.8)
# cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
# fig.colorbar(im, cax=cbar_ax)
#
#
# plt.show()

fig, axes = plt.subplots(nrows=2, ncols=1)

im = axes.flat[0].imshow(grid_echaim,vmin = error_min,vmax =error_max)
im = axes.flat[1].imshow(grid_iri,vmin = error_min,vmax =error_max)
# for ax in axes.flat:
#     im = ax.imshow(np.random.random((10,10)), vmin=0, vmax=1)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)

plt.show()

#
#2D PLOT
#
# fig = plt.figure(1)
#
# plt.subplot(311)
# plt.scatter(hours, months, c=errors_iri,cmap = "inferno")
# # Adding title, xlabel and ylabel
# plt.title('IRI ERRORS') # Title of the plot
# plt.xlabel('Hour') # X-Label
# plt.ylabel('Month') # Y-Label
# plt.colorbar()
# # show() is used for displaying the plot
#
# plt.subplot(312)
# plt.scatter(hours, months, c=errors_echaim,cmap = "inferno")
# # Adding title, xlabel and ylabel
# plt.title('ECHAIM ERRORS') # Title of the plot
# plt.xlabel('Hour') # X-Label
# plt.ylabel('Month') # Y-Label
# plt.colorbar()
#
# plt.subplot(313)
# plt.scatter(hours, months, c=kps,cmap = "inferno")
# # Adding title, xlabel and ylabel
# plt.title('Kp Index') # Title of the plot
# plt.xlabel('Hour') # X-Label
# plt.ylabel('Month') # Y-Label
# plt.colorbar()
# # show() is used for displaying the plot
# fig.tight_layout()
# plt.show()

#
#ERROR GRAPH
#

#
# dates_idx = np.argsort(dates)
# dates_sorted = dates[dates_idx]
# errors_iri_sorted = errors_iri[dates_idx]
# errors_echaim_sorted = errors_echaim[dates_idx]
#
#
#
# #error by altitude slice
# #seasonal plot
#
# plt.title("Error OF IRI-2016 vs ECHAIM")
# plt.plot_date(dates_sorted, errors_iri_sorted,label = 'IRI-2016')
# plt.plot_date(dates_sorted, errors_echaim_sorted,label = 'ECHAIM')
# plt.xlabel("Time Of Day")
# plt.ylabel("RMS Error")
# plt.legend()
# plt.show()

#
#PLAIN PLOT
#

# print("rmse_iri " + "{:e}".format(rmse_iri) +" rmse echaim " + "{:e}".format(rmse_echaim))
#
# kp = runs_kp[run_id]
# plt.plot(runs_ne[run_id], runs_alt[run_id],label = 'Millstone Hill ISR',c = 'b')
# plt.errorbar(runs_ne[run_id],runs_alt[run_id],xerr = runs_dne[run_id],c = 'b',capsize = 2)
#
# plt.plot(xpoints, ypoints,label = 'ECHAIM', c= 'g',linestyle = 'dotted')
# plt.plot(xpoints2, ypoints,label = 'IRI-2016', c= 'r',linestyle = 'dashed')
#
# plt.title("ECHAIM vs IRI-2016 at Millstone Hill " + str(year) + ' ' + str(day) + '/' + str(month) + ' ' + str(hourtime) + " Kp: " + str(kp))
# plt.xlabel("Electron Density")
# plt.ylabel("Altitude")
#
#
# plt.legend()
#
# plt.show()
