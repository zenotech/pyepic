
Examples
********

General Usage
=============

Setting up the client
---------------------
To initialise the client simply import EPICClient and then create a client instance, passing in your API Token from EPIC as a parameter.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")

You can then access the appropriate client api using the corresponding api member variable. 


Catalog
=======
The catalog API allows you to list the current configurations available for Jobs, Applications and Desktops in EPIC.
This can be used to get the IDs necessary for launching a job or desktop with the correct configuration.

Listing Applications
--------------------
To list the available applications you can use the list_applications() method. The applications returned can be viewed by iterating over the response results.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")

    # List all applications
    apps = client.catalog.list_applications()
    print("App Code | Application | Version | Cluster Codes")
    for app in apps:
        for version in app.versions:
            print("{} | {} | {} | {}".format(version.app_code, app.product.name, version.version, version.available_on))

    # List applications but filter for "foam" in the application name
    foam_apps = client.catalog.list_applications(product_name="foam")
    


An example of the output of list_applications is shown below. The App code listed in the versions dictionary is the app_code used when creating a job for that application.

.. code-block:: json

    [
                {'product': {'description': 'The goal of the Extend-Project is to '
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
                            {'id': 8, 'queue_ids': [5], 'version': '2.3.1'}]}
    ]

Listing Queues
--------------

To list queues use the list_clusters() method. You can filter by cluster name or by available application version id.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")

    # List all clusters
    clusters = client.catalog.list_clusters()
    for cluster in clusters:
        print("{} | {}".format(cluster.name, cluster.description))

    # List clusters with a filter for a cluster name
    clusters = client.catalog.list_clusters(cluster_name="csd3")

    # List cluster with a filter for a queue name
    clusters = client.catalog.list_clusters(queue_name="gpu")

    # List clusters with a filter for a particular application versions, filter using the app_codes from the catalog endpoint
    clusters = client.catalog.list_clusters(allowed_apps="cfx:16.1")


An example json response is shown below. The id listed is the queue_code is used when submitting an EPIC job to that queue.

.. code-block:: json

    [
               {'display_description': 'The CFMS cluster is built using the Cray '
                                        'CS-400 solution, with parallel file '
                                        'storage provided by ArcaStream, based '
                                        'upon IBM Spectrum Scale (formerly known '
                                        'as IBM GPFS). The cluster includes '
                                        'latest generation Intel E5-26XX v4 '
                                        '(Broadwell) Xeon CPUs. The GPU nodes '
                                        'each have two Nvidia K80 GPUs.',
                'display_name': 'CFMS - GPU',
                'queue_code': 'cfms:gpu',
                'maintenance_mode': False,
                'max_allocation': 8,
                'max_runtime': 72,
                'reported_avail_tasks': None,
                'reported_max_tasks': None,
                'resource_config': "{'cpus': 2, 'cores_per_cpu': 8, "
                                    "'threads_per_core': 1, 'accelerator': "
                                    "{'name': 'K80 x 2', 'acc_class': 'CUDA', "
                                    "'quantity': 2, 'description': '2 x Nvidia "
                                    "K80'}, 'memory': "
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
                'queue_code': 'cfms:highmem',
                'maintenance_mode': False,
                'max_allocation': 20,
                'max_runtime': 72,
                'reported_avail_tasks': None,
                'reported_max_tasks': None,
                'resource_config': "{'cpus': 2, 'cores_per_cpu': 8, "
                                    "'threads_per_core': 1, 'accelerator': None, "
                                    "'memory': '256.0'}",
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
                'queue_code': 'cfms:low',
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
                        'name': 'Low'}}
    ]

Listing Desktop Types
---------------------

To list the types of desktop nodes available in epic use the catalog.list_desktops() method. 

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")

    # List desktop types
    desktops = client.catalog.list_desktops()

    # Look at the results
    print("Name | Code | Description | CPU Cores | GPUs")
    for desktop in desktops:
        print("{} | {} | {} | {} | {}".format(
                desktop.name,
                desktop.node_code,
                desktop.description,
                desktop.cores,
                desktop.gpus
            ))


An example json output from list_desktops is shown below

