import numpy as np
import scipy.stats 

def mvlr(dep_var,ind_var,alpha):
    # gets data size paremeters 
    shape = np.shape(ind_var)
    W = shape[1]
    D = shape[0]
    xty = []

    # populats xtx  and xty matrices for coeffecient calculations
    for i in range(0,W+1): # for each row
        # initializes needed empty variables to be later populated
        row = []
        xty_i = 0
        for j in range(0,W+1): # for each column
            x = 0
            if i == 0: # top row of xtx
                if j == 0: # first xtx element
                    x = D
                else: 
                    x = sum(ind_var[:,j-1])
            else:
                if j == 0: # first column of xtx matrix
                    x = sum(ind_var[:,i-1])
                else:
                    for k in range(0,D): # every other element
                        x = x + ind_var[k][i-1]*ind_var[k][j-1]
            row = np.append(row,x)

        if i == 0:
            xty_i = sum(dep_var) # first xty element
            xtx = row # first row of xtx
        else: 
            for k in range(0,D):
                xty_i = xty_i + dep_var[k]*ind_var[k][i-1] # rest of xty 
            xtx = np.vstack((xtx,row)) # builds xtx 
        xty = np.append(xty,xty_i)

    # handles matrix algebra for coeffecients 
    xtx_inv = np.linalg.inv(xtx)
    coeff = np.dot(xty,xtx_inv)


    # this half handles confidence interval for coeffecients
    for i in range(0,D): # populates 'x' matrix for error calculation
        x_err_row = []
        for j in range(0,len(coeff)):
            if j == 0:
                x_err_ij = 1
            else: 
                x_err_ij = ind_var[i][j-1]
            x_err_row = np.append(x_err_row,x_err_ij)
        if i == 0:
            x_err = x_err_row
        else:
            x_err = np.vstack((x_err,x_err_row))
        
    err = dep_var - np.dot(x_err,coeff) 
        # starts SSE calculation
    SSE = 0
    for i in range(0,D):
        SSE = SSE + np.power(err[i],2)

    S = np.power(SSE/(D - (W + 1)),0.5)
    t = scipy.stats.t.ppf(1-alpha/2,D-W)
    MoE = []
    for i in range(0,len(coeff)):
        MoE = np.append(MoE,t*S*np.power(xtx_inv[i][i],0.5)) # ith diagnal element of xtx inv is Cii
        # uses S,C, and values to find confidence interval
    
    # final output
    coeff = np.reshape(coeff,(len(coeff),1))
    MoE = np.reshape(MoE,(len(MoE),1))

        # R squared calculation
    y_bar = np.average(dep_var)
    SSM = 0

    for i in range(0,D):
        SSM = SSM + np.power(dep_var[i]-y_bar,2) # sum of squares total
    
    Rsqr = 1 - SSE/SSM
    
        # F calculation
    pfit = len(coeff)
    F = ((SSM-SSE)/(pfit-1))/(SSE/(D-pfit))
    err_stats = [['RS:',Rsqr],
                 ['F:',F]]


    return [np.append(coeff,MoE,1),err_stats]

y = [21,21,22.8,21.4,18.7,18.1]
cyl = [6,6,4,6,8,6]
