import random
import sqlite3

from db.node import Node
from db.map_area import MapArea
import worldgraph
from simulate import Mario, add_to_inventory


def place_items(app, isShuffle, algorithm):
    """Places items into item locations according to the given algorithm."""

    # Place items into item location
    if algorithm == "vanilla":
        # Place items in their vanilla locations
        for node in Node.select().where(key_name_item.is_null(False)):
            node.current_item = node.vanilla_item
            node.save()

    elif algorithm == "random_fill":
        # Place items 100% randomly without any logic attached. Check for solvability afterwards, retry if necessary
        # Generate item pool
        item_pool = []

        for node in Node.select().where(key_name_item.is_null(False)):
            item_pool.append(node.vanilla_item)
        
        for node in Node.select().where(key_name_item.is_null(False)):
            # Place random items
            node.current_item = item_pool.pop(random.randint(0,len(item_pool) - 1))
            node.save()
            
        # Check for solvability
        # TODO

    elif algorithm == "forward_fill":
        # Place items in accessible locations first, then expand accessible locations by unlocked locations
        # Prepare world graph
        print("Generating World Graph ...")
        world_graph = worldgraph.generate()

        # Prepare Mario's starting inventory
        mario = Mario()
        add_to_inventory(["PARTNER_Goombario","PARTNER_Kooper","PARTNER_Bombette","PARTNER_Parakarry",
                          "PARTNER_Bow","PARTNER_Watt","PARTNER_Sushie","PARTNER_Lakilester"])
        add_to_inventory("EQUIPMENT_Hammer_Progressive")

        # Generate item pools
        print("Generating Item Pool ...")
        pool_progression_items = []
        pool_other_items = []
        all_item_nodes = []

        for node_id in world_graph.keys():
            if world_graph.get(node_id).get("node").key_name_item:
                cur_node = world_graph.get(node_id).get("node")
                all_item_nodes.append(cur_node)
                if cur_node.vanilla_item.progression:
                    pool_progression_items.append(cur_node.vanilla_item)
                else:
                    pool_other_items.append(cur_node.vanilla_item)

        # Prepare datastructures
        reachable_nodes = []
        reachable_item_nodes = {}
        non_traversable_edges = []
        filled_item_nodes = []
        filled_item_node_ids = []

        def depth_first_search(node_id):
            if node_id in reachable_nodes:
                return
            reachable_nodes.append(node_id)
            if world_graph.get(node_id).get("node").key_name_item is not None:
                reachable_item_nodes[node_id] = world_graph.get(node_id).get("node")

            outgoing_edges = world_graph.get(node_id).get("edge_list")
            for edge in outgoing_edges:
                try:
                    if all([r() for r in edge.get("reqs")]):
                        if edge.get("pseudoitems") is not None:
                            for pseudoitem in edge.get("pseudoitems"):
                                pseudoitem_acquired = add_to_inventory(pseudoitem)
                        depth_first_search(edge.get("to").get("map") + "/" + str(edge.get("to").get("id")))
                    elif edge not in non_traversable_edges:
                        non_traversable_edges.append(edge)
                except TypeError as err:
                    print(f"{err.args}: {edge}")
                    raise
        
        # Set node to start graph traversal from
        node_id = "MAC_00/4"
        
        # Find initially reachable nodes
        print("Placing Progression Items ...")
        reachable_nodes = []
        reachable_item_nodes = {}

        depth_first_search(node_id)

        # Place all items that influence progression and re-traverse formerly locked parts of the graph
        while len(pool_progression_items) > 0:

            # Pick random progression_item and place it into random reachable and unfilled item node
            while True:
                random_node = reachable_item_nodes.pop(random.choice(list(reachable_item_nodes.keys())))
                if random_node not in filled_item_nodes:
                    break
            random_item = pool_progression_items.pop(random.randint(0, len(pool_progression_items) - 1))
            random_node.current_item = random_item
            filled_item_nodes.append(random_node)
            if random_node.entrance_id is not None:
                filled_item_node_ids.append(random_node.map_area.name + "/" + str(random_node.entrance_id))
            else:
                filled_item_node_ids.append(random_node.map_area.name + "/" + random_node.key_name_item)

            # Add placed progression_item into mario's inventory
            add_to_inventory(random_item.item_name)

            # Check for newly available nodes and add those to reachable_nodes
            while True:
                pseudoitem_acquired = False
                non_traversable_edges_tmp = non_traversable_edges.copy()
                non_traversable_edges = []
                for non_traversable_edge in non_traversable_edges_tmp:
                    from_node_id = (  non_traversable_edge.get("from").get("map")
                                    + "/" 
                                    + str(non_traversable_edge.get("from").get("id")))
                    # remove edge's from-node from reachable_nodes, or else DFS won't do anything
                    i = 0
                    while i < len(reachable_nodes):
                        cur_node_id = reachable_nodes[i]
                        if cur_node_id == from_node_id:
                            reachable_nodes.pop(i)
                            break
                        else:
                            i += 1
                    # DFS from edge's from-node
                    depth_first_search(from_node_id)
                # If we find atleast one pseudo-item (partner, upgrade, flag, koopa koot favor), then
                # we have to check for reachable_nodes repeatedly until no new pseudoitems are found
                if not pseudoitem_acquired:
                    break
        
        # Place all remaining items
        print("Placing Miscellaneous Items ...")
        for item_node in all_item_nodes:
            if item_node.entrance_id is not None:
                item_node_id = item_node.map_area.name + "/" + str(item_node.entrance_id)
            else:
                item_node_id = item_node.map_area.name + "/" + item_node.key_name_item

            if item_node_id not in filled_item_node_ids:
                random_item = pool_other_items.pop(random.randint(0, len(pool_other_items) - 1))
                item_node.current_item = random_item
                filled_item_nodes.append(item_node)
                filled_item_node_ids.append(item_node_id)

        # Write changed items to sqlite db
        print("Writing Items to SQLite DB ...")
        for node in Node.select().where(Node.key_name_item.is_null(False)):
            for filled_item_node in filled_item_nodes:
                if (    filled_item_node.map_area == node.map_area
                    and filled_item_node.key_name_item == node.key_name_item):
                    current_node = filled_item_node
                    break
            node.current_item = current_node.current_item
            node.save()

    elif algorithm == "assumed_fill":
        # Start with all items in inventory, remove an item and try to place it at a reachable location
        None # NYI # TODO
    
    # Compare randomized database with default and log the changes
    with open("./debug/item_placement.txt", "w") as file:
        connection = sqlite3.connect("default_db.sqlite")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        select_statement = ("SELECT node.key_name_item AS key_name_item\
                                  , maparea.area_id    AS area_id\
                                  , maparea.map_id     AS map_id\
                                  , node.item_index    AS item_index\
                               FROM node\
                              INNER JOIN maparea\
                                 ON node.map_area_id = maparea.id\
                              WHERE node.key_name_item IS NOT NULL")
        cursor.execute(select_statement)
        tablerows = [row for row in cursor.fetchall()]
        for i,tablerow in enumerate(tablerows):
            key_name = tablerow['key_name_item']
            area_id = tablerow['area_id']
            map_id = tablerow['map_id']
            item_index = tablerow['item_index']

            node = Node.select().join(MapArea).where((MapArea.area_id==area_id) & (MapArea.map_id==map_id) & (Node.item_index==item_index)).get()
            #node = Node.get(Node.map_area.area_id==area_id, Node.map_area.map_id==map_id, Node.item_index==item_index)
            print(f"{node}")
            file.write(f"[{node.map_area.name}] ({node.map_area.verbose_name}): {node.key_name_item} - {node.vanilla_item.item_name} -> {node.current_item.item_name}\n")
            app.processEvents()

            yield ("Generating Log", int(100 * i / len(tablerows)))
