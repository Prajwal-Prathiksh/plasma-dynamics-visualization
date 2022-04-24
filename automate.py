###########################################################################
# Imports
###########################################################################
# Standard library imports
import shutil
from typing import Tuple
from automan.api import Problem, Simulation, Automator

# Local imports
from data_processing import DataProcessor
from gui import AutomatorGUI

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
        automate_gui = AutomatorGUI()
        automate_gui.configure_traits()

        data_input_dir = automate_gui.data_input_dir
        if data_input_dir == '' or data_input_dir is None:
            raise ValueError('No data input directory specified.')

        self.data_input_dir = f'"{data_input_dir}"'
        self.quiet = automate_gui.quiet

        self.parallel = automate_gui.parallel
        self.batch_size = automate_gui.batch_size

        if self.parallel and self.batch_size is None:
            raise ValueError(
                "If parallel is True, batch_size per job must be set."
            )
        temp_obj = DataProcessor(input_dir=data_input_dir)
        self.batch_limits = get_batch_limits(
            length=len(temp_obj.input_data_files),
            batch=self.batch_size
        )

    def setup(self):
        self.setup_params()
        if self.quiet:
            base_cmd = 'python data_processing.py --quiet'
        else:
            base_cmd = 'python data_processing.py'

        if self.parallel:
            self.cases = [
                Simulation(
                    root=f"_parallel_{i}_data_preprocessing_TEMP",
                    base_command=base_cmd,
                    input_dir=self.data_input_dir,
                    range=tuple2string(self.batch_limits[i]),
                )
                for i in range(len(self.batch_limits))
            ]
        else:
            self.cases = [
                Simulation(
                    root="_series_data_preprocessing_TEMP",
                    base_command=base_cmd,
                    input_dir=self.data_input_dir,
                )
            ]

        print('Setup complete.')

    def run(self):
        self.make_output_dir()


###########################################################################
# Main Code
###########################################################################
if __name__ == '__main__':
    automator = Automator(
        simulation_dir='_automator_TEMP',
        output_dir='_automator_TEMP/output',
        all_problems=[DataPreprocessingAutomator]
    )
    automator.run()
    print('Done.')
    # Remove the temporary directories.
    shutil.rmtree('_automator_TEMP')
