#串接，擷取公開資料
import urllib.request as request
import json
spot_src="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
with request.urlopen(spot_src) as response:
    spot_data=json.load(response)
# print(spot_data)

mrt_src="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
with request.urlopen(mrt_src) as response:
    mrt_data=json.load(response)
# print(mrt_data)

#將Spot的列表存下來
spotlist=spot_data["data"]["results"]
# for spot in spotlist:
#     print(spot["stitle"])  
#     print(spot["longitude"])
#     print(spot["langinfo"])
#     picurl=spot["filelist"].lower().split(".jpg")[0]+".jpg"
#     print(picurl)

# create dictionary for serial_no mapping MAT station
serial_to_mrt = {}
# create dictionary for serial_no mapping district
serial_to_district = {}
for entry in mrt_data["data"]:
    serial_number = entry["SERIAL_NO"]
    mrt_station = entry["MRT"]
    serial_to_mrt[serial_number] = mrt_station

    address = entry["address"]
    district = address.split('  ')[1][:3]
    serial_to_district[serial_number] = district
# print(serial_to_mrt)
# print(serial_to_district)

with open("spot.csv","w",encoding="utf-8-sig") as file:
    for spot in spotlist:
        file.write(spot["stitle"]+",")
        serial_number = spot["SERIAL_NO"]
        district = serial_to_district.get(serial_number, "Unknown District")
        file.write(district+",")
        file.write(spot["longitude"]+",")
        file.write(spot["latitude"]+",") 
        picurl=spot["filelist"].lower().split(".jpg")[0]+".jpg"
        file.write(picurl+"\n") 

# Grouping spots by MRT station
mrt_spots = {}
for spot in spotlist:
    serial_number = spot["SERIAL_NO"]
    mrt_station = serial_to_mrt.get(serial_number, "Unknown MRT")
    if mrt_station not in mrt_spots:
        mrt_spots[mrt_station] = []

    mrt_spots[mrt_station].append(spot["stitle"])
  
# for mrt, spots in mrt_spots.items():
#     spots_list = ",".join(spots)
#     print(f"{mrt},{spots}")

with open("mrt.csv", "w", encoding="utf-8-sig") as file:
    for mrt, spots in mrt_spots.items():
        spots_list = ",".join(spots)
        file.write(f"{mrt},{spots_list}\n")         