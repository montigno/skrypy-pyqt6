class Logging():
    def __init__(self, **options):
        from nipype import config, logging
        config_logging = {}
        config_logging['logging'] = options
        config.update_config(config_logging)
        logging.update_logging(config)

##############################################################################


class Execution():
    def __init__(self, **options):
        from nipype import config
        config_execution = {}
        config_execution['execution'] = options
        config.update_config(config_execution)
