"""
This file represents edges of the world graph that should be modified when
Chapter 5 is not required in Race Mode.
"""
race_edges_ch5_add = [
    # Port District Exit Right -> Port District Ride Whale
    {"from": {"map": "MAC_05", "id": 0}, "to": {"map": "MAC_05", "id": 1},
     "reqs": [["RF_CanRideWhale"], ["YOUWIN"]]},

    # Second Level Entry (B2) Blue Warp Pipe -> Village Buildings Blue Warp Pipe
    {"from": {"map": "TIK_08", "id": 4}, "to": {"map": "JAN_03", "id": 3},
     "reqs": [["YOUWIN"]]},
]


edges_ch5_remove = [
    # Port District Exit Right -> Port District Ride Whale
    {"from": {"map": "MAC_05", "id": 0}, "to": {"map": "MAC_05", "id": 1}, "reqs": [["RF_CanRideWhale"]]},

    # Second Level Entry (B2) Blue Warp Pipe -> Village Buildings Blue Warp Pipe
    {"from": {"map": "TIK_08", "id": 4}, "to": {"map": "JAN_03", "id": 3}, "reqs": []},
]
