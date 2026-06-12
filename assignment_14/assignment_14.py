import sys
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.link = None

    def __del__(self):
        print(f"[Cleanup] Node '{self.name}' has been destroyed.")

def demonstrate_cycle():
    print("--- 1. Creating Nodes ---")
    node_a = Node("A")
    node_b = Node("B")
    
    print(f"Ref count for A: {sys.getrefcount(node_a)}")
    print(f"Ref count for B: {sys.getrefcount(node_b)}")

    print("\n--- 2. Creating the Cycle ---")

    node_a.link = node_b
    node_b.link = node_a

    print(f"Ref count for A after cycle: {sys.getrefcount(node_a)}")
    print(f"Ref count for B after cycle: {sys.getrefcount(node_b)}")

    id_a = id(node_a)
    id_b = id(node_b)

    print("\n--- 3. Deleting Variables (The 'Deletion') ---")
    del node_a
    del node_b
    print("Called 'del node_a' and 'del node_b'. Notice that the destructors have NOT run yet!")

    print("\n--- 4. The Investigation ---")
    found_a = False
    found_b = False
    for obj in gc.get_objects():
        if id(obj) == id_a:
            found_a = True
        elif id(obj) == id_b:
            found_b = True

    print(f"Is Node A still in memory? {found_a}")
    print(f"Is Node B still in memory? {found_b}")
    print("Even though we deleted the variables, the cycle keeps them alive in memory.")

    print("\n--- 5. The Cleanup ---")
    collected = gc.collect()
    print(f"Garbage collector run manually.")
    print(f"Number of unreachable objects collected: {collected}")

if __name__ == "__main__":
    gc.disable()
    
    demonstrate_cycle()
    
    gc.enable()