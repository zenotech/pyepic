import json
from enum import Enum
from .base import JobStep, Job, Upload, Distribution



class ExameshStep(JobStep):
    """ExaMesh

    :var toml_file: The name of the toml control file for the case
    :vartype case_name: str
    """

    def __init__(
        self,
        toml_file,
        partitions=1,
        execute_step=True,
        clean_case=True
    ):
        super().__init__()
        self.step_name = "ExaMesh"
        self.toml_file = toml_file
        self.partitions = partitions
        self.clean_case = clean_case

class ZCFDStep(JobStep):
    """zCFD Solver

    :var case_name: The name of the python control file for the case
    :vartype case_name: str
    :var problem_name: The name of the hdf5 mesh file
    :vartype problem_name: str
    :var override_file: The name of the zcfd override file for overset meshes
    :vartype override_file: str
    :var cycles: How many cycles to run for
    :vartype cycles: int
    :var restart: Is the case a restart from a previous solution
    :vartype restart: bool
    :var partitions: How many parallel partitions should the case use
    :vartype partitions: int
    """

    def __init__(
        self,
        case_name,
        problem_name,
        override_file,
        cycles,
        restart=False,
        partitions=1,
        execute_step=True,
    ):
        super().__init__()
        self.step_name = "ZCFD"
        self.case_name = case_name
        self.problem_name = problem_name
        self.override_file = override_file
        self.restart = restart
        self.partitions = partitions
        self.cycles = cycles


class ZOPTJob(Job):
    """A helper class for submitting an zOpt job to EPIC.

    :param zopt_version: The code of the BatchApplicationVersion of zOpt to use
    :type zopt_version: str
    :param job_name: The name to give the job in EPIC
    :type job_name: str
    :param data_path: The epic data path to the zOpt case directory
    :type data_path: str
    :param case_name: The name of the python control file for the case
    :type case_name: str
    :param problem_name: The name of the hdf5 mesh file
    :type problem_name: str
    :param toml_file: The name of the examesh toml file
    :type toml_file: str
    :param override_file: The name of the zcfd override file for overset meshes. Defaults to None.
    :type override_file: str, optional
    :param cycles: How many cycles to run for. Default 100.
    :type cycles: int, optional
    :param restart: Is the case a restart from a previous solution. Default False.
    :type restart: bool, optional
    :param partitions: How many parallel partitions should the case use. Default 1.
    :type partitions: int, optional

    :var zcfd: zCFD JobStep object
    :vartype zcfd: :class:`ZCFDStep`
    """

    def __init__(
        self,
        zcfd_version,
        job_name,
        data_path,
        case_name,
        problem_name,
        toml_file,
        override_file=None,
        cycles=100,
        restart=False,
        partitions=1,
    ):
        super().__init__(zcfd_version, job_name, data_path)
        self.examesh = ExameshStep(toml_file, partitions=1)
        self.add_step(self.examesh)
        self.zcfd = ZCFDStep(
            case_name,
            problem_name,
            override_file,
            cycles,
            restart=restart,
            partitions=partitions,
            execute_step=True,
        )
        self.zcfd.task_distribution = Distribution.DEVICE
        self.add_step(self.zcfd)

    def get_applications_options(self):
        """Get application configuration options for submission to EPIC

        :return: Dictionary of the job configuration
        :rtype: dict
        """
        return {
            "toml_file": self.examesh.toml_file,
            "run_examesh": self.examesh.execute,
            "case_name": self.zcfd.case_name,
            "problem_name": self.zcfd.problem_name,
            "cycles": self.zcfd.cycles,
            "restart": self.zcfd.restart,
            "override_file": self.zcfd.override_file,
            "partitions": self.zcfd.partitions,
            "solver_tasks_per_node": self.zcfd.task_distribution.value,
            "solver_runtime": self.zcfd.runtime,
            "clean_case": self.examesh.clean_case
        }

    def get_job_create_spec(self, queue_code):
        """Get a JobSpec for this job

        :return: Job Specification
        :rtype: class:`epiccore.models.JobSpec`
        """
        spec = super().get_job_create_spec(queue_code)
        spec.jobs[0].app_options = self.get_applications_options()
        return spec
