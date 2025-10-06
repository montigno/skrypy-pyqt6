Shared memory for inter-process
===============================

Skrypy provides a way to use shared memory, allowing different processes to access the same block of memory to ensure the exchange of parameters between them and avoid data redundancies.
The use of shared memory between processes is done both within the same machine and between client-cluster.


How to use
----------

   .. |pic1| image:: ../ressources/shm_create.png
      :width: 40%
      :alt: (shm create)

   .. |pic2| image:: ../ressources/shm_read.png
      :width: 40%
      :alt: (shm read)

   .. |pic3| image:: ../ressources/shm_consol.png
      :width: 80%
      :alt: (shm consol)

   .. |pic4| image:: ../ressources/shm_probe.png
      :width: 80%
      :alt: (shm probe)
      
.. |br| raw:: html

   <br />

This requires only 2 blocks: **SharedMemory_create** and **Shared_read** |br|
They are found in the library **Environment** then **shared_memory** |br|

|pic1| |pic2| |br|

After running the 2 diagrams, the results are displayed on the console
|pic3| |br| |br|
|pic4|

