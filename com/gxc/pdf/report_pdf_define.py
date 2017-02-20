#-*- encoding:utf-8 -*-

class ReportModuleType:
    TASK_STATS = 2
    BACKUP_RECOVERY = 4
    DISASTER = 5
    REMOTE_COPY= 6
    

class ReportTaskStatsTable:
    header_lables={
       ReportModuleType.TASK_STATS:{
          
        }
    }
    @classmethod
    def get_header_lables(cls,locale,module_id,task_type):
        return
    @classmethod
    def get_colum_widths(cls,module_id,task_type):
        return
    @classmethod
    def get_colum_width_split_nums(cls,module_id,task_type):
        pass
