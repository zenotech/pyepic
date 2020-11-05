
Examples
********

General Usage
=============

Setting up the client
---------------------
To initialise the client simply import EPICClient and then create a client instance, passing in your API Token from EPIC as a parameter.

.. code-block:: python

    from pyepic.client import EPICClient
    
    client = EPICClient("your_api_token_goes_here")


Listing Applications
--------------------
To list the available applications you can use the list_applications() method. The applications returned can be viewed by iterating over the response results.

.. code-block:: python

    from pyepic.client import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    # List all applications
    apps = client.list_applications()
    print("ID | Application | Version | Cluster IDs")
    for app in apps.results:
        for version in app.versions:
            print("{} | {} | {} | {}".format(version.id, app.product.name, version.version, version.queue_ids))

    # List applications but filter for "foam" in the application name
    foam_apps = client.list_applications(product_name="foam")


An example of the output of list_applications is shown below. The ID listed in the versions dictionary is the application_version_id used when creating a job for that application.

.. code-block:: json

    {'count': 2,
    'next': None,
    'previous': None,
    'results': [{'id': 2,
                'product': {'description': 'The goal of the Extend-Project is to '
                                            'open the FOAM CFD toolbox to '
                                            'community contributed extensions in '
                                            'the spirit of the OpenSource '
                                            'development model.',
                            'image': 'https://s3-eu-west-1.amazonaws.com/epic-media-zenotech/media/products/openfoam-extend.png',
                            'name': 'FOAM Extend',
                            'small_print': ' This offering is not approved or '
                                            'endorsed by ESI Group or '
                                            'ESI-OpenCFD®, the producer of the '
                                            'OpenFOAM® software and owner of the '
                                            'OpenFOAM® trademark.'},
                'versions': [{'id': 6, 'queue_ids': [5], 'version': '3.1'},
                            {'id': 4, 'queue_ids': [5], 'version': '1.6'}]},
                {'id': 3,
                'product': {'description': 'OpenFOAM is free, open source '
                                            'software for computational fluid '
                                            'dynamics (CFD), developed primarily '
                                            'by OpenCFD.',
                            'image': 'https://s3-eu-west-1.amazonaws.com/epic-media-zenotech/media/products/openfoam.png',
                            'name': 'OpenFOAM',
                            'small_print': 'This offering is not approved or '
                                            'endorsed by ESI Group or '
                                            'ESI-OpenCFD®, the producer of the '
                                            'OpenFOAM® software and owner of the '
                                            'OpenFOAM® trademark.'},
                'versions': [{'id': 12, 'queue_ids': [5], 'version': 'v1606+'},
                            {'id': 11, 'queue_ids': [5], 'version': '4.1'},
                            {'id': 10, 'queue_ids': [5], 'version': '3.0.1'},
                            {'id': 9, 'queue_ids': [5], 'version': '2.4.0'},
                            {'id': 8, 'queue_ids': [5], 'version': '2.3.1'}]}]}

Listing Queues
--------------

To list queues use the list_clusters() method. You can filter by cluster name or by available application version id.

.. code-block:: python

    from pyepic.client import EPICClient

    client = EPICClient("your_api_token_goes_here")

    # List all clusters
    clusters = client.list_clusters()
    for cluster in clusters.results:
        print("{} | {} | {}".format(cluster.id, cluster.display_name, cluster.display_description))

    # List clusters with a filter for a cluster name
    clusters = client.list_clusters(cluster_name="csd3")

    # List clusters with a filter for a particular application versions, for example list applications above gives "OpenFOAM v1606" ID=12
    clusters = client.list_clusters(application_id=12)


An example response is shown below. The id listed is the batch queue id needed when submitting an EPIC job to that queue.

