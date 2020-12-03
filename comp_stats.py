import psutil

TEMPLATES = {
    'memory':{
        'all': 'Оперативная память: \n\tВсего оперативной памяти: {:.4} ГБ\n\t',
        'used': 'Используется: {:.4} ГБ\n\t',
        'free': 'Свободно: {:.4} ГБ\n\t',
        'total': 'Размер файла подкачки: {:.4} ГБ\n'
    },
    'disks': {
        'disk_c': 'Диск С: \n\tРазмер: {:.4} ГБ, \n\tЗанято: {:.4} ГБ, \n\tСвободно: {:.4}ГБ\n',
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
        res['diskpart']['device'].append(disk.device)
        res['diskpart']['fstype'].append(disk.fstype)
        res['diskpart']['opts'].append(disk.opts)
    for i, disk in enumerate(res['diskpart']['device']):
        if res['diskpart']['fstype'][i] != '':
            res['usage'][disk[0]] = {}
            res['usage'][disk[0]]['total'] = psutil.disk_usage(path=disk[:2]).total / 1024 / 1024 / 1024
            res['usage'][disk[0]]['used'] = psutil.disk_usage(disk).used / 1024 / 1024 / 1024
            res['usage'][disk[0]]['free'] = psutil.disk_usage(disk).free / 1024 / 1024 / 1024
            res['usage'][disk[0]]['percent'] = psutil.disk_usage(disk).percent
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
    print(partitions)


if __name__ == "__main__":
    show()