.. code-block:: json

    [
        {
        "node_code": "desktop:standard",
        "name": "Standard GPU Node",
        "description": "8 Cascade Lake CPU Cores, 32GiB Memory, 1 x NVidia T4 GPU",
        "cores": 8,
        "gpus": 1
        },
        {
        "node_code": "desktop:large",
        "name": "Large GPU Node",
        "description": "64 Cascade Lake CPU Cores, 256GiB Memory, 1 x NVidia T4 GPU",
        "cores": 64,
        "gpus": 1
        },
        {
        "node_code": "desktop:xlarge",
        "name": "Large (multi-GPU) Node",
        "description": "48 Cascade Lake CPU Cores, 192GiB Memory, 4 x NVidia T4 GPU",
        "cores": 64,
        "gpus": 4
        }
    ]

Jobs
====
The job client gives access to job related methods.


Listing Jobs
--------------

To list jobs use the list_jobs() method. You can filter by cluster name or by available application version id.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")

    jobs = client.job.list()

    print("ID | Name | Application | Status")
    for job in jobs:
        print("{} | {} | {} | {}".format(job.id, job.name, job.app, job.status))


An example output is shown below.

.. code-block:: json

    [
                {'app': 'OpenFOAM (v1606+)',
                'application_version': "openfoam:v1606+",
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
                            'queue_code': 'aws:c5',
                            'maintenance_mode': False,
                            'max_allocation': 20,
                            'max_runtime': 36,
                            'reported_avail_tasks': None,
                            'reported_max_tasks': None,
                            'resource_config': "{'cpus': 2, 'cores_per_cpu': "
                                                "18, 'threads_per_core': 2, "
                                                "'accelerator': None, "
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
                'application_version': "openfoam:v1606+",
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
                            'queue_code': 'aws:c5',
                            'maintenance_mode': False,
                            'max_allocation': 20,
                            'max_runtime': 36,
                            'reported_avail_tasks': None,
                            'reported_max_tasks': None,
                            'resource_config': "{'cpus': 2, 'cores_per_cpu': "
                                                "18, 'threads_per_core': 2, "
                                                "'accelerator': None, "
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
                'application_version': "openfoam:v1606+",
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
                            'queue_code': 'aws:c5',
                            'maintenance_mode': False,
                            'max_allocation': 20,
                            'max_runtime': 36,
                            'reported_avail_tasks': None,
                            'reported_max_tasks': None,
                            'resource_config': "{'cpus': 2, 'cores_per_cpu': "
                                                "18, 'threads_per_core': 2, "
                                                "'accelerator': None, "
                                                "'memory': '60.0'}",
                            'sla': {'description': 'The nodes used may be '
                                                    'reclaimed if demand for '
                                                    'resources increases, if '
                                                    'this happens your job may '
                                                    'be stopped and requeued.',
                                    'name': 'Spot'}},
                'status': 'Job Complete',
                'submitted_at': '2020-10-01T13:40:45.102124Z',
                'submitted_by': 'Mike Turner'}
    ]


To get the details of a specific job with a known ID using the get_job_details method.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")

    # Get details for job id 18
    jobs = client.job.get_details(18)


Checking job logs
-----------------

Job logs are available for each step that makes up the job. The step id's for each job are listed in the job details and with that ID you can fetch the current log tails.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")

    # Get the latest tail of the log files, EPIC will request an update of the logs for running jobs
    log_obj = client.job.get_step_logs(50)

    # Print stdout from the logs
    print(log_obj.stdout)

    # Get the latest tail of the log files without requesting a refresh
    log_obj = client.job.refresh_step_logs(50, refresh=False)


Fetching job residuals
----------------------

For applications that support residuals you can fetch the available variable names and then request the data for specific variables.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")

    # Get the list of available variables to plot for job id 101
    available_variables = client.job.get_job_residual_names(101)

    # Print variable names
    print(available_variables)

    # Get the data for variables "Ux" & "Uy". By default a value of xaxis is always returned.
    variables = client.job.get_job_residual_values(50, ['Ux','Uy'])

    for var in variables:
        print("Var name = {}".format(var.variable_name))
        print("Var values = {}".format(var.values))




Submitting Jobs
---------------
Submitting jobs is done with the client.job.submit() method. PyEpic has application specfic helper classes to make the submission as simple as possible, see the application examples below.


OpenFOAM
--------
To create and submit an OpenFOAM job you can use the :class:`pyepic.applications.openfoam.OpenFoamJob` class. 
Prior to creating the job you need to know the code of the application version you wish to use, the code of the batch queue you want to submit to and the path to the root of the openfoam case. The data for this case is assumed to have already been uploaded to your EPIC data store. 
The app and queue codes can be obtained from the catalog endpoints.

