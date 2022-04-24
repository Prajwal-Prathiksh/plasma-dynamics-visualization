###########################################################################
# Imports
###########################################################################
# Standard library imports
import os
import argparse
import numpy as np
import re
from typing import Any, List, Tuple, Union
from tkinter import filedialog, Tk

# Local imports
# None

###########################################################################
# Code
###########################################################################

# TODO
# - GUI when setup from CLI
# - should ask for input_dir and output_dir
# - should ask parallel, or serial


def cli_parser() -> Any:

    def get_range_from_string(string: str) -> Tuple[int, int]:
        """
        Return a range from a string.

        Parameters
        ----------
        string : str
            String containing a range, separated by a hyphen.
            Eg: "1-10"

        Returns
        -------
        Tuple[int, int]
            Range.
        """
        if string is None:
            return None
        try:
            start, end = string.split("-")
            start = int(start)
            end = int(end)
        except ValueError:
            raise ValueError(
                f"Invalid range: {string}. "
                "The range must be separated by a hyphen, and be of the form: "
                "'start-end'."
            )
        if start >= end:
            raise ValueError(
                f"Invalid range: {string}. "
                "The start of the range must be less than the end."
            )
        return start, end

    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-I', '--input-dir', action='store', dest='input_dir', type=str,
        default=None, help='Input directory which contains all the data. '
        'If None, the user will be prompted to select a directory via GUI.'
    )
    parser.add_argument(
        '-F', '--file', action='store', dest='input_basefile', type=str,
        default=None, help='Input basefile name. If None, all the files in '
        'the input directory will be processed.'
    )
    parser.add_argument(
        '-R', '--range', action='store', dest='input_basefile_range', type=str,
        default=None, help='Input basefile range (inclusive limits). If None, '
        'all the files in the input directory will be processed. '
        'Format: 1-500, 233-235.'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_true', dest='quiet',
        help='Do not print progress.'
    )
    parser.add_argument(
        '-O', '--output-dir', action='store', dest='output_dir', type=str,
        default=None, help="Output directory. If None, a folder named "
        "'_processed_data' will be created in the input directory"
    )

    args = parser.parse_args()
    args.input_basefile_range = get_range_from_string(
        args.input_basefile_range
    )
    return args


def get_folder_from_GUI() -> str:
    """
    Allow the user to choose a folder through a Graphical-User-Interface.

    Returns
    -------
    str
        Path to the folder.
    """
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected


def polar2cart(
    r: Union[float, np.ndarray], theta: Union[float, np.ndarray]
) -> Union[Tuple[float, float], Tuple[np.ndarray, np.ndarray]]:
    """
    Convert polar coordinates to cartesian coordinates.

    Parameters
    ----------
    r : float or ndarray
        Radius.
    theta : float or ndarray
        Angle.

    Returns
    -------
    Tuple[float, float] or Tuple[ndarray, ndarray]
        Cartesian coordinates.
    """
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def get_number_in_a_string(
    string: str
) -> int:
    """
    Return the number (int) present in a string.

    Parameters
    ----------
    string : str
        String containing a number.

    Returns
    -------
    int
        Number present in the string.
    """
    return list(map(int, re.findall(r'\d+', string)))[0]


def convert_x_y_array_to_mgrid(
    x_array: np.ndarray, y_array: np.ndarray
) -> np.ndarray:
    """
    Convert x and y arrays to a mgrid.

    Parameters
    ----------
    x_array : ndarray
        Array containing x coordinates.
    y_array : ndarray
        Array containing y coordinates.

    Returns
    -------
    ndarray
        mgrid containing x and y coordinates.
    """
    x_array = np.array(x_array)
    y_array = np.array(y_array)
    x_mgrid, y_mgrid = np.meshgrid(x_array, y_array)
    return x_mgrid, y_mgrid


