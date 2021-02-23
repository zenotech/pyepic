import json
from enum import Enum
from .base import JobStep, Job, Upload


class NastranStep(JobStep):
    """Nastran Solver

    :var dat_file: The name of the nastran data file
    :vartype dat_file: str
    :var nastran_licence_server: The licence server and port for nastran
    :vartype nastran_licence_server: str
    :var partitions: How many parallel partitions should the case use
    :vartype partitions: int
    """

    def __init__(
        self,
        dat_file,
        nastran_licence_server,
        cycles,
        restart=False,
        partitions=1,
        execute_step=True,
    ):
        super().__init__()
        self.step_name = "Nastran"
        self.dat_file = dat_file
        self.nastran_licence_server = nastran_licence_server
        self.restart = restart
        self.partitions = partitions
        self.cycles = cycles


class NastranJob(Job):
    """A helper class for submitting an Nastran job to EPIC.

    :param nastran_version: The code of the BatchApplicationVersion of Nastran to use
    :type nastran_version: str
    :param job_name: The name to give the job in EPIC
    :type job_name: str
    :param data_path: The epic data path to the Nastran case directory
    :type data_path: str
    :param dat_file: The name of the nastran data file
    :type dat_file: str
    :param nastran_licence_server: The licence server and port for nastran
    :type nastran_licence_server: str

    :var nastran: Nastran solver JobStep object
    :vartype nastran: :class:`NastranStep`
    """

    def __init__(
        self,
        nastran_version,
        job_name,
        data_path,
        dat_file,
        nastran_licence_server,
        partitions=1,
    ):
        super().__init__(nastran_version, job_name, data_path)
        self.nastran = NastranStep(
            dat_file, nastran_licence_server, partitions=partitions, execute_step=True
        )
        self.add_step(self.nastran)

    def get_applications_options(self):
        """Get application configuration options for submission to EPIC

        :return: Dictionary of the job configuration
        :rtype: dict
        """
        return {
            "dat_file": self.nastran.dat_file,
            "nastran_licence_server": self.nastran.nastran_licence_server,
            "stop": False,
        }

    def get_job_create_spec(self, queue_code):
        """Get a JobSpec for this job

        :return: Job Specification
        :rtype: class:`epiccore.models.JobSpec`
        """
        spec = super().get_job_create_spec(queue_code)
        spec.jobs[0].app_options = self.get_applications_options()
        return spec
