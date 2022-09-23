"""
This file represents edges of the world graph that should be modified when
Chapter 7 is not required in Race Mode.
"""
race_edges_ch7_add = [
    # Frozen Room (B3) Green Pipe Right -> Shiver City Center Greep Pipe
    {"from": {"map": "TIK_17", "id": 1}, "to": {"map": "SAM_02", "id": 2},
     "reqs": [["YOUWIN"]]},
]


edges_ch7_remove = [
    # Frozen Room (B3) Green Pipe Right -> Shiver City Center Greep Pipe
    {"from": {"map": "TIK_17", "id": 1}, "to": {"map": "SAM_02", "id": 2}, "reqs": []},
]
