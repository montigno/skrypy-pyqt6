Cluster (HPC)
=============

The procedure for installing Skrypy and its dependencies on a cluster is the same as for a local installation.
See with the cluster administrator.

Clusters configuration
^^^^^^^^^^^^^^^^^^^^^^^^

   .. |pic1| image:: ../ressources/menu_config_clusters.png
      :width: 50%
      :alt: (skrypy buttons)

   .. |pic2| image:: ../ressources/cluster_config.png
      :width: 60%
      :alt: (cluster config)

   .. |pic3| image:: ../ressources/cluster_config_test.png
      :width: 60%
      :alt: (cluster config)

You can put several clusters in the list. |br|
(Configuration to be done on your PC, not on the cluster)

1. Go to the `Configuration -> Clusters configuration` menu:|br|
|pic1|

2. A window opens:|br|
|pic2|

3. Fill in the fields  

- ``Host name``: user\@hostname

- ``Password``: your password to access the cluster.

- ``Skrypy directory on this cluster``: specifies the path where Skrypy is installed on the cluster

- ``Workspace on this cluster``: specifies the workspace on the cluster. This allows you to transfer your diagrams to be run on the cluster and can also (optional) be used to transfer your data to be processed.

- ``Max number of cpus to use``: maximum number of CPUs to use for your multiprocessing mode treatments. 

- ``X11 forwarding``: check this box if display returns (image or curves) are expected.

 
 .. attention::
    Depending on the cluster's graphics management capability, the result is not guaranteed.

- ``Pre-execution command``: this field allows you to enter shell-like instructions to be executed before your diagrams run. |br|
                             The example in the figure allows you to activate a conda RSS environment. You should clearly specify the conda source of the cluster.

4. Registration 

   ``Save As ...`` for a new cluster name  or ``Save`` for modification

5. Test

   ``Test``: allows you to perform connection tests, and checks if the paths exist.
   |pic3|

.. # define a hard line break for HTML
.. |br| raw:: html

   <br />
