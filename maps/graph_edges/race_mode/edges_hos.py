"""
This file represents edges of the world graph that should be modified when
the number of star spirits required to reach Star Haven is less than 7.
"""


def get_race_edges_hos_add(chapter_count):
    return [
        # Frozen Room (B3) Green Pipe Right -> Shiver City Center Greep Pipe
        {"from": {"map": "HOS_01", "id": 0}, "to": {"map": "HOS_01", "id": 1},
         "reqs": [[{"starspirits": chapter_count}]]},
    ]


edges_race_hos_remove = [
    # Shooting Star Summit Exit Bottom Left -> Shooting Star Summit Ride Up To Starway
    {"from": {"map": "HOS_01", "id": 0}, "to": {"map": "HOS_01", "id": 1}, "reqs": [[{"starspirits": 7}]]},
]
