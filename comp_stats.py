import psutil
import re

TEMPLATES = {
    'memory':{
        'all': 'Оперативная память: \n\tВсего оперативной памяти: {:.4} ГБ\n\t',
        'used': 'Используется: {:.4} ГБ\n\t',
        'free': 'Свободно: {:.4} ГБ\n\t',
        'total': 'Размер файла подкачки: {:.4} ГБ\n'
    },
    'disks': {
        'yes' : 'Диск {}, \n\topts: {},\n\tТип файловой системы: {}, \n\tРазмер: {:.4} ГБ, \n\tЗанято: {:.4} ГБ, {:.4}%, \n\tСвободно: {:.4}ГБ\n',
        'no' : 'Диск {}, \n\topts: {}\n'
    }
    
}

#   Получение данных об оперативной памяти
def get_memory():
    res = {
        'all': psutil.virtual_memory().total / 1024 / 1024 / 1024,
        'used': psutil.virtual_memory().used / 1024 / 1024 / 1024,
        'free': psutil.virtual_memory().free / 1024 / 1024 / 1024,
        'total': psutil.swap_memory().total / 1024 / 1024 / 1024
    }
    return res

def get_disks():
    res = {
            'diskpart': {
                'device': [],
                'fstype': [],
                'opts': []
            },
            'usage': {}
        }
    for disk in psutil.disk_partitions():
        s = re.match(r'.*([:\\/]?[a-z|A-Z]+[:\\/]?).*', disk.device)
        s = s.group(1)
        res['diskpart']['device'].append(s)
        res['diskpart']['fstype'].append(disk.fstype)
        res['diskpart']['opts'].append(disk.opts)
    for i, disk in enumerate(res['diskpart']['device']):
        if res['diskpart']['fstype'][i] != '':
            res['usage'][disk] = {}
            res['usage'][disk]['total'] = psutil.disk_usage(path=disk).total / 1024 / 1024 / 1024
            res['usage'][disk]['used'] = psutil.disk_usage(disk).used / 1024 / 1024 / 1024
            res['usage'][disk]['free'] = psutil.disk_usage(disk).free / 1024 / 1024 / 1024
            res['usage'][disk]['percent'] = psutil.disk_usage(disk).percent
    return res

def show():
    #   Представление данных об оперативной памяти
    memory = get_memory()
    template_memory = ""
    for key in memory.keys():
        template_memory += TEMPLATES['memory'][key].format(memory[key])
    print(template_memory)
    # Представление данных по информации дискового пространства
    partitions = get_disks()
    for i in range(len(partitions['diskpart']['device'])):
        part_str = ''
        disk = partitions['diskpart']['device'][i]
        if partitions['diskpart']['fstype'][i] != '':
            part_str = TEMPLATES['disks']['yes'].format(disk, partitions['diskpart']['opts'][i], partitions['diskpart']['fstype'][i], partitions['usage'][disk]['total'], partitions['usage'][disk]['used'], partitions['usage'][disk]['percent'], partitions['usage'][disk]['free'])
        else:
            part_str = TEMPLATES['disks']['no'].format(disk, partitions['diskpart']['opts'][i])
        print(part_str)

if __name__ == "__main__":
    show()