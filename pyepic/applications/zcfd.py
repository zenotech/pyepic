import json
from enum import Enum
from .base import JobStep, Job, Upload


class ZCFDStep(JobStep):
    """zCFD Solver

    :var case_name: The name of the python control file for the case
    :vartype case_name: str
    :var problem_name: The name of the hdf5 mesh file
    :vartype problem_name: str
    :var restart: Is the case a restart from a previous solution
    :vartype restart: bool
    :var partitions: How many parallel partitions should the case use
    :vartype partitions: int
    """

    def __init__(
        self,
        case_name,
        problem_name,
        cycles,
        restart=False,
        partitions=1,
        execute_step=True,
    ):
        super().__init__()
        self.step_name = "ZCFD"
        self.case_name = case_name
        self.problem_name = problem_name
        self.restart = restart
        self.partitions = partitions
        self.cycles = cycles


class ZCFDJob(Job):
    """A helper class for submitting an zCFD job to EPIC.

    :param zcfd_version_id: The ID of the BatchApplicationVersion of zCFD to use
    :type zcfd_version_id: int
    :param job_name: The name to give the job in EPIC
    :type job_name: str
    :param data_path: The epic data path to the zCFD case directory
    :type data_path: str

    :var zcfd: zCFD JobStep object
    :vartype zcfd: :class:`ZCFDStep`
    """

    def __init__(
        self,
        zcfd_version_id,
        job_name,
        data_path,
        case_name,
        problem_name,
        cycles=100,
        restart=False,
        partitions=1,
    ):
        super().__init__(zcfd_version_id, job_name, data_path)
        self.zcfd = ZCFDStep(
            case_name,
            problem_name,
            cycles,
            restart=restart,
            partitions=partitions,
            execute_step=True,
        )
        self.add_step(self.zcfd)

    def get_applications_options(self):
        """Get application configuration options for submission to EPIC

        :return: Dictionary of the job configuration
        :rtype: dict
        """
        return {
            "case_name": self.zcfd.case_name,
            "problem_name": self.zcfd.problem_name,
            "cycles": self.zcfd.cycles,
            "restart": self.zcfd.restart,
        }

    def get_job_create_spec(self, queue_id):
        """Get a JobSpec for this job

        :return: Job Specification
        :rtype: class:`epiccore.models.JobSpec`
        """
        spec = super().get_job_create_spec(queue_id)
        spec.jobs[0].app_options = self.get_applications_options()
        return spec
