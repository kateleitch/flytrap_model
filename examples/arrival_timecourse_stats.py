# generating statistical summaries of arrival timecourses, e.g. cross-correlation between timecourses generated from the same data, different machine-vision parameters
from __future__ import print_function
import numpy as np
import flytrap_model
import matplotlib.pyplot as plt
import json
from pylab import *
from scipy.optimize import curve_fit

dirname1 = './data/2019_05_08_experiment_1'
dirname2 = './data/2019_05_08_experiment_2'
dirname3 = './data/2019_05_08_experiment_3'
dirname4 = './data/2017_04_30_experiment'

def adjust_spines(ax_handle, spines):
    ax_handle.tick_params(direction='out')
    for loc, spine in ax_handle.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))  # outward by 10 points
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine
    # turn off ticks where there is no spine
    if 'left' in spines:
        ax_handle.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax_handle.yaxis.set_ticks([])
    if 'bottom' in spines:
        ax_handle.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax_handle.xaxis.set_ticks([])

with open(dirname1+'/unique_arrival_timecourse.json') as f:
    arrival_timecourse_1 = json.load(f)
with open(dirname2+'/unique_arrival_timecourse.json') as f:
    arrival_timecourse_2 = json.load(f)
with open(dirname3+'/unique_arrival_timecourse.json') as f:
    arrival_timecourse_3 = json.load(f)

with open(dirname4+'/unique_arrival_timecourse.json') as f:
    arrival_timecourse_4 = json.load(f)

corr  = np.correlate(arrival_timecourse_1['estimated arrival array (flies per timestep)'],arrival_timecourse_2['estimated arrival array (flies per timestep)'], "full")
corr2 = np.correlate(arrival_timecourse_1['estimated arrival array (flies per timestep)'],arrival_timecourse_3['estimated arrival array (flies per timestep)'], "full")
corr3 = np.correlate(arrival_timecourse_2['estimated arrival array (flies per timestep)'],arrival_timecourse_3['estimated arrival array (flies per timestep)'], "full")
auto_corr = np.correlate(arrival_timecourse_1['estimated arrival array (flies per timestep)'],arrival_timecourse_1['estimated arrival array (flies per timestep)'], "full")

kates_cheesy_corr_metric_1_2 = np.max(corr)/np.max(auto_corr)
kates_cheesy_corr_metric_1_3 = np.max(corr2)/np.max(auto_corr)
print (kates_cheesy_corr_metric_1_2)
print (kates_cheesy_corr_metric_1_3)

neg_control_corr = np.correlate(arrival_timecourse_1['estimated arrival array (flies per timestep)'],arrival_timecourse_4['estimated arrival array (flies per timestep)'], "full")
other_trap_auto_corr = np.correlate(arrival_timecourse_4['estimated arrival array (flies per timestep)'],arrival_timecourse_4['estimated arrival array (flies per timestep)'], "full")

################# now trying to produce some meaningful summary statistics from these arrival data:

def func(x, a, b, c, d):
    return a*np.exp(c*(x-b))+d

arrival_peak = np.max(arrival_timecourse_1['estimated arrival array (flies per timestep)'])
print (arrival_peak)
arrival_peak_index = np.where(arrival_timecourse_1['estimated arrival array (flies per timestep)'] == arrival_peak)[0][0]
print (arrival_peak_index)

popt, pcov = curve_fit(func, arrival_timecourse_1['time array'][:arrival_peak_index], arrival_timecourse_1['estimated arrival array (flies per timestep)'][0:arrival_peak_index], [0.001,30,0.02,0.02])
print (popt)
print ('pcov: ' +str(pcov))
perr = np.sqrt(np.diag(pcov))
print ('perr: ' + str(perr))
x=linspace(0,arrival_timecourse_1['time array'][arrival_peak_index],10000)

linewidth = 2
plt.figure(1)
ax = plt.subplot(111)
plt.plot(arrival_timecourse_1['time array'], arrival_timecourse_1['estimated arrival array (flies per timestep)'],'gray',linewidth=linewidth-1, label = 'analysis 1')
plt.plot(arrival_timecourse_2['time array'], arrival_timecourse_2['estimated arrival array (flies per timestep)'],'b',linewidth=linewidth-1, label = 'analysis 2 corr = %.2f' % kates_cheesy_corr_metric_1_2)
plt.plot(arrival_timecourse_3['time array'], arrival_timecourse_3['estimated arrival array (flies per timestep)'],'green',linewidth=linewidth-1, label = 'analysis 3 corr = %.2f' % kates_cheesy_corr_metric_1_3)
plt.plot(x, func(x,*popt), '--k')
plt.title('2019_05_08 trap_C system ID/Kalman arrival timecourses')
#plt.plot(arrival_timecourse_4['time array'], arrival_timecourse_4['estimated arrival array (flies per timestep)'],'c',linewidth=linewidth, label = '2017_04_30_trap_G')

plt.legend(loc =2, fontsize = 9)
plt.ylabel('arrival rate (flies/timestep)')
plt.xlabel('time since release (sec)')
adjust_spines(ax_handle = ax, spines = ['bottom','left'])
plt.tight_layout()

# ax2 = plt.subplot(212)
# plt.plot(corr,'r',linewidth=linewidth, label = '1,2 x-corr')
# plt.plot(corr2,'k',linewidth=linewidth, label = '1,3 x-corr')
# plt.plot(auto_corr,'g',linewidth=linewidth, label = '1,1 autocorr')
# #plt.plot(neg_control_corr,'c',linewidth=linewidth, label = '1, 04_30 x-corr')
# #plt.plot(other_trap_auto_corr,'m',linewidth=linewidth, label = '04_30, 04_30 x-corr')
# plt.legend(loc=2, fontsize = 9)
# # plt.plot(arrival_timecourse_2['time array'], auto_corr2,'b',linewidth=linewidth)
# adjust_spines(ax_handle = ax2, spines = ['bottom','left'])
plt.show()
