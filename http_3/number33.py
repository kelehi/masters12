import sys

from Samples.business import find_business
from Samples.distance import lonlat_distance
from Samples.geocoder import get_coordinates
from Samples.mapapi_PG import show_map


def main():
    try:
        a = " ".join(sys.argv[1:])
        a1, a2 = get_coordinates(a)
        address_ll = f"{a1},{a2}"
        span = "0.005,0.005"
        organization = find_business(address_ll, span, "аптека")
        point = organization["geometry"]["coordinates"]
        org_lat = float(point[0])
        org_lon = float(point[1])
        point_param = f"pt={org_lat},{org_lon},pm2dgl"
        show_map(f"ll={address_ll}&spn={span}", "map", add_params=point_param)
        points_param = point_param + f"~{address_ll},pm2rdl"
        show_map("ll={0}&spn={1}".format(address_ll, span), "map", add_params=points_param)
        show_map(map_type="map", add_params=points_param)
        name = organization["properties"]["CompanyMetaData"]["name"]
        address = organization["properties"]["CompanyMetaData"]["address"]
        time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
        distance = round(lonlat_distance((a2, a1), (org_lon, org_lat)))

        snippet = f"Название:\t{name}\nАдрес:\t{address}\nВремя работы:\t{time}\n" \
                  f"Расстояние:\t{distance}м."
        print(snippet)
    except BaseException as e:
        print(e)

if __name__ == "__main__":
    main()