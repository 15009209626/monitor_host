import psutil
import datetime
import csv
import traceback
import os


class Monitor(object):
    def __init__(self, interval):
        self.__interval = interval

    # monitor cup information
    def monitor_cpu(self, time):
        cup_usage = str(float(psutil.cpu_percent(self.__interval))) + "%"
        cpu_info = {
            'current_time': str(time),
            'cup_usage': cup_usage
        }
        return cpu_info

    # monitor memory information
    @staticmethod
    def monitor_memory(time):
        mem_total = str(int(psutil.virtual_memory()[0] / 1024 / 1024)) + 'MB'
        mem_used = str(int(psutil.virtual_memory()[3] / 1024 / 1024)) + 'MB'
        mem_usage = str(float(psutil.virtual_memory()[2])) + '%'
        mem_info = {
            'current_time': str(time),
            'mem_total': mem_total,
            'mem_used': mem_used,
            'mem_per': mem_usage
        }
        return mem_info

    # monitor disk space and usage information
    @staticmethod
    def monitor_io(time):
        disk = psutil.disk_partitions()
        io_info = {}
        for i in disk:
            io_device = i.device
            disk_use = psutil.disk_usage(io_device)
            io_used = disk_use.used / 1024 / 1024
            io_free = disk_use.free / 1024 / 1024
            io_total = disk_use.total / 1024 / 1024
            io_usage_percent = disk_use.percent
            io_info['current_time'] = str(time)
            io_info[str(io_device) + 'device'] = io_device
            io_info[str(io_device) + 'total'] = io_total
            io_info[str(io_device) + 'used'] = io_used
            io_info[str(io_device) + 'free'] = io_free
            io_info[str(io_device) + 'usage'] = io_usage_percent
        return io_info

    # monitor network information
    @staticmethod
    def monitor_network(time):
        count = psutil.net_io_counters()
        byte_sent = bytes2human(count.bytes_sent)
        byte_receive = bytes2human(count.bytes_recv)
        packet_sent = bytes2human(count.packets_sent)
        packet_receive = bytes2human(count.packets_recv)
        network_info = {
            'current_time': str(time),
            'byte_sent': byte_sent,
            'byte_receive': byte_receive,
            'packet_sent': packet_sent,
            'packet_receive': packet_receive
        }
        return network_info


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            #return '%.2f %s' % (value, s)
            return '%.2f' % (value)
    return '%.2f B' % (n)


def write_to_csv(file_path, result, filename_list):
    try:
        for filename in range(len(filename_list)):
            with open(file_path + filename_list[filename], 'a', encoding='utf-8', newline='' "") as file:
                csv_writer = csv.writer(file)
                tittle = []
                value = []
                for item, val in result[filename].items():
                    tittle.append(item)
                    value.append(val)
                if not os.path.getsize(file_path + filename_list[filename]):
                    csv_writer.writerow(tittle)
                    csv_writer.writerow(value)
                else:
                    csv_writer.writerow(value)
    except Exception as e:
        print('e.args:\t', e.args)
        print('traceback.format_exc():\n%s' % traceback.format_exc())

if __name__ == '__main__':
    # define monitor term 0==false or  1==true
    enable_memory = 1
    enable_cup = 1
    enable_io = 1
    enable_network = 1

    # default capture interval and times
    default_interval = 1
    default_times = 1 * 5

    filename_list = ['cpu_monitor.csv', 'mem_monitor.csv', 'io_monitor.csv', 'net_monitor.csv']
    result = []
    monitor = Monitor(default_interval)
    path = os.getcwd() + "\\monitor_result\\"

    while default_times:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # get cup information
        if enable_cup:
            cpu_result = monitor.monitor_cpu(current_time)
            result.append(cpu_result)

        # get memory information
        if enable_memory:
            memory_result = monitor.monitor_memory(current_time)
            result.append(memory_result)

        # get io information
        if enable_io:
            io_result = monitor.monitor_io(current_time)
            result.append(io_result)

        # get network information
        if enable_network:
            network_result = monitor.monitor_network(current_time)
            result.append(network_result)

        # write data into csv files
        write_to_csv(path, result, filename_list)
        result.clear()
        default_times -= 1



