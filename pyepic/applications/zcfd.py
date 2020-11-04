import json
from enum import Enum
from .base import JobStep, Job, Upload


class Reconstruct (Enum):
    ALL = 'all'
    LATEST = 'latest'
    TIME = 'time'

class ZCFDStep(JobStep):
    """
    docstring
    """

    def __init__(self, *args, **kwargs):
        super(ZCFDStep, self).__init__(*args, **kwargs)
        self.run_if_previous_step_fails = True
        self.step_name = 'solver'
        self.stopAt = StopAt.END_TIME
        self.startFrom = StartFrom.LATEST
        self.endTime = 0
        self.startTime = 0


class ZCFDJob(Job):
    """
    An ZCFD job object in EPIC
    """

    def __init__(self, foam_version_id, job_name, data_path):
        super(ZCFDJob, self).__init__(foam_version_id, job_name, data_path)
        self.zcfd = ZCFDStep(execute_step=True)


    def get_applications_options(self):
        return {
            "blockMesh": self.blockMesh.execute,
            "decomposePar": self.decomposePar.execute,
            "reconstructPar": self.reconstructPar.execute,
            "blockMesh_runtime": self.blockMesh.runtime,
            "decomposePar_runtime": self.decomposePar.runtime,
            "solver_runtime": self.solver.runtime,
            "reconstructPar_runtime": self.reconstructPar.runtime,
            "clear_partitions": self.clear_partitions,
            "partitions": self.solver.partitions,
            "stopAt": self.solver.stopAt.value,
            "endTime": self.solver.endTime,
            "startTime": self.solver.startTime,
            "startFrom": self.solver.startFrom.value,
            "reconstruct_option": self.reconstructPar.reconstruct_option.value,
            "reconstruct_time": self.reconstructPar.reconstruct_time,
            "upload_excludes": self.sync_processor_directories.value,
        }
    
    def get_job_create_spec(self, queue_id):
        spec = super().get_job_create_spec(queue_id)
        spec.jobs[0].app_options = self.get_applications_options()
        return spec

