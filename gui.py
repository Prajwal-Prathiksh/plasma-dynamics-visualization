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


class MainPipelineGUI(HasTraits):
    
    # Data-preprocessor settings
    run_data_preprocessor = Bool(default_value=False)
    run_visual_setup_simultaneously = Bool(default_value=False)
    data_input_dir = Directory()
    quiet = Bool(default_value=True)
    parallel = Bool(default_value=False)
    batch_size = Int(default_value=300)

    # Visualization settings
    run_visual_setup = Bool(default_value=False)
    use_data_input_dir_for_output = Bool(default_value=False)
    visual_data_input_dir = Directory()

    traits_view = View(
        Group(
            Item(
                name='run_data_preprocessor',
                label='Run Data Preprocessor',
                help='If True, the data preprocessor will be run.',
                tooltip='If True, the data preprocessor will be run.'
            ),
            Item(
                name='run_visual_setup_simultaneously',
                label='Run Visual Setup Simultaneously',
                enabled_when='run_data_preprocessor',
                help='If True, the visual setup will be run '
                'simultaneously with the data preprocessor.',
                tooltip='If True, the visual setup will be run '
                'simultaneously with the data preprocessor.'
            ),
            Item(
                name='data_input_dir',
                label='Data Input Directory',
                has_focus=True,
                help='Input directory which contains all the data. '
                '\nEg : /home/user/data/'
                '   Here the `data` folder will contain sub-folders for each '
                'property, eg:'
                '   - /home/user/data/rho '
                '   - /home/user/data/phi '
                '   - /home/user/data/magnetic_field_strength. '
                "   A folder named '_processed_data' will be created in "
                'the input directory, and the output files will be stored '
                'there. '
                '   Eg : /home/user/data/_preprocessed_data/Benchmark_1.npz',
                tooltip='Input directory which contains all the data.'
            ),
            Item(
                name='quiet',
                label='Quiet',
                help='If True, the program will not print anything to '
                'the console.',
                tooltip='If True, the program will not print anything to '
                'the console.'
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
                help='The number of files to process in each batch. '
                'Enabled only if parallel is True.',
                tooltip='The number of files to process in each batch. '
                'Enabled only if parallel is True.'
            ),
            show_border=True,
            label='Data-Preprocessor Settings'
        ),
        Group(
            Item(
                name='run_visual_setup',
                label='Run Visual Setup',
                enabled_when='not run_visual_setup_simultaneously',
                help='If True, the visualizer will be setup at the end of '
                'data preprocessing.',
                tooltip='If True, the visualizer will be setup at the end of '
                'data preprocessing.'
            ),
            Item(
                name='use_data_input_dir_for_output',
                label='Read Data from Data Input Directory',
                enabled_when='run_data_preprocessor and not '
                'run_visual_setup_simultaneously',
                help='If True, the visualizer will read the data from '
                'the data input directory. If False, the visualizer will '
                'read the data from the Visual Data Input Directory.',
                tooltip='If True, the visualizer will read the data from '
                'the data input directory. If False, the visualizer will '
                'read the data from the Visual Data Input Directory.'
            ),
            Item(
                name='visual_data_input_dir',
                label='Visual Data Input Directory',
                enabled_when='not use_data_input_dir_for_output and not '
                'run_visual_setup_simultaneously',
                help='Input directory which contains all the data. '
                '\nEg : /home/user/data/_processed_data',
                tooltip='Input directory which contains all the data.'
            ),
            show_border=True,
            label='Visual Setup Settings',
        ),
        buttons=[OKButton, CancelButton, HelpButton],
        title='Automator',
        width=600, height=500, resizable=True
    )


###########################################################################
# Main Code
###########################################################################
if __name__ == '__main__':
    main_pipeline_gui = MainPipelineGUI()
    main_pipeline_gui.configure_traits()
    print(f'Run data preprocessor: {main_pipeline_gui.run_data_preprocessor}')
    print(f'Data input directory: {main_pipeline_gui.data_input_dir}')
    print(f'Quiet: {main_pipeline_gui.quiet}')
    print(f'Parallel: {main_pipeline_gui.parallel}')
    print(f'Batch size: {main_pipeline_gui.batch_size}')
    print(f'Run visual setup: {main_pipeline_gui.run_visual_setup}')
    print(f'Use data input directory for output: {main_pipeline_gui.use_data_input_dir_for_output}')
    print(f'Visual data input directory: {main_pipeline_gui.visual_data_input_dir}')