.. code-block:: python

    from pyepic import EPICClient
    from pyepic.applications.openfoam import OpenFoamJob

    client = EPICClient("your_api_token_goes_here")

    # Create the job using application version with id "openfoam:v1606"
    openfoam_job = OpenFoamJob("openfoam:v1606", "job_name", "epic://my_data/foam/")

    # Configure the solver to run on 24 paritions for a maximum of 12 hours
    openfoam_job.solver.partitions = 24
    openfoam_job.solver.runtime = 12

    # Create the specification for submission to queue with code "aws:c5"
    job_spec = openfoam_job.get_job_create_spec("aws:c5")

    # Submit the job
    job = client.job.submit(job_spec)


The submit_job method will return a job object. The job_id can be extraced from this object for future queries.

zCFD
----
To create and submit an zCFD job you can use the :class:`pyepic.applications.zcfd.ZCFDJob` class. 
Prior to creating the job you need to know the code of the application version you wish to use, the id of the batch queue you want to 
submit to and the path to the root of the zcfd case. The data for this case is assumed to have already been uploaded to your EPIC data store.
If your data is in your EPIC data store in a folder called 'work/zcfd' then the data path for the method would be 'epic://work/zcfd/'. 
The app and queue codes can be obtained from the catalog endpoints.

.. code-block:: python

    from pyepic import EPICClient
    from pyepic.applications.zcfd import ZCFDJob

    client = EPICClient("your_api_token_goes_here")

    # Create a zCFD job using application version id "zcfd:2021.1.1"
    zcfd_job = ZCFDJob("zcfd:2021.1.1", "zcfd_case", "epic://work/zcfd/", "fv.py", "box.hdf5", cycles=1000, restart=False, partitions=24)

    # Configure the solver to run for a maximum of 12 hours
    zcfd_job.zcfd.runtime = 12

    # Create the specification for submission to queue "aws:p4d"
    job_spec = zcfd_job.get_job_create_spec("aws:p4d")

    # Submit the job
    job = client.job.submit(job_spec)

    job_id = job[0].id

    print(f"Submitted job with id {id}")

Job Arrays
==========
Job arrays allow you to submit a set of jobs in one submission. Jobs in an array can share common data to reduce the volume of data that you need to transfer. 
To use arrays you should structure your input data to have a shared root folder. This root folder can then contain the "common" folder and multiple job folders.

The example below shows a job array for zCFD. The example folder structure for this case is:

epic://work/zcfd/
    The array root folder for the case.

epic://work/zcfd/common/
    The folder containing files common to all jobs in the array, for example the *box.hdf5* mesh. This must be called "common"

epic://work/zcfd/run.1/
    The folder with the customised input for the first job, for example the *fv_1.py* python control file. 

epic://work/zcfd/run.2/
    The folder with the customised input for the second job, for example the *fv_2.py* python control file.


.. code-block:: python

    import pyepic
    from pyepic.applications.zcfd import ZCFDJob
    from pyepic.applications.base import JobArray

    client = EPICClient("your_api_token_goes_here")

    # Create a new JobArray called my_job_array with epic://work/zcfd/ as the array_root_folder folder
    job_array = JobArray("my_job_array", "epic://work/zcfd/")

    # Create two zCFD jobs using application version id "zcfd:2021.1.1"
    zcfd_job_1 = ZCFDJob("zcfd:2021.1.1", "zcfd_run_1", "epic://work/zcfd/run.1/", "fv_1.py", "box.hdf5", cycles=1000, restart=False, partitions=24)
    zcfd_job_2 = ZCFDJob("zcfd:2021.1.1", "zcfd_run_2", "epic://work/zcfd/run.2/", "fv_2.py", "box.hdf5", cycles=1000, restart=False, partitions=24)

    # Add the jobs to the array
    job_array.add_job(zcfd_job_1)
    job_array.add_job(zcfd_job_2)

    # Create the specification for submission to queue "aws:p4d"
    array_spec = job_array.get_job_create_spec("aws:p4d")
    
    # Submit the job array
    jobs = client.job.submit(array_spec)

    job_1_id = job[0].id
    job_2_id = job[1].id


