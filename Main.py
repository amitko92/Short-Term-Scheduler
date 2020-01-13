import sys


def FCFS(processes):
    ready_queue = []
    clock_time = 0
    while not check_if_all_processes_done(processes):
        check_if_process_arrive(clock_time, ready_queue, processes, 'insert_to_the_end', False)
        deal_with_zero_computation_time(clock_time, ready_queue)
        if len(ready_queue) > 0:
            ready_queue[0]['run_time'] -= 1
        clock_time += 1
    print("FCFS: ",
          sum([process['finishing_time'] - process['arrival_time'] for process in processes]) / len(processes))


def LCFS_not_preemptive(processes):
    ready_queue = []
    clock_time = 0
    while not check_if_all_processes_done(processes):
        check_if_process_arrive(clock_time, ready_queue, processes, 'insert_to_the_start', False)
        deal_with_zero_computation_time(clock_time, ready_queue)
        if len(ready_queue) > 0:
            ready_queue[0]['run_time'] -= 1
        clock_time += 1
    print("LCFS not preemptive: ",
          sum([process['finishing_time'] - process['arrival_time'] for process in processes]) / len(processes))


def LCFS_preemptive(processes):
    ready_queue = []
    clock_time = 0
    while not check_if_all_processes_done(processes):
        check_if_process_arrive(clock_time, ready_queue, processes, 'insert_to_the_start', True)
        deal_with_zero_computation_time(clock_time, ready_queue)
        if len(ready_queue) > 0:
            ready_queue[0]['run_time'] -= 1
        clock_time += 1
    print("LCFS preemptive: ",
          sum([process['finishing_time'] - process['arrival_time'] for process in processes]) / len(processes))


def RR(processes):
    ready_queue = []
    clock_time = 0
    while not check_if_all_processes_done(processes):
        for i in range(clock_time):
            check_if_process_arrive(i, ready_queue, processes, 'insert_to_the_start', True)

        if not check_if_all_processes_done(ready_queue):
            for process in ready_queue:
                if not process['done']:
                    if process['run_time'] == 0:
                        update_finishing_time(clock_time - 4, process)
                    elif process['run_time'] == 1:
                        update_finishing_time(clock_time, process)
                        process['run_time'] -= 1
                        clock_time += 1
                    elif process['run_time'] == 2:
                        update_finishing_time(clock_time + 1, process)
                        process['run_time'] -= 2
                        clock_time += 2
                    elif process['run_time'] >= 2:
                        clock_time += 2
                        process['run_time'] -= 2
        else:
            clock_time += 1
    print("RR: ", sum([process['finishing_time'] - process['arrival_time'] for process in processes]) / len(processes))


def SJF(processes):
    ready_queue = []
    clock_time = 0
    while not check_if_all_processes_done(processes):
        check_if_process_arrive(clock_time, ready_queue, processes, 'insert_to_the_start', True)
        if len(ready_queue) > 0:
            ready_queue.sort(key=lambda x: x['run_time'])
            deal_with_zero_computation_time(clock_time, ready_queue)
            if len(ready_queue) > 0:
                ready_queue[0]['run_time'] -= 1
        clock_time += 1
    print("SJF: ", sum([process['finishing_time'] - process['arrival_time'] for process in processes]) / len(processes))


def load_processes(input_user):
    pro = []

    for line in open(input_user, 'r'):
        if ',' in line:
            pro.append({
                'arrival_time': int(line.rstrip().split(',')[0]),
                'computation_time': int(line.rstrip().split(',')[1]),
                'finishing_time': 0,
                'in_ready_queue': False,
                'run_time': 0,
                'turn_around_time': 0,
                'done': False,
            })
    return sorted(pro, key=lambda p: p['arrival_time'])


def check_if_process_arrive(clock, ready_queue, processes, index, preemptive):
    for process in processes:
        if process['arrival_time'] == clock and not process['in_ready_queue']:
            process['in_ready_queue'] = True
            process['run_time'] = process['computation_time']
            if index == 'insert_to_the_start' and preemptive:
                ready_queue.insert(0, process)
            elif index == 'insert_to_the_start' and not preemptive:
                ready_queue.insert(1, process)
            else:
                ready_queue.append(process)


def check_if_all_processes_done(processes):
    for process in processes:
        if not process['done']:
            return False
    return True


def deal_with_zero_computation_time(clock_time, ready_queue):
    while len(ready_queue) > 0 and ready_queue[0]['run_time'] == 0:
        update_finishing_time(clock_time, ready_queue[0])
        ready_queue.pop(0)


def update_finishing_time(clock_time, process):
    process['finishing_time'] = clock_time
    process['done'] = True
    process['turn_around_time'] = process['finishing_time'] - process['arrival_time']


def run_scheduler(input_path):
    processes = load_processes(input_path)

    FCFS([process.copy() for process in processes])
    LCFS_not_preemptive([process.copy() for process in processes])
    LCFS_preemptive([process.copy() for process in processes])
    RR([process.copy() for process in processes])
    SJF([process.copy() for process in processes])


if __name__ == '__main__':
    input_path = sys.argv[1]
    run_scheduler(input_path)

# run_scheduler("input1.txt")
