import json
from collections import deque

def find_chromatic_geodesic():
    print("--- UBP v7.2: THE CHROMATIC GEODESIC (H -> Cf) ---")
    
    with open('elemental_chromatic_data.json', 'r') as f:
        elements = json.load(f)
    
    # 1. Build Adjacency Map (Hamming Distance <= 8)
    adj = {el['ubp_id']: [] for el in elements}
    id_to_name = {el['ubp_id']: el['name'] for el in elements}
    
    from core import BinaryLinearAlgebra
    
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            v1 = elements[i]['vector']
            v2 = elements[j]['vector']
            if BinaryLinearAlgebra.hamming_distance(v1, v2) <= 8:
                adj[elements[i]['ubp_id']].append(elements[j]['ubp_id'])
                adj[elements[j]['ubp_id']].append(elements[i]['ubp_id'])

    # 2. BFS for Shortest Path
    start_node = "ELEM_H_001"
    end_node = "ELEM_Cf_098"
    
    queue = deque([[start_node]])
    visited = {start_node}
    
    geodesic = []
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == end_node:
            geodesic = path
            break
            
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    # 3. Analyze the Path
    print(f"Geodesic Found! Length: {len(geodesic)} steps.")
    print("\n[THE PATH OF MATTER]")
    print("-" * 30)
    
    path_data = []
    for step, uid in enumerate(geodesic):
        el_data = next(e for e in elements if e['ubp_id'] == uid)
        print(f"Step {step:02d}: {id_to_name[uid]:<15} (Z={el_data['z']})")
        path_data.append({
            "step": step,
            "ubp_id": uid,
            "name": el_data['name'],
            "z": el_data['z']
        })

    # 4. Check for "Z-Jumps"
    # Does the path follow Z+1, or does it teleport across the table?
    z_diffs = [abs(path_data[i+1]['z'] - path_data[i]['z']) for i in range(len(path_data)-1)]
    avg_jump = sum(z_diffs) / len(z_diffs)
    
    print(f"\n[GEODESIC METRICS]")
    print(f"  Average Atomic Jump: {avg_jump:.2f} Z-units")
    
    if avg_jump < 5:
        print("✅ LINEAR GROWTH: Matter evolves sequentially.")
    else:
        print("🌀 NON-LINEAR FOLD: The Periodic Table is a folded manifold.")

    with open('chromatic_geodesic.json', 'w') as f:
        json.dump(path_data, f, indent=2)

if __name__ == "__main__":
    find_chromatic_geodesic()