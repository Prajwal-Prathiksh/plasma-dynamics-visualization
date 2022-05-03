def main():

    import numpy as np
    from mayavi import mlab
    from traits.api import HasTraits, Range, Instance, observe, Enum, Bool, Int
    from traitsui.api import View, Item, Group, HSplit
    from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
    import time
    
    

    class GUI(HasTraits):
        Data = Range(1, 1000, 1, mode='slider')
        Elevation = Range(0, 360, 240)
        Projection = Enum('Polar x-y', 'Cartesian r-theta', 'Both')
        Filters = Enum('Ion Density', 'Electron Density','Potential',
                       'Both Densities', 'Electric Field')
        Movie = Bool(False)
        Colorbar = Bool(False)
        Title = Bool(True)
        scene = Instance(MlabSceneModel, ())

        @observe(
            'Data,Elevation,Filters,Projection,Movie,Colorbar,Title,scene.activated'
            )
        def Plots(self, event=None):

            i = self.Data
            data = np.load(f'./data/_processed_data/rth_Benchmark_{i:04}.npz')
            x=np.reshape(data['x'],(129,257))
            y=np.reshape(data['y'],(129,257))
            z=np.zeros(np.shape(y))
            t=data['t']
            den1=np.reshape(data['den1'],(129,257))
            den2=np.reshape(data['den2'],(129,257))
            phi=np.reshape(data['phi'],(129,257))
            ext1 = (-1.2,-0.2,0.5,1.5,0,0.5)
            ext2 = (0.2,1.2,0,2,0,0.5)
            ext3 = (-1.2,-0.2,0.5,1.5,0,0)
            ext4 = (0.2,1.2,0,2,0,0)
            self.scene.mlab.view(45.0,54.735610317245346,561.0808549293772,
                                 np.array([-0.5, -0.5, 24.66550064]))
            if self.Projection == 'Polar x-y':
                if self.Filters == 'Potential':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x,y,phi/1000,opacity=0.95, reset_zoom = False )
                    self.scene.parallel_projection = True
                if self.Filters == 'Electron Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x,y,den1/1e16,opacity=0.95)
                    self.scene.mlab.mesh(x,y,z,color=(0,0,0))
                    self.scene.parallel_projection = True
                if self.Filters == 'Ion Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x,y,den2/3e15,opacity=0.95)
                    self.scene.mlab.mesh(x,y,z,color=(0,0,0))
                    self.scene.parallel_projection = True
                if self.Filters == 'Both Densities':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x,y,den1/1e16,opacity=0.8,color=(0,0,1))
                    self.scene.mlab.mesh(x,y,den2/3e15,opacity=0.8,color=(1,0,0))
                    self.scene.mlab.mesh(x,y,z,color=(0,0,0))
                    self.scene.parallel_projection = True

            
            if self.Projection == 'Cartesian r-theta':
                if self.Filters == 'Potential':
                    self.scene.mlab.clf()
                    self.scene.mlab.surf(phi,opacity=0.95, reset_zoom = False )
                    self.scene.parallel_projection = True
                if self.Filters == 'Electron Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.surf(den1/3e12,opacity=0.95)
                    self.scene.mlab.surf(z,color=(0,0,0))
                    self.scene.parallel_projection = True
                if self.Filters == 'Ion Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.surf(den2/3e11,opacity=0.95)
                    self.scene.mlab.surf(z,color=(0,0,0))
                    self.scene.parallel_projection = True
                if self.Filters == 'Both Densities':
                    self.scene.mlab.clf()
                    self.scene.mlab.surf(den1/3e12,opacity=0.8, color = (0,0,1))
                    self.scene.mlab.surf(den2/3e11,opacity=0.8,color = (1,0,0))
                    self.scene.mlab.surf(z,color=(0,0,0))
                    self.scene.parallel_projection = True
                    
            
                    
            if self.Projection == 'Both':
                if self.Filters == 'Potential':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x,y,phi/1000,opacity=0.95, extent = ext1)
                    self.scene.mlab.surf(phi,opacity=0.95, extent = ext2)
                    self.scene.parallel_projection = True
                if self.Filters == 'Electron Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x,y,den1/3e15,opacity=0.95, extent = ext1)
                    self.scene.mlab.mesh(x,y,z,color=(0,0,0), extent = ext3)
                    self.scene.mlab.surf(den1/3e12,opacity=0.95, extent = ext2)
                    self.scene.mlab.surf(z,color=(0,0,0), extent = ext4)
                    self.scene.parallel_projection = True
                if self.Filters == 'Ion Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x,y,den2/3e15,opacity=0.95, extent=ext1)
                    self.scene.mlab.mesh(x,y,z,color=(0,0,0), extent=ext3)
                    self.scene.mlab.surf(den2/3e11,opacity=0.95, extent=ext2)
                    self.scene.mlab.surf(z,color=(0,0,0), extent=ext4)
                    self.scene.parallel_projection = True
                if self.Filters == 'Both Densities':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x,y,den1/1e16,opacity=0.8,color=(0,0,1),extent = ext1)
                    self.scene.mlab.mesh(x,y,den2/3e15,opacity=0.8,color=(1,0,0), extent = ext1)
                    self.scene.mlab.surf(den1/3e12,opacity=0.8, color = (0,0,1), extent = ext2)
                    self.scene.mlab.surf(den2/3e11,opacity=0.8,color = (1,0,0), extent=ext2)
                    self.scene.mlab.mesh(x,y,z,color=(0,0,0), extent=ext3)
                    self.scene.mlab.surf(z,color=(0,0,0), extent=ext4)
                    self.scene.parallel_projection = True
                


            # if self.Filters == 'Streamlines':
            #     self.scene.mlab.clf()
            #     extgrd = self.scene.mlab.pipeline.extract_grid(src)
            #     self.scene.mlab.pipeline.outline(extgrd)
            #     iso = self.scene.mlab.pipeline.iso_surface(extgrd)
            #     iso.contour.auto_contours = False
            #     iso.actor.property.opacity = 0.8
            #     str = self.scene.mlab.pipeline.streamline(extgrd)
            #     str.stream_tracer.integration_direction = 'both'
    

            # if self.Filters == 'Vectors':
            #     self.scene.mlab.clf()
            #     extgrd = self.scene.mlab.pipeline.extract_grid(src)
            #     extgrd1 = self.scene.mlab.pipeline.extract_vector_components(
            #         src
            #         )
            #     self.scene.mlab.pipeline.outline(extgrd1)
            #     iso = self.scene.mlab.pipeline.iso_surface(extgrd)
            #     iso.contour.auto_contours = False
            #     iso.actor.property.opacity = 0.8
            #     self.scene.mlab.pipeline.vectors(extgrd1)
            #     if self.Colorbar:
            #         self.scene.mlab.vectorbar()

            # if self.Filters == 'Vorticity':
            #     self.scene.mlab.clf()
            #     extgrd = self.scene.mlab.pipeline.vorticity(src)
            #     self.scene.mlab.pipeline.vectors(extgrd)
            #     self.scene.mlab.pipeline.outline(extgrd)
            #     if self.Colorbar:
            #         self.scene.mlab.vectorbar()

            if self.Colorbar:
                self.scene.mlab.colorbar()

            if self.Title:
                self.scene.mlab.title(self.Filters + ' - Time:' + str(t) + 's', size=0.5,
                                      height=0.8)
            
        
        
            
        view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                         height=800, width=1500, show_label=False),
                    HSplit(Group(Item('Data'), Item('Movie')),
                           Group(Item('Projection'),Item('Filters')),
                           Group(Item('Colorbar',
                                      enabled_when='Filters in \
                                          ["Ion Density","Electron Density",\
                                           "Potential"]'),
                                 Item('Title'))),
                    resizable=True,)

    GUI().configure_traits()


if __name__ == '__main__':

    main()
