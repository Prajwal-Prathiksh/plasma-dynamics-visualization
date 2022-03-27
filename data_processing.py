###########################################################################
# Imports
###########################################################################
# Standard library imports
import os
import argparse
from typing import Any, List

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
        default=None, help="Output directory. If None, a folder named"\
            "'processed_data' will be created in the input directory"
    )

    args = parser.parse_args()
    return args

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
    output_dir : str|None
        Output directory. If None, a folder named 'processed_data' will be
        created in the input directory.
    """
    def __init__(
        self, input_dir: str, input_basefile: str, output_dir: str|None=None
    ) -> None:
        self.input_dir = input_dir
        self.input_basefile = input_basefile
        self.output_dir = output_dir
        os.ma
        self.properties = self._get_properties()
        self.input_files = self._get_input_files()

    def _get_properties(self) -> List[str]:
        """
        Get all the properties available in the input directory.

        Returns:
            List of properties.
        """
        properties = os.listdir(self.input_dir)
        if properties == []:
            raise ValueError('No properties found in the input directory.')
        return properties
    
    def _get_input_files(self) -> List[str]:
        """
        Get all the input files available from the input directory, for each
        of the properties.

        Returns:
            List of input files.
        """
        input_files = []
        for property in self.properties:
            input_files.append(
                os.path.join(self.input_dir, property, self.input_basefile)
            )
        return input_files()

def main() -> None:
    args = cli_parser()
    data_processor = DataProcessor(
        input_dir=args.input_dir,
        input_basefile=args.input_basefile,
        output_dir=args.output_dir
    )


###########################################################################
# Main Code
###########################################################################
if __name__ == '__main__':
    main()
