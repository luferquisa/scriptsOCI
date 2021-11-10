# Scripts para facilitar administración de OCI

Este repositorio se actualizará con scripts que facilitan la administración en OCI.

<h2>Contenido:</h2>
<ol>
  <li>Consideraciones generales</li>
  <li>Inspección de políticas de backup en Block Volumes</li>
</ol>


<h2>Consideraciones generales</h2>

Se hará uso del SDK de OCI para Python, que permite la gestión de recursos por medio de código.

[SDK para Python]https://docs.oracle.com/es-ww/iaas/Content/API/SDKDocs/pythonsdk.htm

<h2>Inspección de políticas de backup en Block Volumes</h2>

Script: politicasBackupVolumes.py

El script tiene tres opciones de ejecución:

<ul>
  <li>All: Lista todos los Boot Volume y Block Volume en el tenant y sus politicas de backup</li>
  <li>conbackup: Lista los Boot Volume y Block Volume que tienen politicas de backup en el tenant</li>
  <li>sinbackup: Lista los Boot Volume y Block Volume que NO tienen politicas de backup</li>
</ul>

En caso de no pasar parámetro de entrada, se asume All
A la hora de ejecutar el script debe tenerse en cuenta la ruta del mismo,  en este caso estoy ejecutando desde el home, donde guarde el script.

Los resultados de la ejecución se pueden ver así:
<h3>Mostrar todos los volumenes</h3>

<em>python3 politicas_v4.py all</em>

Muestra el total de compartimientos a consultar y luego los discos por cada uno y para cada disco, sus políticas asociadas
![image](https://user-images.githubusercontent.com/9708604/141202864-545bf5f3-cc71-4b0c-9ad0-f2e2b0ca3574.png)

<h3>Mostrar solo volumenes que tienen backup</h3>

<em>python3 politicas_v4.py conbackup</em>
![image](https://user-images.githubusercontent.com/9708604/141202688-6f94f37b-b296-4ba5-bd9e-dc78bfc68bc2.png)

<h3>Mostrar solo volumenes que NO tienen backup</h3>

<em>python3 politicas_v4.py sinbackup</em>

![image](https://user-images.githubusercontent.com/9708604/141203052-96eebcad-debf-4ff9-8a0d-0547227fc243.png)






