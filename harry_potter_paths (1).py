import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from queue import Queue, PriorityQueue
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

class HogwartsMap:
    def __init__(self):
        #Set provinces and for paths
        self.places = set()
        self.paths = {}

    def add_path(self, from_place, to_place, hops, distance, time, dementors):
        #Added provinces
        self.places.update([from_place, to_place])
        #For path
        path_info = {
            "to": to_place,
            "hops": hops,
            "distance": distance,
            "time": time,
            "dementors": dementors
        }
        #add path to the lust
        if from_place not in self.paths:
            self.paths[from_place] = []
        self.paths[from_place].append(path_info)

    def build_map(self, path_list):
        #helkp make graph
        for entry in path_list:
            self.add_path(
                entry['start'],
                entry['end'],
                entry['hops'],
                entry['distance'],
                entry['time'],
                entry['dementors']
            )

    def show_map(self):
        #Prints magical places and the paths between them
        print("Magical Places:")
        for place in sorted(self.places):
            print(f"• {place}")
        print("\nPaths:")
        for start, routes in self.paths.items():
            for path in routes:
                print(f"{start} -> {path['to']} | Hops: {path['hops']}, Distance: {path['distance']} km, Time: {path['time']} hrs, Dementors: {path['dementors']}")

    def find_fewest_hops_path(self, start, end):
        #Breadth-First Search (BFS) 
        explore = Queue()
        explore.put((start, [start]))
        visited = set()

        while not explore.empty():
            current, route = explore.get()
            if current == end:
                return route

            if current in visited:
                continue

            visited.add(current)
            for path in self.paths.get(current, []):
                next_place = path['to']
                if next_place not in visited:
                    explore.put((next_place, route + [next_place]))
        return None

    def magical_route(self, start, end, cost_fn):
        #Dijkstra’s algorithm
        #use a priority queue
        explore = PriorityQueue()
        explore.put((0, start, [start]))
        best_cost = {start: 0}

        while not explore.empty():
            cost_so_far, current, route = explore.get()

            if current == end:
                return route, cost_so_far

            if best_cost.get(current, float('inf')) < cost_so_far:
                continue

            for path in self.paths.get(current, []):
                next_place = path['to']
                new_cost = cost_so_far + cost_fn(path)

                if next_place not in best_cost or new_cost < best_cost[next_place]:
                    best_cost[next_place] = new_cost
                    explore.put((new_cost, next_place, route + [next_place]))
        return None, float('inf')

    def find_shortest_distance_path(self, start, end):
        #Gives the path that has the shortets total distance
        return self.magical_route(start, end, lambda path: path['distance'])

    def find_fastest_time_path(self, start, end):
        #Gives the path that gives the fastest the travel time
        return self.magical_route(start, end, lambda path: path['time'])

    def find_least_dementors_path(self, start, end):
        #Give path with the least ammount of dementors
        return self.magical_route(start, end, lambda path: path['dementors'])