.. code-block:: json

    {'count': 3,
    'next': None,
    'previous': None,
    'results': [{'display_description': 'The CFMS cluster is built using the Cray '
                                        'CS-400 solution, with parallel file '
                                        'storage provided by ArcaStream, based '
                                        'upon IBM Spectrum Scale (formerly known '
                                        'as IBM GPFS). The cluster includes '
                                        'latest generation Intel E5-26XX v4 '
                                        '(Broadwell) Xeon CPUs. The GPU nodes '
                                        'each have two Nvidia K80 GPUs.',
                'display_name': 'CFMS - GPU',
                'id': 1,
                'maintenance_mode': False,
                'max_allocation': 8,
                'max_runtime': 72,
                'reported_avail_tasks': None,
                'reported_max_tasks': None,
                'resource_config': "{'cpus': 2, 'cores_per_cpu': 8, "
                                    "'threads_per_core': 1, 'accelerator': "
                                    "{'name': 'K80 x 2', 'acc_class': 'CUDA', "
                                    "'quantity': 2, 'description': '2 x Nvidia "
                                    "K80'}, 'accelerator_count': 2, 'memory': "
                                    "'64.0'}",
                'sla': {'description': 'The jobs will be scheduled using the '
                                        'clusters standard batch scheduling '
                                        'policy.',
                        'name': 'Standard'}},
                {'display_description': 'The CFMS cluster is built using the Cray '
                                        'CS-400 solution, with parallel file '
                                        'storage provided by ArcaStream, based '
                                        'upon IBM Spectrum Scale (formerly known '
                                        'as IBM GPFS). The cluster includes '
                                        'latest generation Intel E5-26XX v4 '
                                        '(Broadwell) Xeon CPUs. The High Memory '
                                        'nodes each have 256GB of RAM.',
                'display_name': 'CFMS - High Memory',
                'id': 2,
                'maintenance_mode': False,
                'max_allocation': 20,
                'max_runtime': 72,
                'reported_avail_tasks': None,
                'reported_max_tasks': None,
                'resource_config': "{'cpus': 2, 'cores_per_cpu': 8, "
                                    "'threads_per_core': 1, 'accelerator': None, "
                                    "'accelerator_count': 0, 'memory': '256.0'}",
                'sla': {'description': 'The jobs will be scheduled using the '
                                        'clusters standard batch scheduling '
                                        'policy.',
                        'name': 'Standard'}},
                {'display_description': 'The CFMS cluster is built using the Cray '
                                        'CS-400 solution, with parallel file '
                                        'storage provided by ArcaStream, based '
                                        'upon IBM Spectrum Scale (formerly known '
                                        'as IBM GPFS). The cluster includes '
                                        'latest generation Intel E5-26XX v4 '
                                        '(Broadwell) Xeon CPUs. The Low SLA gives '
                                        'access to more resources but your job '
                                        'may be pre-empted.',
                'display_name': 'CFMS - Low',
                'id': 3,
                'maintenance_mode': False,
                'max_allocation': 120,
                'max_runtime': 72,
                'reported_avail_tasks': None,
                'reported_max_tasks': None,
                'resource_config': "{'cpus': 2, 'cores_per_cpu': 12, "
                                    "'threads_per_core': 1, 'accelerator': None, "
                                    "'accelerator_count': 0, 'memory': '128.0'}",
                'sla': {'description': 'The Low SLA provides access to a low '
                                        'priority queue. This queue provides '
                                        'access to more resources than the '
                                        'standard queue BUT please be aware that '
                                        'your jobs are at risk of being stopped '
                                        'if a higher priority job requires the '
                                        'resources.',
                        'name': 'Low'}}]}

Listing Jobs
--------------

To list jobs use the list_jobs() method. You can filter by cluster name or by available application version id.

.. code-block:: python

    from pyepic.client import EPICClient

    client = EPICClient("your_api_token_goes_here")

    jobs = client.list_jobs()

    print("ID | Name | Application | Status")
    for job in jobs.results:
        print("{} | {} | {} | {}".format(job.id, job.name, job.app, job.status))


An example output is shown below.

