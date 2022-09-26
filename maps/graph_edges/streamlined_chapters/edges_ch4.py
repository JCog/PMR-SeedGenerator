"""
This file represents edges of the world graph that should be modified when
Chapter 4 is not required for Streamlined Chapters.
"""
streamlined_edges_ch4_add = [
    # Residental District Toybox Spring -> BLU Station Spring Exit
    {"from": {"map": "MAC_04", "id": 2}, "to": {"map": "OMO_03", "id": 4},
     "reqs": [["YOUWIN"]]},
]


streamlined_edges_ch4_remove = [
    # Residental District Toybox Spring -> BLU Station Spring Exit
    {"from": {"map": "MAC_04", "id": 2}, "to": {"map": "OMO_03", "id": 4}, "reqs": []},
]