def show_wizard_routes(hogwarts_map, wizard_paths, wizard_origins):
   
    metrics = ["SHP", "SDP", "STP", "FDP"]
    metric_titles = {
        "SHP": "Shortest Hop Path",
        "SDP": "Shortest Distance Path",
        "STP": "Shortest Time Path",
        "FDP": "Fewest Dementors Path"
    }
    metric_units = {
        "SHP": "Spells",
        "SDP": "km",
        "STP": "hrs",
        "FDP": ""  
    }
    #Character colors on graph
    wizard_colors = {
        "Harry Potter": "red",
        "Hermione Granger": "green",
        "Ron Weasley": "blue",
        "Luna Lovegood": "purple",
        "Neville Longbottom": "orange",
        "Ginny Weasley": "cyan"
    }

    #Makes the graph
    G = nx.DiGraph()
    for place in hogwarts_map.places:
        G.add_node(place)
    for from_place, links in hogwarts_map.paths.items():
        for path in links:
            G.add_edge(
                from_place, path["to"],
                hops=path["hops"],
                distance=path["distance"],
                time=path["time"],
                dementors=path["dementors"]
            )
    try:
        layout = nx.kamada_kawai_layout(G)
    except:
        layout = nx.spring_layout(G, seed=42)

    for metric in metrics:
        #Makes a figure and set up the layout for the graph table and legend)
        fig = plt.figure(figsize=(15, 10))
        gs = GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[1, 3])
        main_ax = fig.add_subplot(gs[:, 0])
        table_ax = fig.add_subplot(gs[0, 1])
        legend_ax = fig.add_subplot(gs[1, 1])
        table_ax.axis("off")
        legend_ax.axis("off")
        fig.suptitle(metric_titles[metric], fontsize=20, fontweight="bold", y=0.98)

        wizard_offsets = {}
        offsets = np.linspace(0.1, 0.6, len(wizard_origins))
        for i, wizard in enumerate(wizard_origins):
            wizard_offsets[wizard] = ((-1) ** i) * offsets[i // 2]

        #Makes here the base network like the nodes, dashed edges, and labels
        nx.draw_networkx_nodes(
            G, layout, ax=main_ax, node_size=700,
            node_color="lightblue", edgecolors="navy", linewidths=2
        )
        nx.draw_networkx_edges(
            G, layout, ax=main_ax,
            edge_color="gray", width=1.5, style="dashed",
            arrowstyle="->", arrowsize=15, alpha=0.7
        )
        nx.draw_networkx_labels(G, layout, ax=main_ax, font_size=12, font_weight="bold")

        #MAkes the labels here
        edge_labels = {(u, v): f"{d['distance']} km" for u, v, d in G.edges(data=True)}
        legend_items, table_rows = [], []

        #Loops each wizard's route
        for wizard, (path, cost) in wizard_paths[metric].items():
            if not path or cost is None:
                continue

            #Gets the wizard color and determine the curve for the route
            color = wizard_colors.get(wizard, "black")
            curve = wizard_offsets.get(wizard, 0.0)
            edges = [(path[i], path[i+1]) for i in range(len(path)-1)]

            #Make wizard's route on the graph
            nx.draw_networkx_edges(
                G, layout, ax=main_ax,
                edgelist=edges,
                edge_color=color,
                width=5,
                arrows=True,
                arrowstyle="-|>",
                arrowsize=30,
                connectionstyle=f"arc3,rad={curve}"
            )

            #marks starting point of the wizards route
            if path[0] in layout:
                marker = {
                    "Harry Potter": "o",
                    "Hermione Granger": "s",
                    "Ron Weasley": "^",
                    "Luna Lovegood": "D",
                    "Neville Longbottom": "p",
                    "Ginny Weasley": "h"
                }.get(wizard, "o")
                main_ax.scatter(
                    *layout[path[0]],
                    s=300, marker=marker, color=color,
                    edgecolors="black", zorder=90
                )

            #Adds wizards info to the legend and table lists
            origin = wizard_origins.get(wizard, "Unknown")
            if origin == "Newfoundland and Labrador":
                origin = "NL"
            unit = metric_units[metric]
            formatted_cost = f"{cost} {unit}" if unit else f"{cost}"
            legend_text = f"{wizard} ({origin}): {formatted_cost}"
            legend_items.append(mpatches.Patch(color=color, label=legend_text))

        #Adds legend to the figure
        if legend_items:
            legend_ax.legend(handles=legend_items, loc="center", fontsize=11, framealpha=0.9)

        nx.draw_networkx_edge_labels(
            G, layout, ax=main_ax,
            edge_labels=edge_labels,
            font_size=9, font_weight="bold",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.8),
            rotate=False
        )

        main_ax.axis("off")

        #gives a explanation text and display the figure
        explanations = {
            "SHP": "Fewest hops between provinces.",
            "SDP": "Least distance between provinces.",
            "STP": "Shortest travel time.",
            "FDP": "Fewest dementor encounters."
        }
        plt.figtext(0.5, 0.92, explanations[metric], ha="center", fontsize=14, style="italic")
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.subplots_adjust(top=0.85)
        plt.show()



