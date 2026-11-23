import requests
import time
import csv
import base64
import subprocess
from pathlib import Path

# node configuration
# IP addresses are the Toxiproxy sidecar addresses advertised by Consul.
NODES = {
    "consul1": {
        "port": 8511,
        "ip": "10.99.0.2",
        "helper": "toxiproxy-netadmin1"
    },
    "consul2": {
        "port": 8512,
        "ip": "10.99.0.3",
        "helper": "toxiproxy-netadmin2"
    },
    "consul3": {
        "port": 8513,
        "ip": "10.99.0.4",
        "helper": "toxiproxy-netadmin3"
    },
    "consul4": {
        "port": 8514,
        "ip": "10.99.0.5",
        "helper": "toxiproxy-netadmin4"
    },
    "consul5": {
        "port": 8515,
        "ip": "10.99.0.6",
        "helper": "toxiproxy-netadmin5"
    },
}

KEY = "exercise2/conflict-demo"
MINORITY_VALUE = "minority-write"
MAJORITY_VALUE = "majority-write"
OUTPUT_DIR = Path("exercise2-files")
CSV_FILE = OUTPUT_DIR / "exercise2-results.csv"
TIMEOUT = 180

# consul config
def api(node, endpoint):
    return f"http://localhost:{NODES[node]['port']}{endpoint}"

def get_leader(node):
    try:
        r = requests.get(
            api(node, "/v1/status/leader"),
            timeout=4
        )
        r.raise_for_status()
        address = r.json().strip().strip('"')
        return address.rsplit(":", 1)[0] if address else None
    except requests.RequestException:
        return None

def wait_for_cluster():
    print("\nWaiting for five-node cluster...")
    deadline = time.time() + TIMEOUT
    while time.time() < deadline:
        leaders = [get_leader(n) for n in NODES]
        if all(leaders) and len(set(leaders)) == 1:
            print("Cluster ready.")
            return
        time.sleep(3)
    raise TimeoutError(
        "Five-node cluster is not ready. Timeout."
    )

def node_from_ip(ip):
    for node, info in NODES.items():
        if info["ip"] == ip:
            return node
    return "Unknown"

def write_value(node, value):
    try:
        r = requests.put(
            api(node, f"/v1/kv/{KEY}"),
            data=value,
            timeout=10
        )
        return f"HTTP {r.status_code}"
    except requests.RequestException as e:
        return f"FAILED: {str(e)[:100]}"

def read_value(node):
    try:
        r = requests.get(
            api(node, f"/v1/kv/{KEY}?consistent"),
            timeout=5
        )
        if r.status_code == 404:
            return "No value"
        r.raise_for_status()
        data = r.json()
        if not data or data[0].get("Value") is None:
            return "No value"
        return base64.b64decode(
            data[0]["Value"]
        ).decode("utf-8")
    except requests.RequestException:
        return "Unavailable"
    except (ValueError, KeyError, IndexError):
        return "Read error"

# partition
def docker_exec(helper, command):
    result = subprocess.run(
        [
            "docker",
            "exec",
            helper,
            "sh",
            "-c",
            command
        ],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"{helper}: {result.stderr.strip()}"
        )
def apply_partition(minority, majority):
    print("\nCreating 3-2 network partition...")
    minority_ips = {
        NODES[n]["ip"] for n in minority
    }
    majority_ips = {
        NODES[n]["ip"] for n in majority
    }
    for node, info in NODES.items():
        helper = info["helper"]
        # iptables.
        docker_exec(
            helper,
            "iptables -N RAFT_EX2 2>/dev/null || true; "
            "iptables -F RAFT_EX2; "
            "iptables -C INPUT -j RAFT_EX2 2>/dev/null "
            "|| iptables -I INPUT -j RAFT_EX2; "
            "iptables -C OUTPUT -j RAFT_EX2 2>/dev/null "
            "|| iptables -I OUTPUT -j RAFT_EX2"
        )
        # identify partition.
        if node in minority:
            blocked_ips = majority_ips
        else:
            blocked_ips = minority_ips
        # block incoming and outgoing traffic to the other partition.
        for ip in blocked_ips:
            docker_exec(
                helper,
                f"iptables -A RAFT_EX2 -s {ip} -j DROP"
            )
            docker_exec(
                helper,
                f"iptables -A RAFT_EX2 -d {ip} -j DROP"
            )
    print("Partition established.")
def heal_partition():
    print("\nHealing network partition...")
    for info in NODES.values():
        docker_exec(
            info["helper"],
            "iptables -F RAFT_EX2 2>/dev/null || true"
        )
    print("Network connectivity restored.")

# majority leader
def find_majority_leader(majority):
    print("\nWaiting for majority leader...")
    deadline = time.time() + TIMEOUT
    while time.time() < deadline:
        leaders = [
            get_leader(n) for n in majority
        ]
        valid = [ip for ip in leaders if ip]
        if len(valid) >= 2 and len(set(valid)) == 1:
            leader = node_from_ip(valid[0])
            if leader in majority:
                print("Majority leader is:", leader)
                return leader
        time.sleep(2)
    raise TimeoutError("Majority leader not found.")


