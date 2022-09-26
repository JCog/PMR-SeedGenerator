"""
This file represents edges of the world graph that should be modified when
Chapter 2 is not required for Streamlined Chapters.
"""
streamlined_edges_ch2_add = [
    # Station District Train -> Train Ride Scene Exit Left
    {"from": {"map": "MAC_03", "id": 1}, "to": {"map": "IWA_11", "id": 1},
     "reqs": [["YOUWIN"]]},

    # Warp Zone 1 (B1) Blue Warp Pipe (Left) -> Outpost 1 Blue Warp Pipe
    {"from": {"map": "TIK_01", "id": 4}, "to": {"map": "DRO_01", "id": 2},
     "reqs": [["YOUWIN"]]},
]


streamlined_edges_ch2_remove = [
    # Station District Train -> Train Ride Scene Exit Left
    {"from": {"map": "MAC_03", "id": 1}, "to": {"map": "IWA_11", "id": 1}, "reqs": []},

    # Warp Zone 1 (B1) Blue Warp Pipe (Left) -> Outpost 1 Blue Warp Pipe
    {"from": {"map": "TIK_01", "id": 4}, "to": {"map": "DRO_01", "id": 2}, "reqs": []},
]
