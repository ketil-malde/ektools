#!/usr/bin/python3
# Usage: python3 eklist.py -r ../ekdata/2014813-D20180628-T202307.raw| python3 corrplot.py
# TODO: eklist output TS instead of Sv - filter?

from rawdecode import unpickle_iter

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def corrdot(*args, **kwargs):
    corr_r = args[0].corr(args[1], 'pearson')
    corr_text = f"{corr_r:2.2f}".replace("0.", ".")
    ax = plt.gca()
    ax.set_axis_off()
    marker_size = abs(corr_r) * 10000
    ax.scatter([.5], [.5], marker_size, [corr_r], alpha=0.6, cmap="coolwarm",
               vmin=-1, vmax=1, transform=ax.transAxes)
    font_size = abs(corr_r) * 40 + 5
    ax.annotate(corr_text, [.5, .5,],  xycoords="axes fraction",
                ha='center', va='center', fontsize=font_size)

# sns.set(style='white', font_scale=1.6)

for r in unpickle_iter():
    pingdata = {}
    for datetime, freqs in r.items():
        print(datetime,freqs.keys())
        for fq,v in freqs.items():
            f = str(fq)
            l = len(v['range'])
            if l not in pingdata.keys():
                pingdata[l] = {}
            if f not in pingdata[l].keys():
#                pingdata[l][f+'range'] = np.empty(0)
                pingdata[l][f+'alpha'] = np.empty(0)
                pingdata[l][f+'beta'] = np.empty(0)
                pingdata[l][f] = np.empty(0)

            cutoff=30

            x = np.log(v['s_v']) # v['angles'][:,0]
            pingdata[l][f]    = np.append(pingdata[l][f], x[cutoff:])
#            pingdata[l][f+'range'] = np.append(pingdata[l][f+'range'], v['range'])
            pingdata[l][f+'alpha'] = np.append(pingdata[l][f+'alpha'], v['angles'][cutoff:,0])
            pingdata[l][f+'beta']  = np.append(pingdata[l][f+'beta'], v['angles'][cutoff:,1])

    print(pingdata.keys())
    for l in pingdata.keys():
        # try to filter on average sv value
        num = 0
        sumsv = np.zeros(l-30)
        for fq in pingdata[l]:
            if fq[-1] == 'a':  # avoid angles
                continue
            num +=1
            sumsv = sumsv + pingdata[l][fq]
        filterx = sumsv/num > -15
        p = {}
        for fq in pingdata[l]:
            p[fq] = pingdata[l][fq][filterx]
            print('len before:', len(pingdata[l][fq]), ' len after:', len(p[fq]))

        ping = pd.DataFrame.from_records(p)
        print(ping)
        g = sns.PairGrid(ping, aspect=1.4, diag_sharey=False)
        g.map_lower(sns.regplot, lowess=True, ci=False, line_kws={'color': 'black'}, marker='.', scatter_kws={'s':2})
        g.map_diag(sns.histplot, kde_kws={'color': 'black'})
        g.map_upper(corrdot)
        plt.show()

