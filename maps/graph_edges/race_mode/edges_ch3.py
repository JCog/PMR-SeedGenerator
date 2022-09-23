"""
This file represents edges of the world graph that should be modified when
Chapter 3 is not required in Race Mode.
"""
race_edges_ch3_add = [
    # Southern District Exit Right -> Exit to Toad Town Exit left
    {"from": {"map": "MAC_02", "id": 1}, "to": {"map": "MIM_10", "id": 0},
     "reqs": [["YOUWIN"]]},

    # Warp Zone 2 (B2) Blue Warp Pipe -> Outside Boo's Mansion Blue Warp Pipe
    {"from": {"map": "TIK_09", "id": 2}, "to": {"map": "MIM_11", "id": 3},
     "reqs": [["YOUWIN"]]},
]


edges_ch3_remove = [
    # Southern District Exit Right -> Exit to Toad Town Exit left
    {"from": {"map": "MAC_02", "id": 1}, "to": {"map": "MIM_10", "id": 0}, "reqs": []},

    # Warp Zone 2 (B2) Blue Warp Pipe -> Outside Boo's Mansion Blue Warp Pipe
    {"from": {"map": "TIK_09", "id": 2}, "to": {"map": "MIM_11", "id": 3}, "reqs": []},
]