class DataProcessor:
    """
    A class to process the output files from XPDC code for various properties,
    and store it as a single file (format: .npz) for each time iteration.

    Parameters
    ----------
    input_dir : str
        Input directory which contains all the data.
        Eg : /home/user/data/
        `data` folder here will contain sub-folders for each property, eg:
            - /home/user/data/rho
            - /home/user/data/phi
            - /home/user/data/magnetic_field_strength
    input_basefile : str, Default: None
        Input basefile name.
        Eg : Benchmark_1.txt
        If None, all the files in the input directory will be processed.
    input_basefile_range : Tuple[int, int], Default: None
        Range of input basefiles to be processed.
        Eg: (1, 5) - Processes files 1 to 5, inclusive.
        If an input basefile with a number not in this range is encountered,
        it will be skipped, and the next file will be processed.
        If None, all the files in the input directory will be processed.
        *Note:* If input_basefile is not None, input_basefile_range will be
        ignored.
    output_dir : str, Default: None
        Output directory. If None, a folder named '_processed_data' will be
        created in the input directory, and the output files will be stored
        there.
        Eg : /home/user/data/_preprocessed_data/Benchmark_1.npz
    """

    def __init__(
        self,
        input_dir: str,
        input_basefile: str = None,
        input_basefile_range: Tuple[int, int] = None,
        output_dir: str = None
    ) -> None:
        self.input_dir = input_dir
        self.input_basefile = input_basefile
        self.input_basefile_range = input_basefile_range

        self.properties = self._get_properties()

        self.input_data_files = self._get_input_data_files(
            input_basefile=self.input_basefile,
            input_basefile_range=self.input_basefile_range
        )

        default_path = os.path.join(input_dir, "_processed_data")
        self.output_dir = output_dir if output_dir else default_path

    # Private methods
    def _get_properties(self) -> List[str]:
        """
        Get all the properties available in the input directory.

        Returns
        -------
            List of properties.
        """
        properties = []
        for prop in os.listdir(self.input_dir):
            if not prop.startswith("_"):
                properties.append(prop)
        if properties == []:
            raise ValueError('No properties found in the input directory.')
        return properties

    def _get_input_data_files(
        self, input_basefile: Union[str, None],
        input_basefile_range: Union[Tuple[int, int],  None]
    ) -> List[str]:
        if input_basefile is not None:
            self.n_leading_zeros = 4
            return [input_basefile]
        else:
            filenames = os.listdir(
                os.path.join(self.input_dir, self.properties[0])
            )
            filenames.sort(key=get_number_in_a_string)
            self.n_leading_zeros = len(str(len(filenames)))
            if input_basefile_range is None:
                return filenames
            else:
                return filenames[
                    input_basefile_range[0] - 1: input_basefile_range[1]
                ]

    def _get_input_file(self, prop: str, fname: str) -> str:
        """
        Get the input filename for the given property.

        Parameters
        ----------
        prop : str
            Property name.
        fname : str
            Filename.

        Returns
        -------
        str
            Input filename.
        """
        return os.path.join(self.input_dir, prop, fname)

    def _get_output_fname(self, fname: str) -> str:
        """
        Get the output filename for the given filename.

        Parameters
        ----------
        fname : str
            Filename.

        Returns
        -------
        str
            Output filename.
        """
        fname = fname.replace(".txt", ".npz")
        idx = str(get_number_in_a_string(fname))
        fname = fname.replace(idx, idx.zfill(self.n_leading_zeros))
        return os.path.join(self.output_dir, fname)

    def _read_lines(self, input_file: str) -> List[str]:
        """
        Read the lines from the given input file.

        Parameters
        ----------
        input_file : str
            Input file path.

        Returns
        -------
        List[str]
            List of lines from the input file.
        """
        with open(input_file, "r") as f:
            lines = f.readlines()
        return lines

    def _get_simulation_data(self, lines: List[str]) -> List[float]:
        """
        Get the simulation data from the input file.
        Input file needs to have the following data:
            - Time
            - R
            - Theta
            - Scalar Property

        Parameters
        ----------
        lines : List[str]
            List of lines from the input file.

        Returns
        -------
        List[float]
            Simulation data.
        """
        try:
            time = float(lines[1].split()[2][:-1])
        except Exception as e:
            print(
                "Time not found in the input file. Check the input file's "
                "format."
            )
            raise e

        r, theta, scalar_property = [], [], []
        for i in range(2, len(lines)):
            data = lines[i].split()
            r.append(float(data[0]))
            theta.append(float(data[1]))
            scalar_property.append(float(data[2]))

        return time, r, theta, scalar_property

    # Public methods
    def process_data(
        self, quiet: bool = False
    ) -> None:
        """
        Process the data from the input files, and store it as a  single file
        (format: .npz).

        Parameters
        ----------
        quiet : bool, Default: False
            If True, no output will be printed.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        
        for fname in self.input_data_files:
            data = dict()
            for prop in self.properties:
                input_file = self._get_input_file(prop=prop, fname=fname)
                lines = self._read_lines(input_file)
                time, r, theta, scalar_property = self._get_simulation_data(
                    lines
                )

                if 't' not in data:
                    data['t'], data['r'], data['theta'] = time, r, theta
                data[prop] = scalar_property

            data['x'], data['y'] = polar2cart(data['r'], data['theta'])

            output_fname = self._get_output_fname(fname=fname)
            np.savez(output_fname, **data)
            if not quiet:
                print(f"Saved data : {output_fname}")


def main() -> None:
    args = cli_parser()

    if args.input_dir is None:
        input_dir = get_folder_from_GUI()
    else:
        input_dir = args.input_dir

    data_processor = DataProcessor(
        input_dir=input_dir,
        input_basefile=args.input_basefile,
        input_basefile_range=args.input_basefile_range,
        output_dir=args.output_dir
    )
    data_processor.process_data(quiet=args.quiet)


###########################################################################
# Main Code
###########################################################################
if __name__ == '__main__':
    main()
