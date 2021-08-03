
def MakeCSV(original):
    
    #opening the original file    
    file = open(original,'r')
    
    #searching for the line containing '2Theta position' or '2theta'    
    search1 = '2Theta position'
    search2 = '2theta'
    search3 = 'Angle'
    search4 = 'Column 0'
    i=0
    for i in range(100):
        line = file.readline()
        line.split(',')
        if search1 in line:
            s1 = line[0:7]
            break
        elif search2 in line:
            s1 = line[0:7]
            break
        elif search3 in line:
            s1 = line[0:7]
            break
        elif search4 in line:
            s1 = line[0:7]
            break
        else:
            i+=1
    
    #reading the table with the data (after the line containing '2Theta position')
    f = file.readlines()
    
    #defining the head of the new file
    if 'heta' in s1:
        head = '2theta,omega,intensity\n'
    elif 'mega' in s1:
        head = 'omega,2theta,intensity\n'
    elif 'ngle' in s1:
        head = 'Angle,intensity\n'
    elif 'Column' in s1:
        head = 'Angle,intensity\n'
    
    #opening a new file for writting
    temp = original+'-temp'        
    file2 = open(temp,'w')
    
    #writting the head + data on the new file
    file2.writelines(head)
    file2.writelines(f)
    
    #closing all the files
    file.close()          
    file2.close()


def RSMplot(arquivo,xmin=1,xmax=1,ymin=1,ymax=1,zmin=1,zmax=1,levels=100,wavelenght=1.5406,color='rainbow'):
    
    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import ticker
    #%matplotlib inline
    #%pylab
    
    MakeCSV(arquivo)
    temp = arquivo+'-temp'
    
    #importing the data and defining arrays (already in radians)
    
    data = pd.read_csv(temp)
    
    omg = (np.pi/180) * np.array(data['omega'])
    tth = (np.pi/180) * np.array(data['2theta'])
    phi = 0
    chi = 0
    cts = np.array(data['intensity'])
    
    #Transforming from angles to reciprocal space coordinates
    
    lb = wavelenght
    th = tth/2
    
    q = (4*np.pi*np.sin(th))/lb
    
    Qx =  q * ( np.sin(omg-th)*np.cos(phi) - np.cos(omg-th)*np.sin(chi)*np.sin(phi) )
    Qy = -q * ( np.sin(omg-th)*np.sin(phi) + np.cos(omg-th)*np.sin(chi)*np.cos(phi) ) 
    Qz =  q * np.cos(omg-th)*np.cos(chi) 
    
    #finding out the number of rows and columns for the grid
    
    t = np.array(data['2theta'])
    i = 0
    vi = t[i]
    
    for i, v in enumerate(t):   
        if v==vi:
            if i>2:
                c=i
                break
        else:
            i+=1
            
    r = len(Qx)//(c) #'//' em vez de '/' é para resultar num inteiro
    
    #defining new arrays with the correct shape (rows,columns)
    
    Qx = np.reshape(Qx,(r,c))
    Qy = np.reshape(Qy,(r,c))
    Qz = np.reshape(Qz,(r,c))
    cts = np.reshape(cts,(r,c))
    
    #defining the levels' scale for the plot
    
    lmin = np.log10(zmin)
        
    if zmax==1:
        lmax = np.log10(np.amax(cts))
    else:
        lmax = np.log10(zmax)
        
    nl = levels 
        
    alevels = np.logspace(lmin,lmax,nl,base=10)
    
    #defininf x and y axis for the plot

    if xmin==1:
        x_i = np.amin(Qx)
    else:
        x_i = xmin
        
    if xmax==1:
        x_f = np.amax(Qx)
    else:
        x_f = xmax
        
    if ymin==1:
        y_i = np.amin(Qz)
    else:
        y_i = ymin
        
    if ymax==1:
        y_f = np.amax(Qz)
    else:
        y_f = ymax
   
    #plotting the data
    
    plt.contourf(Qx, Qz, cts, locator=ticker.LogLocator(), levels=alevels , cmap=color)
    
    plt.title(arquivo, fontsize=13)
    plt.ylabel('Qz (1/Â)')
    plt.xlabel('Qx (1/Â)')
    plt.axis([x_i,x_f,y_i,y_f])
    plt.grid(True)
    
    plt.colorbar(label='counts', ticks=[])
    
    #deleting the temporary file
    
    os.remove(temp)
    
    
def TH2THplot(arquivo,xmin=1,xmax=1,ymin=1,ymax=1,yscale='log',wavelenght=1.5406,space=1):

    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
        
    #Making temporary file and importing the data and defining reciprocal space array
    
    MakeCSV(arquivo)
    temp = arquivo+'-temp'  
    
    data = pd.read_csv(temp)  
   
    tth = np.array(data['Angle'])
    cts = np.array(data['intensity'])
    
    tth_rad = (np.pi/180) * np.array(data['Angle'])
    d = (1/2)*wavelenght/np.sin(tth_rad/2)
      
    #defininf x and y axis for the plot

    if space == -1:
        xaxis = d
    else:
        xaxis = tth
    
    if xmin==1:
        x_i = np.amin(xaxis)
    else:
        x_i = xmin
        
    if xmax==1:
        x_f = np.amax(xaxis)
    else:
        x_f = xmax
        
    if ymin==1:
        y_i = 0.1
    else:
        y_i = ymin
        
    if ymax==1:
        y_f = np.amax(cts)
    else:
        y_f = ymax
        
    if space == -1:
        plt.xlabel('d (Â)')
        plt.axis([x_f,x_i,y_i,y_f])
    else:
        plt.xlabel('2theta (deg)')
        plt.axis([x_i,x_f,y_i,y_f])
              
    plt.plot(xaxis, cts)
    plt.title(arquivo, fontsize=13)
    plt.ylabel("counts (a.u.)")
    plt.yscale(yscale) 
    plt.grid(True)
    plt.show()
    
    os.remove(temp)
    
    
def OMGplot(arquivo,xmin=1,xmax=1,ymin=1,ymax=1,yscale='log'):

    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
        
    #Making temporary file and importing the data and defining reciprocal space array
    
    MakeCSV(arquivo)
    temp = arquivo+'-temp'  
    
    data = pd.read_csv(temp)  
   
    omg = np.array(data['Angle'])
    cts = np.array(data['intensity'])
      
    #defininf x and y axis for the plot
    
    if xmin==1:
        x_i = np.amin(omg)
    else:
        x_i = xmin
        
    if xmax==1:
        x_f = np.amax(omg)
    else:
        x_f = xmax
        
    if ymin==1:
        y_i = 0.1
    else:
        y_i = ymin
        
    if ymax==1:
        y_f = np.amax(cts)
    else:
        y_f = ymax
        

    plt.xlabel('omega (deg)')
    plt.axis([x_i,x_f,y_i,y_f])
              
    plt.plot(omg, cts)
    plt.title(arquivo, fontsize=13)
    plt.ylabel("counts (a.u.)")
    plt.yscale(yscale) 
    plt.grid(True)
    plt.show()
    
    os.remove(temp)    
    