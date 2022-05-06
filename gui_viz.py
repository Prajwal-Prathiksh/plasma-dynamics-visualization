def main():

    import numpy as np
    from traits.api import HasTraits, Range, Instance, observe, Enum, Bool, Str
    from traitsui.api import View, Item, Group, HSplit
    from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel

    class GUI(HasTraits):
        Iteration = Range(1, 1000, 1, mode='slider')
        Projection = Enum('Polar x-y', 'Cartesian r-theta', 'Both')
        Property = Enum('Ion Density', 'Electron Density', 'Potential',
                        'Plasma Density')
        Colorbar = Bool(True)
        Title = Bool(True)
        Details = Bool(True)
        Units = Str('')
        xaxis = Str('')
        yaxis = Str('')
        Axes = Bool(True)
        scene = Instance(MlabSceneModel, ())

        @observe(
            'Iteration,Property,Projection,Colorbar,Title,Details,Axes,\
                scene.activated'
        )
        def Plots(self, event=None):

            i = self.Iteration
            data = np.load(f'./data/_processed_data/rth_Benchmark_{i:04}.npz')
            x = np.reshape(data['x'], (129, 257))
            y = np.reshape(data['y'], (129, 257))
            z = np.zeros(np.shape(y))
            t = data['t']
            den1 = np.reshape(data['den1'], (129, 257))
            den2 = np.reshape(data['den2'], (129, 257))
            phi = np.reshape(data['phi'], (129, 257))
            ext1 = (-1.2, -0.2, 0.5, 1.5, 0, 0.5)
            ext2 = (0.2, 1.2, 0, 2, 0, 0.5)
            ext3 = (-1.2, -0.2, 0.5, 1.5, 0, 0)
            ext4 = (0.2, 1.2, 0, 2, 0, 0)
            self.scene.mlab.view(45.0, 54.735610317245346, 561.0808549293772,
                                 np.array([-0.5, -0.5, 24.66550064]))
            if self.Projection == 'Polar x-y':
                if self.Property == 'Potential':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(
                        x, y, phi / 1000, opacity=0.95, reset_zoom=False)
                    self.scene.parallel_projection = True
                    self.Units = '* Colorbar Units = V, [*1e3]'
                if self.Property == 'Electron Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x, y, den1 / 1e16, opacity=0.95)
                    self.scene.mlab.mesh(x, y, z, color=(0, 0, 0))
                    self.scene.parallel_projection = True
                    self.Units = '* Colorbar Units = m−3, [*1e16]'
                if self.Property == 'Ion Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(x, y, den2 / 3e15, opacity=0.95)
                    self.scene.mlab.mesh(x, y, z, color=(0, 0, 0))
                    self.scene.parallel_projection = True
                    self.Units = '* Colorbar Units = m−3, [*3e15]'
                if self.Property == 'Plasma Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(
                        x,
                        y,
                        den1 / 1e16,
                        opacity=0.8,
                        color=(
                            0,
                            0,
                            1))
                    self.scene.mlab.mesh(
                        x,
                        y,
                        den2 / 3e15,
                        opacity=0.8,
                        color=(
                            1,
                            0,
                            0))
                    self.Units = '* Electrons - Blue/ Ions - Red'
                    self.scene.mlab.mesh(x, y, z, color=(0, 0, 0))
                    self.scene.parallel_projection = True

            if self.Projection == 'Cartesian r-theta':
                if self.Property == 'Potential':
                    self.scene.mlab.clf()
                    self.scene.mlab.surf(phi, opacity=0.95, reset_zoom=False)
                    self.scene.parallel_projection = True
                    self.Units = '* Colorbar Units = V, [*1e0]'
                if self.Property == 'Electron Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.surf(den1 / 3e12, opacity=0.95)
                    self.Units = '* Colorbar Units = m−3, [*3e12]'
                    self.scene.mlab.surf(z, color=(0, 0, 0))
                    self.scene.parallel_projection = True
                if self.Property == 'Ion Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.surf(den2 / 3e11, opacity=0.95)
                    self.Units = '* Colorbar Units = m−3, [*3e11]'
                    self.scene.mlab.surf(z, color=(0, 0, 0))
                    self.scene.parallel_projection = True
                if self.Property == 'Plasma Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.surf(
                        den1 / 3e12, opacity=0.8, color=(0, 0, 1))
                    self.scene.mlab.surf(
                        den2 / 3e11, opacity=0.8, color=(1, 0, 0))
                    self.Units = '* Electrons - Blue/ Ions - Red'
                    self.scene.mlab.surf(z, color=(0, 0, 0))
                    self.scene.parallel_projection = True

            if self.Projection == 'Both':
                if self.Property == 'Potential':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(
                        x, y, phi / 1000, opacity=0.95, extent=ext1)
                    self.scene.mlab.surf(phi, opacity=0.95, extent=ext2)
                    self.scene.parallel_projection = True
                    self.Units = '* Colorbar Units = V,\
                        Polar [*1e3]/Cartesian [*1e0]'
                if self.Property == 'Electron Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(
                        x, y, den1 / 3e15, opacity=0.95, extent=ext1)
                    self.scene.mlab.mesh(x, y, z, color=(0, 0, 0), extent=ext3)
                    self.scene.mlab.surf(
                        den1 / 3e12, opacity=0.95, extent=ext2)
                    self.scene.mlab.surf(z, color=(0, 0, 0), extent=ext4)
                    self.scene.parallel_projection = True
                    self.Units = '* Colorbar Units = m−3,\
                        Polar [*1e15]/Cartesian [*3e12]'
                if self.Property == 'Ion Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(
                        x, y, den2 / 3e15, opacity=0.95, extent=ext1)
                    self.scene.mlab.mesh(x, y, z, color=(0, 0, 0), extent=ext3)
                    self.scene.mlab.surf(
                        den2 / 3e11, opacity=0.95, extent=ext2)
                    self.scene.mlab.surf(z, color=(0, 0, 0), extent=ext4)
                    self.scene.parallel_projection = True
                    self.Units = '* Colorbar Units = m−3,\
                        Polar [*3e15]/Cartesian [*3e11]'
                if self.Property == 'Plasma Density':
                    self.scene.mlab.clf()
                    self.scene.mlab.mesh(
                        x,
                        y,
                        den1 / 1e16,
                        opacity=0.8,
                        color=(
                            0,
                            0,
                            1),
                        extent=ext1)
                    self.scene.mlab.mesh(
                        x,
                        y,
                        den2 / 3e15,
                        opacity=0.8,
                        color=(
                            1,
                            0,
                            0),
                        extent=ext1)
                    self.scene.mlab.surf(
                        den1 / 3e12,
                        opacity=0.8,
                        color=(
                            0,
                            0,
                            1),
                        extent=ext2)
                    self.scene.mlab.surf(
                        den2 / 3e11,
                        opacity=0.8,
                        color=(
                            1,
                            0,
                            0),
                        extent=ext2)
                    self.scene.mlab.mesh(x, y, z, color=(0, 0, 0), extent=ext3)
                    self.scene.mlab.surf(z, color=(0, 0, 0), extent=ext4)
                    self.scene.parallel_projection = True
                    self.Units = '* Electrons - Blue/ Ions - Red'

            if self.Colorbar:
                if self.Property != 'Plasma Density':
                    self.scene.mlab.colorbar(
                        nb_labels=5, orientation='vertical')

            if self.Title:
                self.scene.mlab.title(self.Property, size=0.5, height=0.8)

            if self.Details:
                self.scene.mlab.text(
                    0.7,
                    0.95,
                    'Visualization Details',
                    width=0.2,
                    color=(
                        1,
                        1,
                        1))
                self.scene.mlab.text(
                    0.7,
                    0.9,
                    '* time = ' +
                    '{:0.2e}'.format(t) +
                    's',
                    width=0.15,
                    color=(
                        0,
                        0,
                        0))
                self.scene.mlab.text(
                    0.7,
                    0.85,
                    '* Projection Type = ' +
                    self.Projection,
                    width=0.2,
                    color=(
                        0,
                        0,
                        0))
                self.scene.mlab.text(
                    0.7, 0.8, self.Units, width=0.2, color=(
                        0, 0, 0))

            if self.Projection == 'Polar x-y':
                self.xaxis = 'X, [m]'
                self.yaxis = 'Y, [m]'

            if self.Projection == 'Cartesian r-theta':
                self.xaxis = 'r, 128 [Cells]'
                self.yaxis = 'theta, 256 [Cells]'

            if self.Axes:
                ax = self.scene.mlab.axes(
                    y_axis_visibility=False,
                    xlabel=self.xaxis,
                    ylabel=self.yaxis)
                ax.axes.font_factor = 0.8

        view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                         height=800, width=1500, show_label=False),
                    HSplit(Group(Item('Iteration')),
                           Group(Item('Projection'), Item('Property')),
                           Group(Item('Colorbar'), Item('Title')),
                           Group(Item('Details'), Item('Axes'))),
                    resizable=True,)

    GUI().configure_traits()


if __name__ == '__main__':

    main()
