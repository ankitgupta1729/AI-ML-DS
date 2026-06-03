1. Big Picture of Google Cloud Platform(GCP):

Google is one of the hyper scale infrastructure providers. Its footprints spans multiple continents including Asia, Europe and the Americas.  

Google has 20 regions, 61 zones, 134 network edge locations and available in 200+ countries and territories. 

A region is a collection of multiple data centers. You can associate a zone with a data center. And, when Google launches a new region then it typically has at least 2 zones. 

Zone provides high availability, reliability and redundancy to customers.

When customers launch applications they use more than one zone, making their own application highly available.

Network edge locations deliver static content which will enhance the user experience.

2. Building blocks of Google Cloud Platform(GCP):

Like most of the cloud providers, google has an expensive set of offerings. This building block of stack is is given below:

- Compute: It is most critical building block of cloud infrastructure.
- Storage: It provides durability and persistence to applications.
- Network: It enables communication across multiple applications and services offered by Google.

On top of these core foundational building blocks, we have additional services like databases that includes both NoSQL databases and relational databases followed by a set of data and analytical services that offers business intelligence and data warehouse in the cloud. 

Google is known for its expertise in AI and Machine Learning, so, there are quite a few services that deliver machine learning and AI based services.

For enterprises, there are a set of services that make it possible to deploy hybrid and multi cloud capabilities, API management and even migrating workloads from on-premises to the cloud.

We then have security and DevOps that cuts across the stack because these are not specific to a layer, they are important for all the services and all the applications deployed on GCP, so they essentially cover the entire stack.

Finally we have management tools which deliver services through which customers can interact and manage their deployments and cloud infrastructure services. 

![stack](./images/1.png)

3. Key GCP Services:

Here we will see the most critical and most building block services of GCP.

A. Compute:

It is one of the foundational aspects of the GCP. There are multiple services when it comes to compute.

- Compute Engine: It delivers infrastructure-as-a-service(IaaS).
- App Engine: It delivers platform-as-a-service(PaaS).
- Kubernetes Engine: Container has service and it is delivered by kubernetes.
- Container Registry: It manages docker container images.
- Cloud Functions: It delivers functions-as-a-service(FaaS).

B. Storage and Database Services:

It delivers persistence and durability. It includes:

- Cloud Storage:
- Cloud Bigtable:
- Cloud Datastore:
- Cloud SQL:
- Cloud Spanner:
- Persistence Disk

C. Network Services:

It provides connectivity and security for all the services and applications deployed on GCP. It includes

- Cloud Virtual Network: It provides hybrid and isolated network capabilities within the public cloud.  
- 