import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from matplotlib import cm


class capacitor_rectangle:
    def __init__(self,x_length,y_length,realism=False):
        self.x_length=int(x_length)
        self.y_length=int(y_length)
        self.realism=realism
        grid_increase=10
        self.grid_increase=grid_increase
        if realism:
            self.SQUARE_GRID=np.zeros((x_length+x_length*grid_increase,y_length+y_length*grid_increase))
            #the grid is inside other larger grid because the Contour
        else:            
            self.SQUARE_GRID=np.zeros((x_length+2,y_length+2))
            #the grid is inside other larger grid because the Contour
        
    def contour(self,x_bottom,x_top,y_bottom,y_top):
        self.x_bottom=x_bottom
        self.x_top=x_top
        self.y_bottom=y_bottom
        self.y_top=y_top
        if x_bottom.shape[0]!=self.x_length or x_top.shape[0]!=self.x_length:
            print('ERRO -- X contour size does not match')
            
        if y_bottom.shape[0]!=self.y_length or y_top.shape[0]!=self.y_length:
            print('ERRO -- Y contour size does not match')

        if self.realism:
            x_length=self.x_length
            y_length=self.y_length
            coordinate_small_grid=[int(x_length*10/2)-1,int(x_length*10/2)+x_length-1,int(y_length*10/2)-1,int(y_length*10/2)+y_length-1]#x_inf,x_sup,y_inf,y_sup --- if the small box has dimension of 10 X 10, then the real grid has 100 X 100, So the small grid has vertice coordinates [50,50],[60,50],[60,60],[50,60], or in numpy arrays
            SQUARE_GRID=self.SQUARE_GRID
            SQUARE_GRID[coordinate_small_grid[0]:coordinate_small_grid[1],coordinate_small_grid[2]-1]=self.x_bottom
            SQUARE_GRID[coordinate_small_grid[0]:coordinate_small_grid[1],coordinate_small_grid[3]]=self.x_top
            SQUARE_GRID[coordinate_small_grid[0]-1,coordinate_small_grid[2]:coordinate_small_grid[3]]=self.y_bottom
            SQUARE_GRID[coordinate_small_grid[1],coordinate_small_grid[2]:coordinate_small_grid[3]]=self.y_top
        else:
            SQUARE_GRID=self.SQUARE_GRID
            SQUARE_GRID[1:-1,0]=self.x_bottom
            SQUARE_GRID[1:-1,-1]=self.x_top
            SQUARE_GRID[0,1:-1]=self.y_bottom
            SQUARE_GRID[-1,1:-1]=self.y_top
        self.contour_nonzero=np.nonzero(SQUARE_GRID)

    def run(self,rounds=False,precision=False):
        SQUARE_GRID=np.array(self.SQUARE_GRID)
        if not precision:
            result=self.iterate_rounds(rounds,SQUARE_GRID)
            self.result=result
            return result
            pass
        if not rounds:
            result=self.iterate_precision(precision,SQUARE_GRID)
            self.result=result
            return result
            

       
    def iterate_rounds(self,rounds,vector1):
        x_length=self.x_length
        y_length=self.y_length

        if self.realism:
            x_length=x_length*self.grid_increase
            y_length=y_length*self.grid_increase

        for z in range(0,rounds):
            GRID=np.array(vector1)
            for k in range(x_length*y_length):                                
                i=k%x_length+1
                j=int(k/x_length)+1
                
                vector1[i,j]=0.25*(GRID[i+1,j]+GRID[i-1,j]+GRID[i,j-1]+GRID[i,j+1])
            vector1[self.contour_nonzero]=self.SQUARE_GRID[self.contour_nonzero]

        
        return vector1


    def iterate_precision(self,precision,vector1):
        x_length=self.x_length
        y_length=self.y_length

        if self.realism:
            x_length=x_length*self.grid_increase
            y_length=y_length*self.grid_increase

        iteration=0
        while(iteration<5 or np.fabs(np.trace(vector1)-np.trace(GRID))>precision): 
            GRID=np.array(vector1)  
            for k in range(x_length*y_length):                
                i=k%x_length+1
                j=int(k/x_length)+1
                vector1[i,j]=0.25*(GRID[i+1,j]+GRID[i-1,j]+GRID[i,j-1]+GRID[i,j+1])
            vector1[self.contour_nonzero]=self.SQUARE_GRID[self.contour_nonzero]

            iteration+=1
        print(str(iteration)+' iterations')
        return vector1

    def plot3d(self,data=False,save_image=False,dpi=300,name='3d_laplace_equation_capacitor.jpg'):
        if not data:
            data=self.result
        fig = plt.figure(figsize=(8,6))
        ax = plt.subplot(111, projection='3d')
        ax.xaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('white')
        ax.yaxis.pane.fill = False
        ax.yaxis.pane.set_edgecolor('white')
        ax.zaxis.pane.fill = False
        ax.zaxis.pane.set_edgecolor('white')
        ax.grid(False)
        X, Y = np.meshgrid(np.linspace(0,self.x_length , len(data)), np.linspace(0, self.y_length, len(data)))
        plot = ax.plot_surface(X=X, Y=Y, Z=data, cmap='YlGnBu_r', vmin=round(data.min()/10)*10, vmax=round(data.max()/10)*10)
        cbar = fig.colorbar(plot, ax=ax, shrink=0.6)


        if save_image:
            plt.savefig(name,dpi=dpi)


    def plot2d(self,data=False,save_image=False,dpi=300,name='2d_laplace_equation_capacitor.jpg'):
        if not data:
            data=self.result
        plt.imshow(data,cmap=plt.cm.Greys)
        plt.colorbar()
        plt.grid(True)
        if save_image:
            plt.savefig(name,dpi=dpi)
    
    def dataframe(self,name):

        df=pd.DataFrame(self.result)
        df.to_csv(name+'.csv')
        return 'csv file saved'

