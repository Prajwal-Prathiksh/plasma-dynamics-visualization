###########################################################################
# Imports
###########################################################################
# Standard library imports
import os
import argparse
import numpy as np
from typing import Any, List, Tuple, Union

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
        '-I', '--input-dir', action='store', dest='input_dir', type=str,
        required=True, help='Input directory which contains all the data.'
    )
    parser.add_argument(
        '-F', '--file', action='store', dest='input_basefile', type=str,
        required=True, help='Input basefile name.'
    )
    parser.add_argument(
        '-O', '--output-dir', action='store', dest='output_dir', type=str,
        default=None, help="Output directory. If None, a folder named "
        "'_processed_data' will be created in the input directory"
    )

    args = parser.parse_args()
    return args


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


class DataProcessor:
    """
    A class to process the output files from XPDC code for various properties,
    and store it as a single file (format: .npz) for each time iteration.

    Parameters
    ----------
    input_dir : str
        Input directory which contains all the data.
    input_basefile : str
        Input basefile name.
    output_dir : str
        Output directory. If None, a folder named '_processed_data' will be
        created in the input directory.
    """

    def __init__(
        self, input_dir: str, input_basefile: str, output_dir: str = None
    ) -> None:
        self.input_dir = input_dir
        self.input_basefile = input_basefile

        if output_dir is None:
            self.output_dir = os.path.join(input_dir, "_processed_data")
            os.makedirs(self.output_dir, exist_ok=True)
        else:
            self.output_dir = output_dir

        self.output_fname = os.path.join(
            self.output_dir, self.input_basefile.replace(".txt", ".npz")
        )

        self.properties = self._get_properties()

        self.data: Union[None, dict] = None

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

    def _get_input_filename(self, prop: str) -> str:
        """
        Get the input filename for the given property.

        Parameters
        ----------
        prop : str
            Property name.

        Returns
        -------
        str
            Input filename.
        """
        return os.path.join(self.input_dir, prop, self.input_basefile)

    def _read_data(self, input_file: str) -> List[str]:
        """
        Read the data from the given input file.

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
    def process_data(self) -> None:
        """
        Process the data from the input files, and store it as a single file
        for each property.
        """
        data = dict()
        for prop in self.properties:
            input_file = self._get_input_filename(prop)
            lines = self._read_data(input_file)
            time, r, theta, scalar_property = self._get_simulation_data(lines)

            if 't' not in data:
                data['t'], data['r'], data['theta'] = time, r, theta
            data[prop] = scalar_property

        data['x'], data['y'] = polar2cart(data['r'], data['theta'])
        self.data = data

    def save_data(self) -> None:
        """
        Save the processed data as a single file (format: .npz).
        """
        if self.data is None:
            raise ValueError('No data to save. Run process_data() first.')
        np.savez(self.output_fname, **self.data)
        print(f"Saved data to {self.output_fname}")


def main() -> None:
    args = cli_parser()
    data_processor = DataProcessor(
        input_dir=args.input_dir,
        input_basefile=args.input_basefile,
        output_dir=args.output_dir
    )
    data_processor.process_data()
    data_processor.save_data()


###########################################################################
# Main Code
###########################################################################
if __name__ == '__main__':
    main()