Data
====
EPIC uses AWS S3 as an object store for data. The commands in this API use the boto3 library to communicate with the backend S3 services.
Using PyEpic data in your EPIC data store can be referenced using an EPIC data url. The client class for data functions is :class:`pyepic.client.EPICClient.data`.
For example if you have a folder in your EPIC data store called "MyData" then the data url would be "epic://MyData/", a file called "data.in" in that folder would be "epic://MyData/data.in".

Listing a folder
----------------
List a folder using the ls method.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    directory_listing = client.data.ls("epic://Folder/data/")
    
    print("Path | Name | Is folder? | File size")
    for item in directory_listing:
        print("{} | {} | {} | {}".format(item.obj_path, item.name, item.folder, item.size))


Downloading a file
------------------
PyEpic lets you download files directly to the local disk or to a File-like object.

To download to a file:

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    client.data.download_file("epic://MyData/data.in", "./data.in")


To download to an in-memory object, for example BytesIO:

.. code-block:: python

    import io
    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    # Create a new BytesIO object
    my_data = io.BytesIO()

    # Download contents of epic file into my_data
    client.data.download_file("epic://MyData/data.in", my_data)

    # Do something with the data in memory
    my_data.seek(0)
    my_data.read()


Uploading a file
----------------
In a similar way to downloading, PyEpic lets you upload from a local file of a file-like object. If you specify a directory as the target then the filename will be taken from the localfile if available.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    # Upload data.new to epic://MyData/data.new
    client.data.upload_file("./data.new", "epic://MyData/")


To upload to an in-memory object, for example BytesIO:

.. code-block:: python

    import io
    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    # Create a new BytesIO object
    my_data = io.BytesIO(b"This is new data")

    # Upload contents of my_data to epic file 
    client.data.upload_file(my_data, "epic://MyData/data.new")


Copying whole folders/directories
---------------------------------

upload_file and download_file are useful for dealing with single files but often you will need to upload or download whole folders.
To do this you can use the sync method. This takes a source_path and a target_path than can either be a local path or a remote epic:// url. 
This means you can either sync from your local files upto EPIC or from EPIC back to your local files.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    # Copy everything in my local dir ./data/ to a path on EPIC call new_data. 
    # If the files already exist in epic://new_data/ then still copy them if the local ones are newer.
    client.data.sync("./data/", "epic://new_data/", overwrite_existing=True)


You can get more information about the copy progress my passing a method in the "callback" kwarg.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    def my_callback(source_path, target_path, uploaded, dryrun):
        print("Callback. Source={} Target={} Uploaded={} Dryrun={}".format(source_path, target_path, uploaded, dryrun))

    # Copy everything in my local dir ./data/ to a path on EPIC call new_data
    client.data.sync("./data/", "epic://new_data/", callback=my_callback, overwrite_existing=True)


When uploading large datasets then the "dryrun" kwarg lets you see what PyEpic will do without actually performming the copies.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    def my_callback(source_path, target_path, uploaded, dryrun):
        print("Callback. Source={} Target={} Uploaded={} Dryrun={}".format(source_path, target_path, uploaded, dryrun))

    # Copy everything in my local dir ./data/ to a path on EPIC call new_data
    client.data.sync("./data/", "epic://new_data/", dryrun=True, callback=my_callback, overwrite_existing=True)


Deleting files or folders
-------------------------
PyEpic lets you delete indivdual files or whole folders from EPIC.

To delete to a single file:

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    client.data.delete("epic://MyData/data.in")


To delete a folder and its contents:

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")
    
    client.data.delete("epic://MyData/")
    

Desktops
========

Listing Desktop Instances
-------------------------
To list your desktop instances use the list and get_details methods in :class:`pyepic.client.EPICClient.desktops`.

.. code-block:: python

    from pyepic import EPICClient

    client = EPICClient("your_api_token_goes_here")

    # List all of my desktop instances
    desktops = client.desktops.list()

    # Get the details of desktop id 3
    desktop_instance = client.desktops.get_details(3)


Getting a quote for a Desktop
-----------------------------

PyEpic provides the helper class :class:`pyepic.desktops.Desktop` to help create Desktops in EPIC. To get a quote create an instance of this class and then use that the retrieve the quote via the desktop client class.
The valid application_version, node_type and connection_type values can be retrieved via :attr:`pyepic.EPICClient.catalog`..

