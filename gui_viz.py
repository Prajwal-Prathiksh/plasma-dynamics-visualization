def main():

    import numpy as np
    from mayavi import mlab
    from traits.api import HasTraits, Range, Instance, observe, Enum, Bool
    from traitsui.api import View, Item, Group, HSplit
    from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
    
    

    class GUI(HasTraits):
        Data = Range(1, 1000, 1)
        Elevation = Range(0, 360, 240)
        Filters = Enum('Potential', 'Ion Density', 'Electron Density',
                       'Vectors', 'Vorticity')
        Axes = Bool(True)
        Colorbar = Bool(True)
        Title = Bool(True)
        scene = Instance(MlabSceneModel, ())

        @observe(
            'Data,Elevation,Filters,Axes,Colorbar,Title,scene.activated'
            )
        def Plots(self, event=None):
            
            i = self.Data
            data = np.load(f'./data/_processed_data/rth_Benchmark_{i:04}.npz')
            x=np.reshape(data['x'],(129,257))
            y=np.reshape(data['y'],(129,257))
            z=np.zeros(np.shape(y))
            time=data['t']
            den1=np.reshape(data['den1'],(129,257))
            den2=np.reshape(data['den2'],(129,257))
            phi=np.reshape(data['phi'],(129,257))
            

            if self.Filters == 'Potential':
                self.scene.mlab.clf()
                self.scene.mlab.mesh(x,y,phi/1000,opacity=0.8, reset_zoom = False )
                self.scene.mlab.mesh(x,y,z,color=(0,0,0))
                self.scene.parallel_projection = True
            if self.Filters == 'Electron Density':
                self.scene.mlab.clf()
                self.scene.mlab.mesh(x,y,den1/1e16,opacity=1)
                self.scene.mlab.mesh(x,y,z,color=(0,0,0))
                self.scene.parallel_projection = True
            if self.Filters == 'Ion Density':
                self.scene.mlab.clf()
                self.scene.mlab.mesh(x,y,den2/3e15,opacity=0.95)
                self.scene.mlab.mesh(x,y,z,color=(0,0,0))
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
            #     if self.Colorbar:
            #         self.scene.mlab.colorbar()

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

            if self.Axes:
                self.scene.mlab.orientation_axes()

            if self.Title:
                self.scene.mlab.title(self.Filters + ' - Time:' + str(time) + 's', size=0.5,
                                      height=0.8)
            
            

        
            
        view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                         height=500, width=500, show_label=False),
                    HSplit(Group(Item('Data'), Item('Elevation')),
                           Group(Item('Filters'), Item('Axes')),
                           Group(Item('Colorbar',
                                      enabled_when='Filters in \
                                          ["Vorticity","Vectors",\
                                           "Streamlines"]'),
                                 Item('Title'))),
                    resizable=True,)

    GUI().configure_traits()


if __name__ == '__main__':

    main()