# results
def record_phase(
        writer,
        phase,
        minority,
        majority,
        minority_leader,
        majority_leader
):
    snapshot = {}
    for node in NODES:
        leader_ip = get_leader(node)
        leader = (
            node_from_ip(leader_ip)
            if leader_ip else "Unknown"
        )
        value = read_value(node)

        group = (
            "Minority" if node in minority
            else "Majority" if node in majority
            else "Connected"
        )
        snapshot[node] = {
            "leader": leader,
            "value": value
        }
        writer.writerow({
            "Phase": phase,
            "Node": node,
            "Partition": group,
            "Reported Leader": leader,
            "Minority Leader": minority_leader,
            "Majority Leader": majority_leader,
            "Observed Value": value
        })
    return snapshot


# table display
def display_table(
        snapshots,
        minority,
        majority,
        minority_leader,
        majority_leader
):
    nodes = list(NODES.keys())
    headers = [
                  "Phase"
              ] + [
                  f"{node} ({'Minority' if node in minority else 'Majority'})"
                  for node in nodes
              ] + [
                  "Raft Mechanism Observed"
              ]
    rows = []

    phase_names = [
        "Active (Partition On)",
        "Heals (Reconnected)",
        "Reconciled (Post-Recovery)"
    ]
    mechanisms = [
        "Minority lacks quorum (2/5); majority elects a leader and accepts the write.",
        "Network connectivity is restored; nodes begin recognizing the current leader.",
        "All five nodes converge on the majority value."
    ]
    for i, phase in enumerate(phase_names):
        row = [phase]
        for node in nodes:
            leader = snapshots[i][node]["leader"]
            value = snapshots[i][node]["value"]
            row.append(
                f"Leader: {leader}; Value: {value}"
            )
        row.append(mechanisms[i])
        rows.append(row)
    widths = [29] + [35] * 5 + [70]
    def print_row(values):
        print(
            "| " +
            " | ".join(
                str(v)[:w].ljust(w)
                for v, w in zip(values, widths)
            ) +
            " |"
        )
    print("\n\nExercise 2: Five-Node Log Lifecycle Trace Table\n")
    print_row(headers)
    print("-" * (sum(widths) + 3 * len(widths) + 1))
    for row in rows:
        print_row(row)

# main
def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    fields = [
        "Phase",
        "Node",
        "Partition",
        "Reported Leader",
        "Minority Leader",
        "Majority Leader",
        "Observed Value"
    ]
    snapshots = []
    partition_active = False
    with CSV_FILE.open(
            "w",
            newline="",
            encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fields
        )
        writer.writeheader()
        try:
            # find og leader.
            wait_for_cluster()
            initial_ip = get_leader("consul1")
            minority_leader = node_from_ip(initial_ip)
            if minority_leader not in NODES:
                raise RuntimeError(
                    "Could not identify original leader."
                )
            # form minority.
            minority = [
                minority_leader,
                next(
                    n for n in NODES
                    if n != minority_leader
                )
            ]
            # form majority.
            majority = [
                n for n in NODES
                if n not in minority
            ]
            print("\nMinority nodes:", minority)
            print("Majority nodes:", majority)
            # partition.
            apply_partition(minority, majority)
            partition_active = True
            time.sleep(8)
            # find new majority leader.
            majority_leader = find_majority_leader(
                majority
            )

            # attempt minority write.
            print("\nAttempting minority write...")
            minority_result = write_value(
                minority_leader,
                MINORITY_VALUE
            )
            print("Minority write:", minority_result)
            # attempt majority write.
            print("\nAttempting majority write...")
            majority_result = write_value(
                majority_leader,
                MAJORITY_VALUE
            )
            print("Majority write:", majority_result)
            # Record active partition phase.
            snapshots.append(
                record_phase(
                    writer,
                    "Active Partition",
                    minority,
                    majority,
                    minority_leader,
                    majority_leader
                )
            )
            # heal network.
            heal_partition()
            partition_active = False
            time.sleep(5)
            snapshots.append(
                record_phase(
                    writer,
                    "Heals/Reconnected",
                    minority,
                    majority,
                    minority_leader,
                    majority_leader
                )
            )
            print("\nWaiting for cluster convergence...")
            deadline = time.time() + 90
            converged = False
            while time.time() < deadline:
                values = [
                    read_value(n) for n in NODES
                ]
                if all(
                        v == MAJORITY_VALUE
                        for v in values
                ):
                    converged = True
                    break
                time.sleep(2)
            snapshots.append(
                record_phase(
                    writer,
                    "Reconciled/Post-Recovery",
                    minority,
                    majority,
                    minority_leader,
                    majority_leader
                )
            )
            if converged:
                print("\nSUCCESS: All five nodes converged.")
            else:
                print(
                    "\nWARNING: All nodes did not converge "
                    "before timeout."
                )
            # deliverable table.
            display_table(
                snapshots,
                minority,
                majority,
                minority_leader,
                majority_leader
            )
        finally:
            if partition_active:
                heal_partition()
    print("\nCSV results saved to:", CSV_FILE)
if __name__ == "__main__":
    main()


