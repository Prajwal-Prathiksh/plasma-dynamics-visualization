###########################################################################
# Imports
###########################################################################
# Standard library imports
import os
import argparse
from typing import Any
import numpy as np
from traits.api import (
    HasTraits, Range, Instance, observe, Enum, Bool, Str, Int, Button
)
from traitsui.api import View, Item, Group, HSplit
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel

# Local imports
# None

###########################################################################
# Code
###########################################################################
def cli_parser() -> Any:
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-I', '--visual-data-input-dir', action='store',
        dest='visual_data_input_dir', type=str,
        default=None, help='Input directory which contains all the data '
        'to be visualized.', required=True
    )

    args = parser.parse_args()
    return args

class VisualSetupGUI(HasTraits):
    # Traits
    Iteration = Range(
        low='_low',
        high='_n_files',
        value=0,
        desc='Iteration number'
    )
    _n_files = Int(0)
    _low = Int(0)
    update_files = Button('Refresh')
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

    def __init__(self,visual_data_input_dir,**kw):
        """
        Initialize the GUI.
        
        Parameters
        ----------
        visual_data_input_dir : str
            Input directory which contains all the data to be visualized.
        """
        self.visual_data_input_dir=visual_data_input_dir
        self._setup_data()
        super(VisualSetupGUI,self).__init__(**kw)

    def _get_data_files(self):
        """
        Get the data files in the input directory, which ends with '.npz'.
        """
        filenames = os.listdir(self.visual_data_input_dir)
        filenames = [
            filename for filename in filenames if filename.endswith('.npz')
        ]
        filenames = [
            os.path.join(self.visual_data_input_dir, filename)
            for filename in filenames
        ]
        self.data_filenames = filenames
    
    def _setup_data(self):
        """
        Setup the data to be visualized.
        """
        self._get_data_files()
        self._n_files = len(self.data_filenames)


    def _get_ith_filename(self, i:int) -> str:
        """
        Get the ith filename.
        
        Parameters
        ----------
        i : int
            Index of the filename.
        
        Returns
        -------
        str
            The ith filename.
        """
        if i < len(self.data_filenames):
            return self.data_filenames[i]
        else:
            raise ValueError(f"Index {i} is out of range.")

    # Obervable Functions
    def _update_files_fired(self):
        print('Updating files...')
        self._setup_data()

    @observe(
        'Iteration,Property,Projection,Colorbar,Title,Details,Axes,\
            scene.activated'
    )
    def Plots(self, event=None):

        i = self.Iteration
        fname = self._get_ith_filename(i)
        data = np.load(fname)
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
                self.Units = ('* Colorbar Units = V,' +
                    'Polar [*1e3]/Cartesian [*1e0]')
            if self.Property == 'Electron Density':
                self.scene.mlab.clf()
                self.scene.mlab.mesh(
                    x, y, den1 / 3e15, opacity=0.95, extent=ext1)
                self.scene.mlab.mesh(x, y, z, color=(0, 0, 0), extent=ext3)
                self.scene.mlab.surf(
                    den1 / 3e12, opacity=0.95, extent=ext2)
                self.scene.mlab.surf(z, color=(0, 0, 0), extent=ext4)
                self.scene.parallel_projection = True
                self.Units = ('* Colorbar Units = m−3,' +
                    'Polar [*1e15]/Cartesian [*3e12]')
            if self.Property == 'Ion Density':
                self.scene.mlab.clf()
                self.scene.mlab.mesh(
                    x, y, den2 / 3e15, opacity=0.95, extent=ext1)
                self.scene.mlab.mesh(x, y, z, color=(0, 0, 0), extent=ext3)
                self.scene.mlab.surf(
                    den2 / 3e11, opacity=0.95, extent=ext2)
                self.scene.mlab.surf(z, color=(0, 0, 0), extent=ext4)
                self.scene.parallel_projection = True
                self.Units = ('* Colorbar Units = m−3,' +
                    'Polar [*3e15]/Cartesian [*3e11]')
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
                Group(Item('Iteration')),
                HSplit(
                        Group(Item('Projection'), Item('Property')),
                        Group(Item('Colorbar'), Item('Title')),
                        Group(Item('Details'), Item('Axes')),
                    ),
                Item(name='update_files', show_label=False),
                resizable=True,)

def main(visual_data_input_dir):
    visual_setup_gui = VisualSetupGUI(
        visual_data_input_dir=visual_data_input_dir
    )
    visual_setup_gui.configure_traits()

###########################################################################
# Main Code
###########################################################################
if __name__ == '__main__':
    args = cli_parser()
    main(
        visual_data_input_dir=args.visual_data_input_dir
    )