if __name__ == "__main__":
    #defines magical paths
    spell_routes = [
        {"start": "British Columbia", "end": "Saskatchewan", "hops": 13, "distance": 1800, "time": 19, "dementors": 6},
        {"start": "Alberta", "end": "Quebec", "hops": 3, "distance": 2000, "time": 21, "dementors": 7},
        {"start": "Ontario", "end": "Nova Scotia", "hops": 2, "distance": 1300, "time": 13, "dementors": 4},
        {"start": "Quebec", "end": "NL", "hops": 13, "distance": 1900, "time": 20, "dementors": 26},
        {"start": "Nova Scotia", "end": "Saskatchewan", "hops": 2, "distance": 1800, "time": 18, "dementors": 5},
        {"start": "Alberta", "end": "Saskatchewan", "hops": 6, "distance": 1600, "time": 8, "dementors": 3},
        {"start": "NL", "end": "Alberta", "hops": 4, "distance": 2400, "time": 24, "dementors": 9},
        {"start": "Ontario", "end": "Quebec", "hops": 10, "distance": 500, "time": 5, "dementors": 1},
        {"start": "Nova Scotia", "end": "Ontario", "hops": 3, "distance": 2000, "time": 21, "dementors": 7},
        {"start": "Saskatchewan", "end": "Nova Scotia", "hops": 3, "distance": 2000, "time": 20, "dementors": 37},
        {"start": "Quebec", "end": "Saskatchewan", "hops": 4, "distance": 200, "time": 2, "dementors": 0},
        {"start": "Alberta", "end": "Ottawa", "hops": 3, "distance": 2400, "time": 24, "dementors": 9},
        {"start": "Saskatchewan", "end": "Quebec", "hops": 2, "distance": 2000, "time": 20, "dementors": 6},
        {"start": "Ontario", "end": "Alberta", "hops": 2, "distance": 1500, "time": 16, "dementors": 4},
        {"start": "British Columbia", "end": "Saskatchewan", "hops": 2, "distance": 1200, "time": 14, "dementors": 3},
        {"start": "NL", "end": "Quebec", "hops": 3, "distance": 2200, "time": 22, "dementors": 7},
        {"start": "Nova Scotia", "end": "NL", "hops": 10, "distance": 1200, "time": 12, "dementors": 6},
        {"start": "Quebec", "end": "Ottawa", "hops": 29, "distance": 1800, "time": 19, "dementors": 17},
        {"start": "Alberta", "end": "British Columbia", "hops": 2, "distance": 1800, "time": 18, "dementors": 27},
        {"start": "British Columbia", "end": "Quebec", "hops": 2, "distance": 1900, "time": 19, "dementors": 7},
        {"start": "Ontario", "end": "NL", "hops": 3, "distance": 2300, "time": 23, "dementors": 8},
        {"start": "Nova Scotia", "end": "Alberta", "hops": 3, "distance": 2200, "time": 22, "dementors": 8},
        {"start": "NL", "end": "Alberta", "hops": 3, "distance": 2300, "time": 23, "dementors": 8},
        {"start": "Alberta", "end": "NL", "hops": 3, "distance": 2400, "time": 24, "dementors": 9},
        {"start": "Saskatchewan", "end": "British Columbia", "hops": 3, "distance": 2000, "time": 21, "dementors": 8},
        {"start": "Ontario", "end": "Saskatchewan", "hops": 2, "distance": 1600, "time": 16, "dementors": 5},
        {"start": "Quebec", "end": "Nova Scotia", "hops": 2, "distance": 1000, "time": 10, "dementors": 2},
        {"start": "NL", "end": "Saskatchewan", "hops": 4, "distance": 2200, "time": 23, "dementors": 19},
        {"start": "Nova Scotia", "end": "Quebec", "hops": 2, "distance": 1100, "time": 11, "dementors": 2},
        {"start": "British Columbia", "end": "NL", "hops": 4, "distance": 2500, "time": 26, "dementors": 10},
        {"start": "Ontario", "end": "Ottawa", "hops": 7, "distance": 1450, "time": 4, "dementors": 12},
        {"start": "Alberta", "end": "Saskatchewan", "hops": 5, "distance": 600, "time": 8, "dementors": 3},
        {"start": "Quebec", "end": "Alberta", "hops": 2, "distance": 1700, "time": 17, "dementors": 6},
        {"start": "Saskatchewan", "end": "Nova Scotia", "hops": 9, "distance": 1800, "time": 18, "dementors": 5},
        {"start": "Alberta", "end": "Quebec", "hops": 6, "distance": 2000, "time": 21, "dementors": 6},
        {"start": "Nova Scotia", "end": "British Columbia", "hops": 4, "distance": 2500, "time": 26, "dementors": 10},
        {"start": "Ontario", "end": "Nova Scotia", "hops": 12, "distance": 1300, "time": 13, "dementors": 4},
        {"start": "British Columbia", "end": "Saskatchewan", "hops": 13, "distance": 1800, "time": 19, "dementors": 6}
    ]

    #Makes the Hogwarts graph and add the defined paths
    map = HogwartsMap()
    map.build_map(spell_routes)

    #Starting locations
    wizards = {
        "Harry Potter": "British Columbia",
        "Hermione Granger": "Ontario",
        "Ron Weasley": "Quebec",
        "Luna Lovegood": "NL",
        "Neville Longbottom": "Saskatchewan",
        "Ginny Weasley": "Nova Scotia"
    }
    final_stop = "Ottawa"

    wizard_routes = {
        "SHP": {},
        "SDP": {},
        "STP": {},
        "FDP": {}
    }

    #prints out the best routes for each wizard
    for wizard, start in wizards.items():
        print("------------------------------------------------------------")
        print(f"Routes for {wizard} from {start} to {final_stop}")
        print("------------------------------------------------------------")

        shp = map.find_fewest_hops_path(start, final_stop)
        wizard_routes["SHP"][wizard] = (shp, len(shp) - 1 if shp else None)
        print("Shortest Hop Path (SHP):")
        print("  " + " → ".join(shp) + f"  ({len(shp)-1} hops)") if shp else print("  No route found.")

        sdp, dist = map.find_shortest_distance_path(start, final_stop)
        wizard_routes["SDP"][wizard] = (sdp, dist)
        print("Shortest Distance Path (SDP):")
        print("  " + " → ".join(sdp) + f"  ({dist} km)") if sdp else print("  No route found.")

        stp, time = map.find_fastest_time_path(start, final_stop)
        wizard_routes["STP"][wizard] = (stp, time)
        print("Shortest Time Path (STP):")
        print("  " + " → ".join(stp) + f"  ({time} hrs)") if stp else print("  No route found.")

        fdp, dementors = map.find_least_dementors_path(start, final_stop)
        wizard_routes["FDP"][wizard] = (fdp, dementors)
        print("Fewest Dementors Path (FDP):")
        print("  " + " → ".join(fdp) + f"  ({dementors} dementors)") if fdp else print("  No route found.")

        print("------------------------------------------------------------\n")

    #Create the wizard routes on the graph
    show_wizard_routes(map, wizard_routes, wizards)
