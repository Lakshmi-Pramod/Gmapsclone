import time

class Node:
    def __init__(self, node_id, all_nodes):
        self.node_id = node_id
        self.all_nodes = sorted(all_nodes)  # Only consider currently active nodes
        self.leader = None

    def start_election(self):
        print(f"🔄 Node {self.node_id} is starting an election.")
        higher_nodes = [n for n in self.all_nodes if n > self.node_id]

        if not higher_nodes:
            self.leader = self.node_id
            print(f"🏆 Node {self.node_id} is the leader.")
        else:
            for node in higher_nodes:
                print(f"✅ Node {node} responded. Leader remains {node}.")
                self.leader = node
                return  # Higher node will take over the election

        print(f"🏆 Node {self.node_id} is the new leader.")

