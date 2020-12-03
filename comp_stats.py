import psutil

TEMPLATES = {
    'memory':{
        'all': 'Оперативная память: \n\tВсего оперативной памяти: {:.4} ГБ\n\t',
        'used': 'Используется: {:.4} ГБ\n\t',
        'free': 'Свободно: {:.4} ГБ\n'
    }
}

def get_memory():
    res = {
        'all': psutil.virtual_memory().total / 1024 / 1024 / 1024,
        'used': psutil.virtual_memory().used / 1024 / 1024 / 1024,
        'free': psutil.virtual_memory().free / 1024 / 1024 / 1024
    }
    return res

def show():
    memory = get_memory()
    template_memory = ""
    for key in memory.keys():
        template_memory += TEMPLATES['memory'][key].format(memory[key])
    
    print(template_memory)

if __name__ == "__main__":
    show()