.. code-block:: python

    from pyepic import EPICClient
    from pyepic.desktops import Desktop

    client = EPICClient("your_api_token_goes_here")

    # Create a desktop spec
    my_desktop = Desktop("epic://data_path/", application_version=5, node_type=1, connection_type=3)

    # Set the runtime to two hours
    my_desktop.runtime = 2

    # Get a quote for this desktop
    quote = client.desktops.get_quote(my_desktop.get_quote_spec()))

An example response for the quote is shown below.

.. code-block:: json

    {'cost': {'amount': 0.71, 'currency': 'GBP'}, 'reason': '', 'valid': True}


Launching a desktop
-------------------

PyEpic provides the helper class :class:`pyepic.desktops.Desktop` to help create Desktops in EPIC. To launch a desktop create an instance of this class and then use that to launch the desktop via the desktop client class.
The valid application_version, node_type and connection_type values can be retrieved via :attr:`pyepic.EPICClient.catalog`.

.. code-block:: python

    from pyepic import EPICClient
    from pyepic.desktops import Desktop

    client = EPICClient("your_api_token_goes_here")

    # Create a desktop spec
    my_desktop = Desktop("epic://data_path/", application_version=5, node_type=1, connection_type=3)

    # Set the runtime to two hours
    my_desktop.runtime = 2

    # Launch this desktop
    instance = client.desktops.launch(my_desktop.get_launch_spec()))

    # Get the newly created desktop instance id.
    id = instance.id

The launch method returns a :class:`epiccore.models.DesktopInstance` object that includes the newly created desktop instance ID. If there is an issue with the specification then launch will return the list of validation errors.
An example response is shown below.

.. code-block:: json

    {'application': {'application': {'description': 'zCAD is an CAD repair and '
                                                    'mesh generation tool from '
                                                    'Zenotech. EPIC will start a '
                                                    'DCV instance that you can '
                                                    'connect to with your browser '
                                                    'with zCAD and other Zenotech '
                                                    'tools installed and ready to '
                                                    'go.',
                                    'image': '/media/viz/zcad.png',
                                    'name': 'zCAD'},
                    'application_version': '2016.9',
                    'id': 5},
    'connection_string': None,
    'connection_type': {'description': 'Connect using Nice DCV in your browser',
                        'id': 3,
                        'name': 'DCV'},
    'created': datetime.datetime(2020, 11, 27, 9, 19, 47, 127429, tzinfo=tzutc()),
    'id': 11,
    'launched_by': 'Danny Develop',
    'status': 'new',
    'team': None}


Terminating a desktop
---------------------
Terminate a desktop using the terminate client method and the Desktops ID.

.. code-block:: python

    from pyepic import EPICClient
    from pyepic.desktops import Desktop

    client = EPICClient("your_api_token_goes_here")

    # Terminate desktop with ID 3
    client.desktops.terminate(3)


Teams
=====

.. code-block:: python

    from pyepic import EPICClient
    from pyepic.desktops import Desktop

    client = EPICClient("your_api_token_goes_here")

    # List teams
    teams = client.teams.list()
    
    for team in teams:
        print(team)

    # Get team ID 334
    team = client.teams.get_details(334)

Projects
========

Listing Projects
----------------
To list your project codes you can use the projects client.

.. code-block:: python

    from pyepic import EPICClient
    from pyepic.desktops import Desktop

    client = EPICClient("your_api_token_goes_here")

    # List projects
    projects = client.projects.list()

    for project in projects:
        print(project)

    # Get project ID 102
    project = client.projects.get_details(102)

Setting active projects on jobs
-------------------------------
You can set the project when submitting a new job by updating the project_id value on your job config object. For example to create a zCFD job with the project id set to 27:

.. code-block:: python

    from pyepic import EPICClient
    from pyepic.applications.zcfd import ZCFDJob

    client = EPICClient("your_api_token_goes_here")

    # Create a zCFD job using application version id "zcfd:2021.1.1"
    zcfd_job = ZCFDJob("zcfd:2021.1.1", "zcfd_case", "epic://work/zcfd/", "fv.py", "box.hdf5", cycles=1000, restart=False, partitions=24)

    # Run the job in project with ID 27
    zcfd_job.config.project_id = 27

    # Create the specification for submission to queue "aws:p4d"
    job_spec = zcfd_job.get_job_create_spec("aws:p4d")

    # Submit the job
    job = client.job.submit(job_spec)

    job_id = job[0].id

    print(f"Submitted job with id {id}")
