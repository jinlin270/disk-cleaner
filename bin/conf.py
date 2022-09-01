import yaml
import logging
import logging.config
import os


class Config(object):
    """
    configure log file and attributes for Disk
    """
    def __init__(self, path: str = None):
        disk_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_yamlpath = disk_path + '/config/log_config.yaml'
        with open(log_yamlpath) as file:
            log_config = yaml.safe_load(file.read())
        logging.config.dictConfig(log_config)
        self.main_logger = logging.getLogger('__main__')
        self.thread_logger = logging.getLogger('thread')

        disk_cleanup_config_yamlpath = disk_path + '/config/disk_cleaner_config.yaml'
        with open(disk_cleanup_config_yamlpath) as file:
            config = yaml.safe_load(file.read())
            self.normal_period = config['normal_period_day']
            self.locked_period = config['locked_period_day']
            self.match_express = config['match_express']
            self.disk_usage_trigger = config['disk_usage_trigger_percent']
            self.inode_usage_trigger = config['inode_usage_trigger_percent']
            self.webhook = config['webhook']
            self.inode_overflow = config['inode_usage_overflow_percent']
            self.disk_overflow = config['disk_usage_overflow_percent']
            if not self.match_express:
                self.match_express = ['']
            self.queue_size = config['queue_size']
            assert(self.queue_size > 0)
            if path is None:
                if config['disk_path'] is not None and os.path.exists(config['disk_path']):
                    self.path = config['disk_path']
            else:
                self.path = path



