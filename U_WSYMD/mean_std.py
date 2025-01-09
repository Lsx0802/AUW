# coding=utf-8
import  numpy as np

###
a=[0.704,0.658,0.728,0.774,0.713]
b=[0.719,0.666,0.758,0.777,0.756]
c=[	0.748,0.666,0.684,0.811,0.761]
d=[0.716,0.655,0.708,0.783,0.743]
###
print("{:.4f} +- {:.4f}".format(np.mean(a),np.std(a, ddof = 1)))
print("{:.4f} +- {:.4f}".format(np.mean(b),np.std(b, ddof = 1)))
print("{:.4f} +- {:.4f}".format(np.mean(c),np.std(c, ddof = 1)))
print("{:.4f} +- {:.4f}".format(np.mean(d),np.std(d, ddof = 1)))



