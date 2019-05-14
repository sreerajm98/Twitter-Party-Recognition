
state_main = "Alabama	32.806671	-86.791130\n\
Alaska	61.370716	-152.404419\n\
Arizona	33.729759	-111.431221\n\
Arkansas	34.969704	-92.373123\n\
California	36.116203	-119.681564\n\
Colorado	39.059811	-105.311104\n\
Connecticut	41.597782	-72.755371\n\
Delaware	39.318523	-75.507141\n\
District of Columbia	38.897438	-77.026817\n\
Florida	27.766279	-81.686783\n\
Georgia	33.040619	-83.643074\n\
Hawaii	21.094318	-157.498337\n\
Idaho	44.240459	-114.478828\n\
Illinois	40.349457	-88.986137\n\
Indiana	39.849426	-86.258278\n\
Iowa	42.011539	-93.210526\n\
Kansas	38.526600	-96.726486\n\
Kentucky	37.668140	-84.670067\n\
Louisiana	31.169546	-91.867805\n\
Maine	44.693947	-69.381927\n\
Maryland	39.063946	-76.802101\n\
Massachusetts	42.230171	-71.530106\n\
Michigan	43.326618	-84.536095\n\
Minnesota	45.694454	-93.900192\n\
Mississippi	32.741646	-89.678696\n\
Missouri	38.456085	-92.288368\n\
Montana	46.921925	-110.454353\n\
Nebraska	41.125370	-98.268082\n\
Nevada	38.313515	-117.055374\n\
New Hampshire	43.452492	-71.563896\n\
New Jersey	40.298904	-74.521011\n\
New Mexico	34.840515	-106.248482\n\
New York	42.165726	-74.948051\n\
North Carolina	35.630066	-79.806419\n\
North Dakota	47.528912	-99.784012\n\
Ohio	40.388783	-82.764915\n\
Oklahoma	35.565342	-96.928917\n\
Oregon	44.572021	-122.070938\n\
Pennsylvania	40.590752	-77.209755\n\
Rhode Island	41.680893	-71.511780\n\
South Carolina	33.856892	-80.945007\n\
South Dakota	44.299782	-99.438828\n\
Tennessee	35.747845	-86.692345\n\
Texas	31.054487	-97.563461\n\
Utah	40.150032	-111.862434\n\
Vermont	44.045876	-72.710686\n\
Virginia	37.769337	-78.169968\n\
Washington	47.400902	-121.490494\n\
West Virginia	38.491226	-80.954453\n\
Wisconsin	44.268543	-89.616508\n\
Wyoming	42.755966	-107.302490"

arr  = state_main.split("\n")
state_dict = {}

for line in arr:
    curr_arr = line.split('	')
    state_dict[curr_arr[0]] = curr_arr[1] + "," + curr_arr[2] + ",100mi"

print state_dict


