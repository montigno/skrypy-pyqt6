class list_SharedMemory():
    def __init__(self):
        import os
        import yaml

        file_shme = os.path.expanduser("~")
        file_shme = os.path.join(file_shme, '.skrypy', 'list_shm.yml')
        self.l_shm = []
        if os.path.exists(file_shme):
            with open(file_shme, 'r') as file_yml:
                data = yaml.load(file_yml, Loader=yaml.SafeLoader)
                self.l_shm = list(data.keys())

    def list_shm(self: 'list_str'):
        return self.l_shm

##############################################################################


class SharedMemory_create():
    def __init__(self, memoryName='', data='', **options):
        import os
        import yaml

        memoryName = memoryName.strip()
        shared_data = {}
        file_shme = os.path.expanduser("~")
        file_shme = os.path.join(file_shme, '.skrypy', 'list_shm.yml')
        if os.path.exists(file_shme):
            with open(file_shme, 'r') as file_yml:
                shared_data = yaml.load(file_yml, Loader=yaml.SafeLoader)
                if 'overwrite' in options:
                    if not options['overwrite']:
                        if memoryName not in shared_data:
                            shared_data[memoryName] = data
                    else:
                        shared_data[memoryName] = data
                else:
                    shared_data[memoryName] = data
        else:
            shared_data[memoryName] = data
        with open(file_shme, 'w') as file_yml:
            yaml.dump(shared_data, file_yml)
            while not os.path.exists(file_shme):
                time.sleep(1)

##############################################################################


class SharedMemory_read():
    def __init__(self, memoryName='', **options):
        import os
        import yaml

        memoryName = memoryName.strip()
        self.data = None
        file_shme = os.path.expanduser("~")
        file_shme = os.path.join(file_shme, '.skrypy', 'list_shm.yml')
        if not os.path.exists(file_shme):
            print('list_shm.yml doesn\'t exist')
            return
        with open(file_shme, 'r') as file_yml:
            data = yaml.load(file_yml, Loader=yaml.SafeLoader)

        if memoryName in data:
            self.data = data[memoryName]

            if 'cleanup' in options:
                if options['cleanup']:
                    del data[memoryName]
                    if bool(data):
                        with open(file_shme, 'w') as file_yml:
                            yaml.dump(data, file_yml)
                    else:
                        os.remove(file_shme)

    def out_data(self: 'str'):
        return self.data
