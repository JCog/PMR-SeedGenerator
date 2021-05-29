import random
import sqlite3

from db.node import Node
import worldgraph


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
        world_graph = worldgraph.generate()

        # Generate item pools
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
        reachable_item_nodes = {}
        non_traversable_edges = []
        filled_item_nodes = []

        def depth_first_search(node_id):
            if node_id in reachable_item_nodes.keys():
                return
            reachable_item_nodes[node_id] = world_graph.get(node_id).get("node")
        
            outgoing_edges = world_graph.get(node_id).get("edge_list")
            for edge in outgoing_edges:
                #TODO check against mario's current inventory
                if all(edge.get("reqs")):
                    depth_first_search(edge.get("to").get("map") + "/" + str(edge.get("to").get("id")))
                else:
                    non_traversable_edges.append(edge)
        
        # Set node to start graph traversal from
        node_id = "KMR_20/4"

        # Place all items that influence progression
        while len(pool_progression_items) > 0:
            reachable_item_nodes = {}

            # Find all currently reachable item nodes
            depth_first_search(node_id)

            # Pick random progression_item and place it into random reachable and unfilled item node
            while True:
                random_node = reachable_item_nodes.pop(random.choice(reachable_item_nodes.keys()))
                if random_node not in filled_item_nodes:
                    break
            random_item = pool_progression_items.pop(random.randint(0, len(pool_progression_items) - 1))
            random_node.current_item = random_item
            filled_item_nodes.append(random_node)

            # Add placed progression_item into mario's inventory
            #TODO add random_item to mario's inventory
        
        # Place all remaining items
        for item_node in all_item_nodes:
            if item_node not in filled_item_nodes:
                random_item = pool_other_items.pop(random.randint(0, len(pool_other_items) - 1))
                item_node.current_item = random_item
                filled_item_nodes.append(item_node)

        for node in Node.select().where(key_name_item.is_null(False)):
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
        select_statement = ("SELECT *\
                               FROM node\
                              INNER JOIN maparea\
                                 ON node.map_area_id = maparea.id\
                              WHERE node.key_name_item IS NOT NULL")
        cursor.execute(select_statement)
        tablerows = [row for row in cursor.fetchall()]
        for i,tablerow in enumerate(tablerows):
            key_name = tablerow['key_name']
            area_id = tablerow['area_id']
            map_id = tablerow['map_id']
            index = tablerow['index']

            node = Node.get(Node.map_area.area_id==area_id, Node.map_area.map_id==map_id, Node.item_index==index)
            print(f"{node}")
            file.write(f"[{node.map_area.name}] ({node.map_area.verbose_name}): {node.key_name_item} - {node.vanilla_item.item_name} -> {node.current_item.item_name}\n")
            app.processEvents()

            yield ("Generating Log", int(100 * i / len(tablerows)))