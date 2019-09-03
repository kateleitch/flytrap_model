#from __future__ import print_function
import numpy
import flytrap_model
import matplotlib.pyplot as plt
import json

dirname = './data/2019_05_08_experiment_1'
trap = 'C'

# dirname = './data/2017_10_26_experiment/'
# trap = 'F'

# dirname = './data/2017_04_30_experiment/'
# trap = 'G'

def adjust_spines(ax_handle, spines):
    ax_handle.tick_params(direction='out')
    for loc, spine in ax_handle.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))  # outward by 10 points
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine
    if 'left' in spines:
        ax_handle.yaxis.set_ticks_position('left')
    else:
        ax_handle.yaxis.set_ticks([])
    if 'bottom' in spines:
        ax_handle.xaxis.set_ticks_position('bottom')
    else:
        ax_handle.xaxis.set_ticks([])
    plt.tight_layout()
    
#model, values, variance, inputs = flytrap_model.fit_and_filter_from_dir(dirname,trap,method='sm',smooth_param=0.01)
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
ax = plt.subplot(111)
plt.plot(t_array,o_array,'k',linewidth=linewidth,label = 'on trap')
#plt.plot(t_array,o_array_est,color = [0.5,0.5,0.5]',linewidth=linewidth)
plt.fill_between(t_array,o_array_est+o_array_err,o_array_est-o_array_err,color='k',alpha=0.25)
plt.plot(t_array,h_array_est,color = [0.58, 0.91, 0.67],linewidth=linewidth,label = 'hidden')
plt.fill_between(t_array,h_array_est+h_array_err,h_array_est-h_array_err,color=[0.58, 0.91, 0.67],alpha=0.25)
plt.plot(t_array,v_array,color = [0.6,0,0.6],linewidth=linewidth, label ='visible')
#plt.plot(t_array,v_array_est,'g',linewidth=linewidth)
plt.fill_between(t_array,v_array_est+v_array_err,v_array_est-v_array_err,color = [0.6,0,0.6],alpha=0.25)
plt.xlabel('seconds since release')
plt.ylabel('on trap')
# ax.set_ylim([])
adjust_spines(ax_handle = ax, spines = ['bottom','left'])

# ax =plt.subplot(312)
# plt.plot(t_array,h_array_est,color = [0.58, 0.91, 0.67],linewidth=linewidth)
# plt.fill_between(t_array,h_array_est+h_array_err,h_array_est-h_array_err,color=[0.58, 0.91, 0.67],alpha=0.25)
# plt.ylabel('hidden')
# adjust_spines(ax_handle = ax, spines = ['bottom','left'])
#
# ax = plt.subplot(313)
# plt.plot(t_array,v_array,color = [0.6,0,0.6],linewidth=linewidth)
# #plt.plot(t_array,v_array_est,'g',linewidth=linewidth)
# plt.fill_between(t_array,v_array_est+v_array_err,v_array_est-v_array_err,color = [0.6,0,0.6],alpha=0.25)
# plt.ylabel('visible')
# plt.xlabel('t (sec)')
# adjust_spines(ax_handle = ax, spines = ['bottom','left'])

# plt.figure(2)
# ax = plt.subplot(211)
# plt.plot(t_array,a_array_est,'b',linewidth=linewidth)
# plt.ylabel('arrivals (flies/step)')
# adjust_spines(ax_handle = ax, spines = ['bottom','left'])
# ax = plt.subplot(212)
# plt.plot(t_array,acum_array_est,'b',linewidth=linewidth)
# plt.axhline(y=inputs['count_final'], color = 'k')
# plt.ylim(top=inputs['count_final']*1.1)
# plt.ylabel('cumulative arrivals')
# plt.xlabel('seconds since release)')
# adjust_spines(ax_handle = ax, spines = ['bottom','left'])

out_dictionary = {'time array': t_array.tolist(), 'estimated arrival array (flies per timestep)': a_array_est.tolist()}
with open(dirname+'/unique_arrival_timecourse.json', mode = 'w') as f:
    json.dump(out_dictionary,f, indent = 1)

plt.savefig('./data/2019_05_08_experiment_1/ontrap_intrap_hidden_analysis1.svg')
plt.show()
