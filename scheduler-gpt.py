import sys

# Data structure to represent a process
class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_time = burst
        self.start_time = -1
        self.finish_time = -1

# Function to parse input file and create processes
def parse_input(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        process_list = []
        process_count = 0
        runtime = 0
        quantum = None
        algorithm = None

        for line in lines:
            words = line.split()

            if words[0] == 'processcount':
                process_count = int(words[1])
            elif words[0] == 'runfor':
                runtime = int(words[1])
            elif words[0] == 'use':
                algorithm = words[1]
            elif words[0] == 'quantum':
                quantum = int(words[1])
            elif words[0] == 'process':
                name = words[2]
                arrival = int(words[4])
                burst = int(words[6])
                process_list.append(Process(name, arrival, burst))
            elif words[0] == 'end':
                break
        
        # Check for missing parameters
        if algorithm == 'rr' and quantum is None:
            print("Error: Missing quantum parameter when use is 'rr'")
            sys.exit(1)

        return process_list, runtime, algorithm, quantum

    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        sys.exit(1)

# Function to simulate First In, First Out (FIFO)
def fifo_scheduling(process_list, runtime):
    process_list.sort(key=lambda p: p.arrival)  # Sort processes by arrival time
    time = 0
    log = []
    
    for process in process_list:
        if time < process.arrival:
            log.append(f"Time {time}: Idle")
            time = process.arrival
        
        process.start_time = time
        log.append(f"Time {time}: {process.name} selected (burst {process.burst})")
        
        time += process.burst
        process.finish_time = time
        log.append(f"Time {time}: {process.name} finished")

    while time < runtime:
        log.append(f"Time {time}: Idle")
        time += 1

    return log

# Function to simulate Preemptive Shortest Job First (SJF)
def sjf_scheduling(process_list, runtime):
    time = 0
    log = []
    ready_queue = []
    process_list.sort(key=lambda p: p.arrival)  # Sort by arrival time
    current_process = None
    
    while time < runtime:
        # Add new arrivals to the ready queue
        for process in process_list:
            if process.arrival == time:
                log.append(f"Time {time}: {process.name} arrived")
                ready_queue.append(process)
        
        # Sort ready queue by remaining time
        ready_queue.sort(key=lambda p: p.remaining_time)
        
        if current_process and current_process.remaining_time > 0:
            ready_queue.append(current_process)

        if ready_queue:
            current_process = ready_queue.pop(0)
            if current_process.start_time == -1:
                current_process.start_time = time
            
            log.append(f"Time {time}: {current_process.name} selected (burst {current_process.remaining_time})")
            current_process.remaining_time -= 1
            
            if current_process.remaining_time == 0:
                current_process.finish_time = time + 1
                log.append(f"Time {time + 1}: {current_process.name} finished")
        else:
            log.append(f"Time {time}: Idle")
        
        time += 1

    return log

# Function to simulate Round Robin (RR)
def round_robin_scheduling(process_list, runtime, quantum):
    time = 0
    log = []
    ready_queue = []
    process_list.sort(key=lambda p: p.arrival)  # Sort by arrival time
    current_process = None
    q_time = 0  # Quantum counter
    
    while time < runtime:
        # Add new arrivals to the ready queue
        for process in process_list:
            if process.arrival == time:
                log.append(f"Time {time}: {process.name} arrived")
                ready_queue.append(process)
        
        if current_process is not None and q_time == quantum:
            if current_process.remaining_time > 0:
                ready_queue.append(current_process)
            q_time = 0
            current_process = None

        if not current_process and ready_queue:
            current_process = ready_queue.pop(0)
            q_time = 0
            if current_process.start_time == -1:
                current_process.start_time = time
            
        if current_process:
            log.append(f"Time {time}: {current_process.name} selected (burst {current_process.remaining_time})")
            current_process.remaining_time -= 1
            q_time += 1

            if current_process.remaining_time == 0:
                current_process.finish_time = time + 1
                log.append(f"Time {time + 1}: {current_process.name} finished")
                current_process = None
                q_time = 0
        else:
            log.append(f"Time {time}: Idle")
        
        time += 1

    return log

# Function to calculate turnaround time, waiting time, and response time
def calculate_times(process_list):
    for process in process_list:
        turnaround_time = process.finish_time - process.arrival
        waiting_time = turnaround_time - process.burst
        response_time = process.start_time - process.arrival
        print(f"{process.name}: wait {waiting_time} turnaround {turnaround_time} response {response_time}")

# Main function to handle input and scheduling selection
def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler.py <input file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not input_file.endswith(".in"):
        print(f"Error: Input file {input_file} must have '.in' extension")
        sys.exit(1)

    process_list, runtime, algorithm, quantum = parse_input(input_file)

    print(f"{len(process_list)} processes")
    print(f"Using {algorithm.upper()}")
    
    if algorithm == 'fifo':
        log = fifo_scheduling(process_list, runtime)
    elif algorithm == 'sjf':
        log = sjf_scheduling(process_list, runtime)
    elif algorithm == 'rr':
        print(f"Quantum {quantum}")
        log = round_robin_scheduling(process_list, runtime, quantum)
    else:
        print(f"Error: Unknown algorithm {algorithm}")
        sys.exit(1)
    
    for entry in log:
        print(entry)
    
    calculate_times(process_list)

if __name__ == "__main__":
    main()
