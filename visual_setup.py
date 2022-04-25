def main():

    import numpy as np
    from mayavi import mlab
    import time

    #mlab.figure(size=(1200, 900))
    
    i=19
    mlab.clf()
    data = np.load(f'./data/_processed_data/rth_Benchmark_{i+1:02}.npz')
    x=np.reshape(data['x'],(129,257))
    y=np.reshape(data['y'],(129,257))
    den=np.reshape(data['den1'],(129,257))
    phi=np.reshape(data['phi'],(129,257))


    #s = mlab.mesh(x,y,den/(1e16))
    w = mlab.mesh(x,y,phi/1000)
    mlab.orientation_axes()
    mlab.title('Ion Density', size=0.2,
                height=0.95)
    mlab.show()
if __name__ == '__main__':

    main()