from __future__ import print_function
import numpy
import flytrap_model
import matplotlib.pyplot as plt
import json

dirname = './data/2019_05_08_experiment_3'
trap = 'C'

# dirname = './data/2017_10_26_experiment/'
# trap = 'G'

dirname = './data/2017_04_30_experiment/'
trap = 'G'

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

model, values, variance, inputs = flytrap_model.fit_and_filter_from_dir(dirname,trap)

t_array = inputs['t_array']
o_array = inputs['o_array']
v_array = inputs['v_array']
a_array_est = values['a_array']
o_array_est = values['o_array']
h_array_est = values['h_array']
v_array_est = values['v_array']

print ('caught ' + str(inputs['count_final'])+' flies')

o_array_err = 1.0*numpy.sqrt(variance['o_array'])
h_array_err = 1.0*numpy.sqrt(variance['h_array'])
v_array_err = 1.0*numpy.sqrt(variance['v_array'])

acum_array_est = values['acum_array']

linewidth = 2
plt.figure(1)
ax = plt.subplot(311)
plt.plot(t_array,o_array,'b',linewidth=linewidth)
plt.plot(t_array,o_array_est,'g',linewidth=linewidth)
plt.fill_between(t_array,o_array_est+o_array_err,o_array_est-o_array_err,color='g',alpha=0.25)
plt.ylabel('on trap')
adjust_spines(ax_handle = ax, spines = ['bottom','left'])

ax =plt.subplot(312)
plt.plot(t_array,h_array_est,'g',linewidth=linewidth)
plt.fill_between(t_array,h_array_est+h_array_err,h_array_est-h_array_err,color='g',alpha=0.25)
plt.ylabel('hidden')
adjust_spines(ax_handle = ax, spines = ['bottom','left'])

ax = plt.subplot(313)
plt.plot(t_array,v_array,'b',linewidth=linewidth)
plt.plot(t_array,v_array_est,'g',linewidth=linewidth)
plt.fill_between(t_array,v_array_est+v_array_err,v_array_est-v_array_err,color='g',alpha=0.25)
plt.ylabel('visible')
plt.xlabel('t (sec)')
adjust_spines(ax_handle = ax, spines = ['bottom','left'])

plt.figure(2)
ax = plt.subplot(211)
plt.plot(t_array,a_array_est,'g',linewidth=linewidth)
plt.ylabel('arrivals (flies/step)')
adjust_spines(ax_handle = ax, spines = ['bottom','left'])
ax = plt.subplot(212)
plt.plot(t_array,acum_array_est,'g',linewidth=linewidth)
plt.axhline(y=inputs['count_final'])
plt.ylim(top=inputs['count_final']*1.1)
plt.ylabel('cumulative arrivals')
plt.xlabel('t (sec)')
adjust_spines(ax_handle = ax, spines = ['bottom','left'])

out_dictionary = {'time array': t_array.tolist(), 'estimated arrival array (flies per timestep)': a_array_est.tolist()}
with open(dirname+'/unique_arrival_timecourse.json', mode = 'w') as f:
    json.dump(out_dictionary,f, indent = 1)

plt.show()