.. code-block:: json

    {'count': 3,
    'next': None,
    'previous': None,
    'results': [{'app': 'OpenFOAM (v1606+)',
                'application_version': 12,
                'config': {'data_sync_interval': 0,
                            'overwrite_existing': True,
                            'upload': ['failure', 'cancel', 'complete']},
                'cost': '£5.18',
                'finished': True,
                'id': 16,
                'invoice_reference': None,
                'name': 'motorBike',
                'project': None,
                'resource': {'display_description': 'Amazon Web Services offers '
                                                    'flexible infrastructure '
                                                    'services on demand. '
                                                    'Zenotech use these services '
                                                    'to offer HPC on demand via '
                                                    'EPIC. This cluster is built '
                                                    'from C4.8xlarge Compute '
                                                    'Optimised instances '
                                                    'connected by the AWS '
                                                    'Enhanced networking. The '
                                                    'queue uses the AWS Spot '
                                                    'Market, this gives access '
                                                    'to unused resources at a '
                                                    'reduced cost but please be '
                                                    'aware there is a risk that '
                                                    'the nodes may be reclaimed '
                                                    'if demand rises.',
                            'display_name': 'AWS C5 Spot',
                            'id': 5,
                            'maintenance_mode': False,
                            'max_allocation': 20,
                            'max_runtime': 36,
                            'reported_avail_tasks': None,
                            'reported_max_tasks': None,
                            'resource_config': "{'cpus': 2, 'cores_per_cpu': "
                                                "18, 'threads_per_core': 2, "
                                                "'accelerator': None, "
                                                "'accelerator_count': 0, "
                                                "'memory': '60.0'}",
                            'sla': {'description': 'The nodes used may be '
                                                    'reclaimed if demand for '
                                                    'resources increases, if '
                                                    'this happens your job may '
                                                    'be stopped and requeued.',
                                    'name': 'Spot'}},
                'status': 'Job Cancelled',
                'submitted_at': '2020-10-01T09:37:40.674500Z',
                'submitted_by': 'Mike Turner'},
                {'app': 'OpenFOAM (v1606+)',
                'application_version': 12,
                'config': {'data_sync_interval': 0,
                            'overwrite_existing': True,
                            'upload': ['failure', 'cancel', 'complete']},
                'cost': '£5.18',
                'finished': True,
                'id': 17,
                'invoice_reference': None,
                'name': 'motorBike',
                'project': None,
                'resource': {'display_description': 'Amazon Web Services offers '
                                                    'flexible infrastructure '
                                                    'services on demand. '
                                                    'Zenotech use these services '
                                                    'to offer HPC on demand via '
                                                    'EPIC. This cluster is built '
                                                    'from C4.8xlarge Compute '
                                                    'Optimised instances '
                                                    'connected by the AWS '
                                                    'Enhanced networking. The '
                                                    'queue uses the AWS Spot '
                                                    'Market, this gives access '
                                                    'to unused resources at a '
                                                    'reduced cost but please be '
                                                    'aware there is a risk that '
                                                    'the nodes may be reclaimed '
                                                    'if demand rises.',
                            'display_name': 'AWS C5 Spot',
                            'id': 5,
                            'maintenance_mode': False,
                            'max_allocation': 20,
                            'max_runtime': 36,
                            'reported_avail_tasks': None,
                            'reported_max_tasks': None,
                            'resource_config': "{'cpus': 2, 'cores_per_cpu': "
                                                "18, 'threads_per_core': 2, "
                                                "'accelerator': None, "
                                                "'accelerator_count': 0, "
                                                "'memory': '60.0'}",
                            'sla': {'description': 'The nodes used may be '
                                                    'reclaimed if demand for '
                                                    'resources increases, if '
                                                    'this happens your job may '
                                                    'be stopped and requeued.',
                                    'name': 'Spot'}},
                'status': 'Job Complete',
                'submitted_at': '2020-10-01T13:33:54.569241Z',
                'submitted_by': 'Mike Turner'},
                {'app': 'OpenFOAM (v1606+)',
                'application_version': 12,
                'config': {'data_sync_interval': 0,
                            'overwrite_existing': True,
                            'upload': ['failure', 'cancel', 'complete']},
                'cost': '£5.18',
                'finished': True,
                'id': 18,
                'invoice_reference': None,
                'name': 'motorBike',
                'project': None,
                'resource': {'display_description': 'Amazon Web Services offers '
                                                    'flexible infrastructure '
                                                    'services on demand. '
                                                    'Zenotech use these services '
                                                    'to offer HPC on demand via '
                                                    'EPIC. This cluster is built '
                                                    'from C4.8xlarge Compute '
                                                    'Optimised instances '
                                                    'connected by the AWS '
                                                    'Enhanced networking. The '
                                                    'queue uses the AWS Spot '
                                                    'Market, this gives access '
                                                    'to unused resources at a '
                                                    'reduced cost but please be '
                                                    'aware there is a risk that '
                                                    'the nodes may be reclaimed '
                                                    'if demand rises.',
                            'display_name': 'AWS C5 Spot',
                            'id': 5,
                            'maintenance_mode': False,
                            'max_allocation': 20,
                            'max_runtime': 36,
                            'reported_avail_tasks': None,
                            'reported_max_tasks': None,
                            'resource_config': "{'cpus': 2, 'cores_per_cpu': "
                                                "18, 'threads_per_core': 2, "
                                                "'accelerator': None, "
                                                "'accelerator_count': 0, "
                                                "'memory': '60.0'}",
                            'sla': {'description': 'The nodes used may be '
                                                    'reclaimed if demand for '
                                                    'resources increases, if '
                                                    'this happens your job may '
                                                    'be stopped and requeued.',
                                    'name': 'Spot'}},
                'status': 'Job Complete',
                'submitted_at': '2020-10-01T13:40:45.102124Z',
                'submitted_by': 'Mike Turner'}]}


