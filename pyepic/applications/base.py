from enum import Enum

from epiccore.models import (
    JobQuote,
    JobSpec,
    JobTaskSpec,
    JobArraySpec,
    JobConfiguration,
    JobDataBinding,
    JobClusterSpec,
    DataSpec,
)


class Distribution(Enum):
    """How should the partitions/processes or tasks be distrubuted on the remote cluster, 1 per CORE/SOCKET/NODE or DEVICE"""

    CORE = "core"
    SOCKET = "socket"
    NODE = "node"
    DEVICE = "device"

class Upload(Enum):
    """Should excluded files be uploaded? Yes, No or only when the job finishes in an error state."""

    YES = "yes"
    NO = "no"
    ON_ERROR = "error"


class JobStep(object):
    """A Step within an EPIC Job

    :param execute_step: Enable this step as part of this job
    :type execute_step: int

    :var step_name: Name of step, this is application specific
    :vartype step_name: str
    :var execute: Should this step execute when the job is submitted
    :vartype execute: bool
    :var partitions: How many partitions/processes make up this step
    :vartype partitions: int
    :var task_distribution: How are the partitions distributed to the hardware
    :vartype task_distribution: :class:`Distribution`
    :var runtime: The maximum runtime of this step in hours
    :vartype runtime: int
    :var run_if_previous_step_fails: Should this step execute if the previous step fails
    :vartype run_if_previous_step_fails: bool
    :var hyperthreading: Does this step count hyperthreaded cores as individual CPUs?
    :vartype hyperthreading: bool
    """

    def __init__(self, execute_step=True):
        self.step_name = None
        self.execute = execute_step
        self.partitions = 1
        self.task_distribution = Distribution.CORE
        self.tasks_per_device = 1
        self.runtime = 1
        self.run_if_previous_step_fails = True
        self.hyperthreading = True

    def get_task_spec(self):
        """Get a JobTaskSpec for this job step

        :return: Job Task Specification
        :rtype: :class:`epiccore.models.JobTaskSpec`
        """
        spec = JobTaskSpec(
            reference=self.step_name,
            partitions=self.partitions,
            runtime=self.runtime,
            task_distribution=self.task_distribution.value,
            hyperthreading=self.hyperthreading,
            tasks_per_device=self.tasks_per_device
        )
        return spec


class Config(object):
    """The Job Configuration

    :var overwrite_existing: Should data created on the remote cluster overwrite older data that exists in the epic data store
    :vartype overwrite_existing: bool
    :var upload: Which job states should trigger a data upload
    :vartype upload: list
    :var data_sync_interval: How frequently should the data be periodically uploaded while the job is still running, set to 0 to disable.
    :vartype data_sync_interval: int
    :var project_id: ID of the EPIC project to run this job in
    :vartype project_id: int, optional
    """

    def __init__(self):
        self.overwrite_existing = True
        self.upload = ["failure", "complete", "cancel"]
        self.data_sync_interval = 0
        self.project_id = None

    def get_configuration(self):
        """Get a JobConfiguration for this job
        :return: Job Configuration
        :rtype: class:`epiccore.models.JobConfiguration`
        """
        return JobConfiguration(
            upload=self.upload,
            overwrite_existing=self.overwrite_existing,
            data_sync_interval=self.data_sync_interval,
        )


class Job(object):
    """An EPIC Job Definition

    :param application_version: The Code of the BatchApplicationVersion that this job will user
    :type application_version: str
    :param job_name: A user friendly name for the job
    :type job_name: str
    :param path: The path to the root of the OpenFOAM job, formed as an epic url (e.g. "epic://path_to/data")
    :type path: str

    :var job_name: A user friendly name for the job
    :vartype job_name: str
    :var path: The path to the root of the OpenFOAM job, formed as an epic url (e.g. "epic://path_to/data")
    :vartype path: str
    :var config: The Job configuration options object
    :vartype config: :class:`Config`
    :var steps: The job steps that make up this job
    :vartype steps: list
    """

    def __init__(self, application_version, job_name, path):
        self.application_version = application_version
        self.job_name = job_name
        self.path = path
        self.config = Config()
        self.steps = []

    def add_step(self, job_step):
        """Add a new step to this job

        :param job_step: The step to append to this job
        :type job_step: :class:`JobStep`
        """
        self.steps.append(job_step)

    def get_job_spec(self):
        """Get a JobSpec for this job

        :return: Job Specification
        :rtype: class:`epiccore.models.JobSpec`
        """
        tasks = []
        for step in self.steps:
            if step.execute:
                tasks.append(step.get_task_spec())
        jobspec = JobSpec(
            app_code=self.application_version,
            project=self.config.project_id,
            tasks=tasks,
        )
        return jobspec

    def get_job_create_spec(self, queue_code):
        """Get a JobArraySpec for this job. The JobArraySpec can be used to submit the job to EPIC via the client.

        :param queue_code: The code of the EPIC batch queue to submit to
        :type queue_code: str

        :return: Job ArraySpecification
        :rtype: class:`epiccore.models.JobArraySpec`
        """
        spec = JobArraySpec(
            name=self.job_name,
            config=self.config.get_configuration(),
            jobs=[
                JobDataBinding(
                    name=self.job_name,
                    spec=self.get_job_spec(),
                    app_options={},
                    cluster=JobClusterSpec(
                        queue_code=queue_code,
                    ),
                    input_data=DataSpec(
                        path=self.path,
                    ),
                ),
            ],
        )
        return spec


class JobArray(object):
    """A helper class for submitting an array of  jobs to EPIC.

    :param array_name: The name to give the array in EPIC
    :type array_name: str
    :param array_root_folder: The epic data path to the root of the array data folder, formed as an epic url (e.g. "epic://path_to/data"). Any data in a folder called "common" within this folder will be shared between all jobs in the array.
    :type array_root_folder: str

    :var config: The Job configuration options object, common to all jobs in the array
    :vartype config: :class:`Config`
    :var jobs: The jobs that make up this array
    :vartype jobs: list
    """

    def __init__(
        self,
        array_name,
        array_root_folder,
    ):
        self.array_name = array_name
        self.array_root_folder = array_root_folder
        self.jobs = []
        self.config = Config()

    def add_job(self, job):
        """Add a job to this array

        :param job: The code of the EPIC batch queue to submit to
        :type job: class:`Job`
        """
        if isinstance(job, Job):
            self.jobs.append(job)
        else:
            raise Exception("Can only append Job instances to a JobArray")

    def get_job_create_spec(self, queue_code):
        """Get a JobArraySpec for this array. The JobArraySpec can be used to submit the array to EPIC via the client.

        :param queue_code: The code of the EPIC batch queue to submit to
        :type queue_code: str

        :return: Job ArraySpecification
        :rtype: class:`epiccore.models.JobArraySpec`
        """
        job_bindings = []
        for job in self.jobs:
            job_bindings.append(
                JobDataBinding(
                    name=job.job_name,
                    spec=job.get_job_spec(),
                    app_options=job.get_applications_options(),
                    cluster=JobClusterSpec(
                        queue_code=queue_code,
                    ),
                    input_data=DataSpec(
                        path=job.path,
                    ),
                )
            )

        if self.array_root_folder:
            spec = JobArraySpec(
                name=self.array_name,
                config=self.config.get_configuration(),
                jobs=job_bindings,
                common_data=DataSpec(
                    path=self.array_root_folder,
                ),
            )
        else:
            spec = JobArraySpec(
                name=self.array_name,
                config=self.config.get_configuration(),
                jobs=job_bindings,
                common_data=None,
            )
        return spec
