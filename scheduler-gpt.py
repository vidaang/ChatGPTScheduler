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

def sapce_size(time):
    space = "   "
    size = len(space)
    count = 10

    if (time >= count):
        space = space[:(size-1)]
    
    if (time > count*count):
        space = space[:(size-1)]

    return space

def sapce_size_process_count(time):
    space = "  "
    size = len(space)
    count = 10

    if (time >= count):
        space = space[:(size-1)]
    
    if (time > count*count):
        space = space[:(size-1)]

    return space

def process_arrived(process_list, log, time, ready_queue):
     # Add any arriving processes to the ready queue
     for process in process_list:
         if process.arrival == time:
             log.append(f"Time{sapce_size(time)}{time} : {process.name} arrived")
             ready_queue.append(process)
             

# Function to simulate First In, First Out (FIFO)
def fcfs_scheduling(process_list, runtime):
    time = 0
    log = []
    ready_queue = []
    process_list.sort(key=lambda p: p.arrival)  # Sort processes by arrival time
    current_process = None
    already_arrived = False
    
    while time < runtime:
        if already_arrived:
             already_arrived = False
        else:
            process_arrived(process_list, log, time, ready_queue)

        # If no process is currently running, select the next one from the ready queue
        if current_process is None and ready_queue:
            current_process = ready_queue.pop(0)
            current_process.start_time = time
            log.append(f"Time{sapce_size(time)}{time} : {current_process.name} selected (burst{sapce_size(current_process.remaining_time)}{current_process.burst})")
        
        # If there is a current process, simulate its execution
        if current_process:
            current_process.remaining_time -= 1
            if current_process.remaining_time == 0:
                current_process.finish_time = time + 1
                process_arrived(process_list, log, time+1, ready_queue)
                already_arrived = True
                log.append(f"Time{sapce_size(time)}{time + 1} : {current_process.name} finished")
                current_process = None  # Process finished, no current process
        
        # If no process is selected, print Idle
        elif current_process is None and not ready_queue:
            log.append(f"Time{sapce_size(time)}{time} : Idle")

        time += 1

    # Handle processes that did not finish within the runtime
    for process in ready_queue:
        log.append(f"{process.name} did not finish")

    log.append(f"Finished at time  {time}")
    
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
            
            log.append(f"Time {time}: {current_process.name} selected (burst   {current_process.remaining_time})")
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
    notburst_flag = True
    already_arrived = False
    
    while time < runtime:
        if already_arrived:
             already_arrived = False
        else:
            process_arrived(process_list, log, time, ready_queue)
        
        if current_process is not None and q_time == quantum:
            if current_process.remaining_time > 0:
                ready_queue.append(current_process)
            q_time = 0
            current_process = None

        if not current_process and ready_queue:
            current_process = ready_queue.pop(0)
            q_time = 0
            notburst_flag = True
            if current_process.start_time == -1:
                current_process.start_time = time
            
        if current_process:
            if notburst_flag:
                log.append(f"Time{sapce_size(time)}{time} : {current_process.name} selected (burst{sapce_size(current_process.remaining_time)}{current_process.remaining_time})")
                notburst_flag = False
            current_process.remaining_time -= 1
            q_time += 1

            if current_process.remaining_time == 0:
                current_process.finish_time = time + 1
                process_arrived(process_list, log, time+1, ready_queue)
                already_arrived = True
                log.append(f"Time{sapce_size(time)}{time + 1} : {current_process.name} finished")
                current_process = None
                q_time = 0
                
        else:
            log.append(f"Time{sapce_size(time)}{time} : Idle")
        
        time += 1

    log.append(f"Finished at time  {time}")

    return log


# Function to calculate turnaround time, waiting time, and response time
def calculate_times(process_list):
    times_log = []
    process_list.sort(key=lambda p: p.name)

    for process in process_list:
        turnaround_time = process.finish_time - process.arrival
        waiting_time = turnaround_time - process.burst
        response_time = process.start_time - process.arrival
        times_log.append(f"{process.name} wait{sapce_size(waiting_time)}{waiting_time} turnaround{sapce_size(turnaround_time)}{turnaround_time} response{sapce_size(response_time)}{response_time}")
    return times_log

# Main function to handle input and scheduling selection
def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler.py <input file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not input_file.endswith(".in"):
        print(f"Error: Input file {input_file} must have '.in' extension")
        sys.exit(1)

    output_file = input_file.replace(".in", ".out")

    process_list, runtime, algorithm, quantum = parse_input(input_file)

    log = []
    log.append(f"{sapce_size_process_count(len(process_list))}{len(process_list)} processes")
    
    if algorithm == 'fcfs':
        log.append("Using First-Come First-Served")
        log.extend(fcfs_scheduling(process_list, runtime))

    elif algorithm == 'sjf':
        log.append("Using preemptive Shortest Job First")
        log.extend(sjf_scheduling(process_list, runtime))

    elif algorithm == 'rr':
        log.append("Using Round-Robin")
        log.append(f"Quantum   {quantum}\n")
        log.extend(round_robin_scheduling(process_list, runtime, quantum))
        
    else:
        print(f"Error: Unknown algorithm {algorithm}")
        sys.exit(1)
    
    log.append("")
    times_log = calculate_times(process_list)
    log.extend(times_log)

    # Write log to the output file
    with open(output_file, 'w') as out:
        for entry in log:
            out.write(entry + '\n')

if __name__ == "__main__":
    main()
