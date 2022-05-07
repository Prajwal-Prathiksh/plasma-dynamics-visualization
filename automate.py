###########################################################################
# Imports
###########################################################################
# Standard library imports
import os
import shutil
from typing import Tuple
from automan.api import Problem, Simulation, Automator

# Local imports
from data_processing import DataProcessor
from gui import MainPipelineGUI
from visual_setup import VisualSetupGUI

###########################################################################
# Code
###########################################################################


def get_batch_limits(length: int, batch: int):
    """
    Get the index limits for a given batch size, and the length of the original
    list.

    Parameters
    ----------
    length : int
        The length of the original list.
    batch : int
        Size of the batch.
    """
    batch_limits = []
    lb = 1
    while lb <= length:
        if lb + batch < length:
            limits = (lb, lb + batch - 1)
        else:
            limits = (lb, length)
        batch_limits.append(limits)
        lb += batch
    return batch_limits


def tuple2string(tup: Tuple[int, int]) -> str:
    """
    Convert a tuple to a string.

    Parameters
    ----------
    tup : Tuple[int, int]
        The tuple to convert.

    Returns
    -------
    str
        The string representation of the tuple.
    """
    return f"{tup[0]}-{tup[1]}"


class DataPreprocessingAutomator(Problem):
    def get_name(self):
        return "_data_preprocessing_TEMP"

    def setup_params(self):
        main_pipeline_gui = MainPipelineGUI()
        main_pipeline_gui.configure_traits()

        self.run_data_preprocessor = main_pipeline_gui.run_data_preprocessor
        self.run_visual_setup_simultaneously =\
            main_pipeline_gui.run_visual_setup_simultaneously

        data_input_dir = main_pipeline_gui.data_input_dir
        if data_input_dir == '' and self.run_data_preprocessor:
            raise ValueError('No data input directory specified.')

        self.data_input_dir = f'"{data_input_dir}"'
        self.quiet = main_pipeline_gui.quiet

        self.parallel = main_pipeline_gui.parallel
        self.batch_size = main_pipeline_gui.batch_size          

        self.use_data_input_dir_for_output =\
            main_pipeline_gui.use_data_input_dir_for_output
        self.visual_data_input_dir = main_pipeline_gui.visual_data_input_dir
        self.run_visual_setup = main_pipeline_gui.run_visual_setup

        if self.parallel and self.batch_size is None:
            raise ValueError(
                "If parallel is True, batch_size per job must be set."
            )

        if self.run_data_preprocessor:
            temp_obj = DataProcessor(input_dir=data_input_dir)
            self.batch_limits = get_batch_limits(
                length=len(temp_obj.input_data_files),
                batch=self.batch_size
            )
        

        if self.run_data_preprocessor and self.visual_data_input_dir == '':
            self.visual_data_input_dir = os.path.join(
                data_input_dir, '_processed_data'
            )
        elif self.run_visual_setup and self.visual_data_input_dir == '':
            raise ValueError(
                'No visual data input directory specified. '
                'Please set the visual data input directory.'
            )
        self.visual_data_input_dir = f'"{self.visual_data_input_dir}"'

    def setup_visualizer(self):
        visual_setup_gui = VisualSetupGUI(
            visual_data_input_dir=self.visual_data_input_dir,
        )
        visual_setup_gui.configure_traits()

    def setup(self):
        self.setup_params()
        self.cases = []
        
        if self.run_data_preprocessor is False:
            print("Skipping data preprocessing.")
            self.cases = []
            return

        if self.quiet:
            base_cmd = 'python data_processing.py --quiet'
        else:
            base_cmd = 'python data_processing.py'

        if self.run_visual_setup_simultaneously:
            temp_base_cmd = 'python visual_setup.py'
            self.cases.append(
                Simulation(
                    root="_visual_setup_TEMP",
                    base_command=temp_base_cmd,
                    visual_data_input_dir=self.visual_data_input_dir,
                )
            )
            print("Running visual setup simultaneously.")

        if self.parallel:
            self.cases += [
                Simulation(
                    root=f"_parallel_{i}_data_preprocessing_TEMP",
                    base_command=base_cmd,
                    input_dir=self.data_input_dir,
                    range=tuple2string(self.batch_limits[i]),
                )
                for i in range(1, len(self.batch_limits))
            ]
        else:
            self.cases += [
                Simulation(
                    root="_series_data_preprocessing_TEMP",
                    base_command=base_cmd,
                    input_dir=self.data_input_dir,
                )
            ]

        print('Setup complete.')

    def run(self):
        self.make_output_dir()
        if self.run_visual_setup:
            print("Running visual setup.")
            self.setup_visualizer()
        


###########################################################################
# Main Code
###########################################################################
if __name__ == '__main__':
    import time
    tic = time.perf_counter()
    automator = Automator(
        simulation_dir='_automator_TEMP',
        output_dir='_automator_TEMP/output',
        all_problems=[DataPreprocessingAutomator]
    )
    automator.run()
    toc = time.perf_counter()
    print('Done.')
    print(f"Time taken: {toc - tic:0.4f} seconds.")
    # Remove the temporary directories.
    shutil.rmtree('_automator_TEMP')
