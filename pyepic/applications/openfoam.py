import json
from enum import Enum
from .base import JobStep, Job, Upload


class Reconstruct(Enum):
    ALL = "all"
    LATEST = "latest"
    TIME = "time"


class StopAt(Enum):
    END_TIME = "endTime"
    WRITE_NOW = "writeNow"
    NO_WRITE_NOW = "noWriteNow"
    NEXT_WRITE = "nextWrite"


class StartFrom(Enum):
    FIRST = "firstTime"
    START = "startTime"
    LATEST = "latestTime"


class BlockMeshStep(JobStep):
    """BlockMeshStep step of OpenFOAM"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step_name = "blockMesh"


class DecomposeParStep(JobStep):
    """DecomposeParStep step of OpenFOAM"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step_name = "decomposePar"


class SolverStep(JobStep):
    """Solver step of OpenFOAM

    :var run_if_previous_step_fails: Run if previous step fails, defaults to False
    :vartype run_if_previous_step_fails: bool
    :var stopAt: When to stop the solver. Defaults to END_TIME
    :vartype stopAt: :class:`StopAt`
    :var startFrom: Which timestep to start the solver from. Defaults to LATEST
    :vartype startFrom: :class:`StartFrom`
    :var endTime: If stopAt == END_TIME then which timestep to stop the solver at.
    :vartype endTime: int
    :var startTime: If startFrom == START then which timestep to start the solver from.
    :vartype startTime: int
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run_if_previous_step_fails = False
        self.step_name = "solver"
        self.stopAt = StopAt.END_TIME
        self.startFrom = StartFrom.LATEST
        self.endTime = 0
        self.startTime = 0
        self.application = "simpleFoam"


class ReconstructParStep(JobStep):
    """ReconstructPar step of OpenFOAM

    :var run_if_previous_step_fails: Run if solver fails, defaults to True
    :vartype run_if_previous_step_fails: bool
    :var reconstruct_option: Which time step to reconstruct. Defaults to ALL
    :vartype reconstruct_option: :class:`Reconstruct`
    :var reconstruct_time: If reconstruct_option == TIME then which timestep to reconstruct.
    :vartype reconstruct_time: int
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run_if_previous_step_fails = True
        self.step_name = "reconstructPar"
        self.reconstruct_option = Reconstruct.ALL
        self.reconstruct_time = ""


class OpenFoamJob(Job):
    """A helper class for submitting an OpenFOAM job to EPIC.

    :param foam_version: The code of the BatchApplicationVersion of OpenFOAM to use
    :type foam_version: str
    :param job_name: The name to give the job in EPIC
    :type job_name: str
    :param data_path: The epic data path to the OpenFOAM case directory
    :type data_path: str

    :var blockMesh: blockMesh JobStep object
    :vartype blockMesh: :class:`BlockMeshStep`
    :var decomposePar: decomposePar JobStep object
    :vartype decomposePar: :class:`DecomposeParStep`
    :var solver: initial solver JobStep object
    :vartype solver: :class:`SolverStep`
    :var reconstructPar: reconstructPar JobStep object
    :vartype reconstructPar: :class:`ReconstructParStep`
    :var clear_partitions: Delete any existing processor directories before running job
    :type clear_partitions: bool
    :var sync_processor_directories: Upload processor after job completion, default No
    :vartype sync_processor_directories: :class:`.base.Upload`

    """

    def __init__(self, foam_version, job_name, data_path):

        super().__init__(foam_version, job_name, data_path)
        self.blockMesh = BlockMeshStep(execute_step=False)
        self.decomposePar = DecomposeParStep(execute_step=True)
        self.solver = SolverStep(execute_step=True)
        self.reconstructPar = ReconstructParStep(execute_step=True)
        self.add_step(self.blockMesh)
        self.add_step(self.decomposePar)
        self.add_step(self.solver)
        self.add_step(self.reconstructPar)
        self.clear_partitions = True
        self.sync_processor_directories = Upload.NO

    def get_applications_options(self):
        """Get application configuration options for submission to EPIC

        :return: Dictionary of the job configuration
        :rtype: dict
        """
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
            "solver": self.solver.application,
            "reconstruct_option": self.reconstructPar.reconstruct_option.value,
            "reconstruct_time": self.reconstructPar.reconstruct_time,
            "upload_excludes": self.sync_processor_directories.value,
            "solver_tasks_per_node": self.solver.task_distribution,
        }

    def get_job_create_spec(self, queue_code):
        """Get a JobSpec for this job

        :return: Job Specification
        :rtype: class:`epiccore.models.JobSpec`
        """
        spec = super().get_job_create_spec(queue_code)
        spec.jobs[0].app_options = self.get_applications_options()
        return spec
