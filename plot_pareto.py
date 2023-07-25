import matplotlib.pyplot as plt
import csv

f1,f2 = [],[]
with open('./paretos/domF_0.5_1_0_10__500_400_100.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        f1.append(float(row[0]))
        f2.append(float(row[1]))
        print(', '.join(row))
utop1 = min(f1)
utop2 = min(f2)
nadi1 = max(f1)
nadi2 = max(f2)
plt.rcParams.update({'font.size': 12})
fig = plt.figure(1,facecolor='none')
ax = plt.axes()
ax.set_facecolor('none')
plt.plot(f1,f2,marker='o',color='#72d9f0',fillstyle = 'none',label = 'Pareto Front',markersize=5,linewidth=2)
plt.plot(utop1,utop2,marker='*',color='#a5cf27',label = 'Utopia Point',markersize=10,linewidth=2)
plt.text(utop1+0.001,utop2+0.1,'Utopia',color='#a5cf27')
plt.plot(nadi1,nadi2,marker = 'x',color = '#ff5858',label='Nadir Point',markersize=10,linewidth=2)
plt.text(nadi1-0.015,nadi2-4,'Nadir',color = '#ff5858')
plt.legend
plt.xlabel('LCOE [$/kWh]')
plt.ylabel('Maximum Array Dimension [m]')

plt.show()
