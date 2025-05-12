# ✨ Harry Potter Reunion – Magical Pathfinding in Python

This project simulates a magical journey across Canada, helping Harry Potter and his friends reach a reunion in Ottawa. Each character starts in a different province, and your task is to find the best magical path for each of them while avoiding Dementors and minimizing travel costs.

---

## 🧭 What It Does

- Models Canadian provinces and magical paths as a **graph**.
- Calculates four types of best paths from each starting location to **Ottawa**:
  - **Shortest Hop Path (SHP)**: Fewest number of magical connections.
  - **Shortest Distance Path (SDP)**: Lowest total travel distance.
  - **Shortest Time Path (STP)**: Fastest total travel time.
  - **Fewest Dementors Path (FDP)**: Safest path with minimal danger.
- Uses common **pathfinding algorithms** like BFS and Dijkstra’s.
- Creates a **visual map** of the network using Python graphing libraries.

---

## 🧙 Characters and Starting Locations

- **Harry Potter** – British Columbia  
- **Hermione Granger** – Ontario  
- **Ron Weasley** – Quebec  
- **Luna Lovegood** – Newfoundland and Labrador  
- **Neville Longbottom** – Saskatchewan  
- **Ginny Weasley** – Nova Scotia  

---

## 📊 Magical Path Graph Info

Provinces are modeled as **nodes**, and magical paths are **edges** with four properties:
- Hops
- Distance (km)
- Time (hours)
- Dementors (danger level)

Example:
```
British Columbia -> Saskatchewan: 
  Hops: 2
  Distance: 1200 km
  Time: 14 hrs
  Dementors: 3
```

---

## 🛠 How to Run

1. **Install Python 3**
   Make sure Python 3 is installed on your machine.

2. **Install Required Libraries**
   This project may use `networkx` and `matplotlib` for visualization:
   ```bash
   pip install networkx matplotlib
   ```

3. **Run the Script**
   In your terminal, run:
   ```bash
   python harry_potter_reunion.py
   ```

4. **View Output**
   - The console will display each character’s best path to Ottawa using SHP, SDP, STP, and FDP.
   - A network diagram will be shown illustrating the magical graph.

---

## 🧮 Algorithms Used

- **Breadth First Search (BFS)** for Shortest Hop Path.
- **Dijkstra’s Algorithm** for Distance, Time, and Dementor-weighted paths.

You can modify the code to try other algorithms like DFS or A* for additional learning.

---

## 🔍 Example Output Format

```
Harry Potter (British Columbia) to Ottawa:
- SHP: BC → AB → Ottawa
- SDP: BC → SK → QC → Ottawa (1800 km)
- STP: BC → SK → QC → Ottawa (19 hrs)
- FDP: BC → SK → QC → Ottawa (6 Dementors)

Visualization generated in window.
```

---

## 📈 Graph Visualization

This project includes a network diagram using `networkx` and `matplotlib`. Edges can be styled based on:
- Weight type (distance, time, or danger).
- Color-coded paths per alumnus.

---

## 💡 Extras You Can Add

- Highlight each path with a different color in the graph.
- Let users select which metric to optimize.
- Add a GUI or command-line input for custom journeys.
- Track total metrics (e.g., how many Dementors avoided total).

---

## 📁 File Structure

```
project-folder/
├── harry_potter_reunion.py   # Main script
├── reunion_graph.png         # Optional: saved graph output
├── README.md                 # This file
```

---

## 🧠 Tips

- Ottawa is the target node.
- Start by loading the graph data (edges) into a dictionary or adjacency list.
- Keep separate weights for distance, time, and Dementors for each edge.
- Use priority queues for Dijkstra-based calculations.

---

Join Harry and friends in this cross-country magical journey — and make sure they all arrive safely at the reunion! 🧙‍♂️🧙‍♀️📍
