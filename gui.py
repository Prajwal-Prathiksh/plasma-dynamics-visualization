###########################################################################
# Imports
###########################################################################
# Standard library imports
from traits.api import (
    HasTraits, Int, Bool, Directory
)
from traitsui.api import (
    Group, View, Item, OKButton, CancelButton, HelpButton
)

# Local imports
# None

###########################################################################
# Code
###########################################################################

class AutomatorGUI(HasTraits):
    data_input_dir = Directory()
    quiet = Bool(default_value=True)
    parallel = Bool(default_value=False)
    batch_size = Int(default_value=1000)

    traits_view = View(
        Group(
            Item(
                name='data_input_dir',
                label='Data Input Directory',
                has_focus=True,
                help='Input directory which contains all the data.',
                tooltip='Input directory which contains all the data.'
            ),
            Item(
                name='quiet',
                label='Quiet',
                help='If True, the program will not print anything to the console.',
                tooltip='If True, the program will not print anything to the console.'
            ),
            Item(
                name='parallel',
                label='Parallel',
                help='If True, the program will run in parallel.',
                tooltip='If True, the program will run in parallel.'
            ),
            Item(
                name='batch_size',
                label='Batch Size',
                enabled_when='parallel',
                help='The number of files to process in each batch.',
                tooltip='The number of files to process in each batch.'
            ),
            show_border=True,
            label='Automator Settings',
        ),
        buttons=[OKButton, CancelButton, HelpButton],
        title='Automator',
        width=600, height=500, resizable=True
    )

