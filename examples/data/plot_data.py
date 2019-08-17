from __future__ import print_function
import sys
import json
import matplotlib.pyplot as plt

filename = sys.argv[1]
while True:
    trap_list = []
    letter = raw_input("Enter a trap letter to analyze: ")
    trap_list.append('trap_'+letter)
    while True:
        letter = raw_input("Enter another trap letter to analyze, or enter 'go' to start batch analysis: ")
        if letter == 'go':
            break
        else:
            trap_list.append('trap_'+letter)
    print ('')
    print ('you said you want to analyze: ')
    for an_trap in trap_list:
        print (an_trap)
    user_go_ahead = raw_input("Are those the traps you'd like to analyze? (y/n) ")
    if user_go_ahead == 'y':
        break
    if user_go_ahead == 'n':
        continue


with open(filename,'r') as f:

    data = json.load(f)


# for k in data:
#     print(k)
# print()

#trap_list = data.keys()
#trap_list = ['trap_{}'.format(x) for x in ['F', 'G', 'H']]
# trap_list = ['trap_C']

for i, trap in enumerate(trap_list):

    trap_data = data[trap]

    for k,v in trap_data.items():
        print(k)
    print()

    t = trap_data['seconds since release:']
    o_array = trap_data['flies on trap over time:']
    v_array = trap_data['flies in trap over time:']

    plt.figure(i+1)
    plt.subplot(2,1,1)
    plt.plot(t,o_array)
    plt.grid('on')
    plt.ylabel('on trap')

    plt.subplot(2,1,2)
    plt.plot(t,v_array)
    plt.grid('on')
    plt.ylabel('in trap vis')
    plt.xlabel('t (sec)')

plt.show()
