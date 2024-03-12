import sys

from Samples.geocoder import get_coordinates, get_ll_span
from Samples.mapapi_PG import show_map


def main():
    a = " ".join(sys.argv[1:])
    text = 'No data'

    if a:
        b, b1 = get_coordinates(a)
        ll_spn = f"ll={b},{b1}&spn=0.005,0.005"
        show_map(ll_spn, "map")

        v, spn = get_ll_span(a)
        ll_spn = f"ll={v}&spn={spn}"
        show_map(ll_spn, "map")

        point_param = f"pt={v}"
        show_map(ll_spn, "map", add_params=point_param)
    else:
        print(text)


if __name__ == "__main__":
    main()
