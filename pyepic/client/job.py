import epiccore

from .base import Client

class JobClient(Client):
    """A wrapper class around the epiccore Job API.

            :param connection_token: Your EPIC API authentication token
            :type connection_token: str
            :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
            :type connection_url: str, optional

        """

    def get_quote(self, job_spec):
        """Get a Quote for running a series of tasks on EPIC.

            :param job_spec: The EPIC job specification
            :type job_spec: class:`epiccore.models.JobSpec`
            :return: A quote giving the price for the job on the available HPC queues
            :rtype: class:`epiccore.models.JobQuote`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_quote(job_spec)

    def submit(self, job_array_spec):
        """Submit new job in EPIC as described by job_array_spec.

            :param job_array_spec: The EPIC job specification
            :type job_array_spec: class:`epiccore.models.JobArraySpec`
            :return: The newly created job instance
            :rtype: class:`epiccore.models.Job`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_create(job_array_spec)

    def list(self, limit=10, offset=0):
        """List all of the jobs in EPIC. 

            :return: Response with results of returned :class:`epiccore.models.Job` objects
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_list(limit=limit, offset=offset)

    def list_steps(self, parent_job=None, limit=10, offset=0):
        """List all of the job steps in EPIC. 

            :param parent_job: The ID of the parent job to list the steps for
            :type parent_job: int, optional
            :param limit: Number of results to return per request, defaults to 10
            :type limit: int
            :param offset: The initial index from which to return the results, defaults to 0
            :type offset: int
            :return: Response with results of returned :class:`epiccore.models.JobStep` objects
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobstepApi(api_client)
            return instance.jobstep_list(parent_job=parent_job, limit=limit, offset=offset)

    def get_details(self, job_id):
        """Get details of job with ID job_id

            :param job_id: The ID of the job to fetch details on
            :type job_id: int
            :return: A Job instance
            :rtype: class:`epiccore.models.Job`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_read(job_id)

    def get_step_details(self, step_id):
        """Get the details of the step ID step_id

            :param step_id: The ID of the job step to fetch
            :type step_id: int
            :return: A Job Step instance
            :rtype: class:`epiccore.models.JobStep`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobstepApi(api_client)
            return instance.jobstep_read(step_id)

    def get_step_logs(self, step_id):
        """Get the step logs for step with id step_id

            :param step_id: The ID of the step to fetch the logs for
            :type step_id: int
            :return: A Job Log instance
            :rtype: class:`epiccore.models.JobLog`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobstepApi(api_client)
            return instance.jobstep_logs_read(step_id)

    def refresh_step_logs(self, step_id):
        """Request a refresh for the step logs for step with id step_id

            :param step_id: The ID of the job to fetch the steps for
            :type step_id: int
            :return: A Job Log instance
            :rtype: class:`epiccore.models.JobLog`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobstepApi(api_client)
            data = epiccore.JobLog()
            return instance.jobstep_logs_update(step_id, data)

    def cancel(self, job_id):
        """Cancel job with ID job_id

            :param job_id: The ID of the job to cancel
            :type job_id: int
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_cancel(job_id, {})