To get the details of a specific job with a known ID using the get_job_details method.

.. code-block:: python

    from pyepic.client import EPICClient

    client = EPICClient("your_api_token_goes_here")

    # Get details for job id 18
    jobs = client.get_job_details(18)



OpenFOAM
========
To create and submit an OpenFOAM job you can use the :class:`pyepic.applications.openfoam.OpenFoamJob` class. 
Prior to creating the job you need to know the ID over the application version you wish to use, the id of the batch queue you want to 
submit to and the path to the root of the openfoam case. The data for this case is assumed to have already been uploaded to your EPIC data store.

.. code-block:: python

    from pyepic.client import EPICClient
    from pyepic.applications.openfoam import OpenFoamJob

    client = EPICClient("your_api_token_goes_here")

    # Create the job using application version ID 12
    openfoam_job = OpenFoamJob(12, "job_name", "epic://my_data/foam/")

    # Configure the solver to run on 24 paritions for a maximum of 12 hours
    openfoam_job.solver.partitions = 24
    openfoam_job.solver.runtime = 12

    # Create the specification for submission to queue ID 3
    job_spec = openfoam_job.get_job_create_spec(3)

    # Submit the job
    job = client.submit_job(job_spec)


The submit_job method will return a job object. The job_id can be extraced from this object for future queries.

zCFD
====
To create and submit an zCFD job you can use the :class:`pyepic.applications.zcfd.ZCFDJob` class. 
Prior to creating the job you need to know the ID over the application version you wish to use, the id of the batch queue you want to 
submit to and the path to the root of the zcfd case. The data for this case is assumed to have already been uploaded to your EPIC data store.


.. code-block:: python

    import pyepic

    from pyepic.client import EPICClient
    from pyepic.applications.zcfd import ZCFDJob

    client = EPICClient("your_api_token_goes_here")

    # Create a zCFD job using application version id 3
    zcfd_job = ZCFDJob(3, "zcfd_case", "epic://zcfd/", "fv.py", "box.hdf5", cycles=1000, restart=False, partitions=24)

    # Configure the solver to run for a maximum of 12 hours
    zcfd_job.zcfd.runtime = 12

    # Create the specification for submission to queue ID 3
    job_spec = zcfd_job.get_job_create_spec(3)

    # Submit the job
    job = client.submit_job(job_spec)
