"""
This file represents edges of the world graph that should be modified when
Chapter 4 is not required in Race Mode.
"""
race_edges_ch4_add = [
    # Residental District Toybox Spring -> BLU Station Spring Exit
    {"from": {"map": "MAC_04", "id": 2}, "to": {"map": "OMO_03", "id": 4},
     "reqs": [["YOUWIN"]]},
]


edges_ch4_remove = [
    # Residental District Toybox Spring -> BLU Station Spring Exit
    {"from": {"map": "MAC_04", "id": 2}, "to": {"map": "OMO_03", "id": 4}, "reqs": []},
]
