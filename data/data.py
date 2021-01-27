import pathlib
import csv


def get_data(txt_file="wg22_xy.txt"):
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    base_dir = pathlib.Path(__file__).parent.parent.absolute()
    data = {}
    location_key = 0
    with open(base_dir.joinpath("data").joinpath(txt_file), 'r') as xy_file:
        reader = csv.reader(xy_file, delimiter=' ')
        for row in reader:
            if "#" in row:
                continue
            coord = tuple(float(i) for i in row if isfloat(i) and -90 < float(i) < 90 and float(i) != 0)
            if len(coord) != 2:
                continue
            data.update(
                {location_key: coord}
            )
            location_key += 1
    return data
