# py4DSTEM SER to DataCube Converter

A Python script for converting SER files containing 4D-STEM (CBED) diffraction patterns into the py4DSTEM DataCube format for further analysis.

## Description

This tool reads SER files (a common format for storing electron diffraction data from TEM/STEM microscopes) and converts them into the py4DSTEM DataCube class, which is optimized for 4D-STEM data processing and analysis. The script also provides optional binning functionality to reduce file size while preserving essential diffraction information.

## Features

- Interactive file selection from current directory
- Conversion of SER format to py4DSTEM DataCube (HDF5)
- Manual input of scan dimensions (X and Y)
- Calibration metadata preservation (pixel size and units)
- Optional NBED pattern binning (128×128, 256×256, or 512×512)
- Data export to HDF5 format

## Required Libraries

Before running the script, install the following Python packages:

```bash
pip install py4DSTEM
pip install ncempy
pip install numpy
```

### Dependencies:
- **py4DSTEM** - Main library for 4D-STEM data analysis
- **ncempy** - National Center for Electron Microscopy Python tools (for reading SER files)
- **numpy** - Numerical computing library

## How It Works

The script performs the following steps:

1. **File Selection**: Scans the current directory and displays all available files with numbered indices, allowing the user to select the target SER file.

2. **Scan Dimensions Input**: Prompts the user to input the scan grid dimensions (number of pixels in X and Y directions), as this information may not always be stored in the SER file metadata.

3. **Data Reshaping**: Reads the SER file data and reshapes it from a sequential array into a 4D array with dimensions `(scanY, scanX, nbedY, nbedX)`, where:
   - `scanY, scanX` - real-space scan dimensions
   - `nbedY, nbedX` - reciprocal-space (diffraction pattern) dimensions

4. **DataCube Creation**: Creates a py4DSTEM DataCube object with proper calibration:
   - Q-space (reciprocal space) pixel size and units from SER metadata
   - R-space (real space) pixel size set to 1 nm (can be adjusted)

5. **Optional Binning**: Offers the option to bin (downsample) the diffraction patterns to reduce file size. Optimal binned size is 128×128 pixels for most applications.

6. **Export**: Saves the DataCube to an HDF5 file with a user-specified filename.

## Usage

1. Place the script in the same directory as your SER file(s)
2. Run the script:
   ```bash
   python py4dstem_01_builder_v05.py
   ```
3. Follow the interactive prompts:
   - Select the SER file by entering its index number
   - Enter the scan dimensions (X and Y pixels)
   - Choose whether to bin the diffraction patterns
   - Enter the output filename (with .h5 extension)

## Example

```
files in current directory:
{1: 'sample_data.ser', 2: 'other_file.txt'}
enter SER file index(1-2): 1
enter pixels per line (X direction): 64
enter pixels per col  (Y direction): 64
initial size of NBED is 1024x1024
Do u want to reduce size of resulting h5 file (y/n)? y
Enter the preferred final NBED size (128, 256 or 512): 128
enter h5 output file name (_something_.h5): gaas_nbed_output.h5
```

## Notes

- The script currently sets placeholder calibration values for pixel size (`0.00025 Å⁻¹`). Update these values in the code based on your experimental conditions.
- For large scan grids (>100×100 pixels), binning is recommended to keep file sizes manageable.
- The output HDF5 file can be opened and analyzed using py4DSTEM's analysis tools.

## Author

Created for 4D-STEM data processing workflows.

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.
