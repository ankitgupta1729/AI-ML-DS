### A. Fundamentals

1. Data is everywhere and everyone needs to leverage it.
2. Today, every company wants to be a Data+AI company.
3. Leaders are seeing the benefits with Data and AI:
   (i)   Cost Reduction: CFOs seek lower TCO to enable other investments or to fund new initiatives
   (ii)  High quality data that ise secure and consumable
   (iii) Transformational AI for their organization and business. Companies want AI to drive innovation internally and improve customer experiences

4. The data estate is highly fragmented and complex:
   (i)   Generative AI
   (ii)  BI
   (iii) Governance
   (iv)  Orchestration and ETL
   (v)   Data Lake
   (vi)  Data Science
   (vii) Streaming
   (viii) Data Warehouse
   (ix)   Machine Learning

etc..

It's a complexity nightmare of high costs and proprietary formats

5. This complexity stops success

Let's say that your organization has duplicate platforms, Platforms that might do similar things or even just the same thing but one might do one thing better than the other. While your costs grow across these platforms, you have less money available to invest in other area of your business.

What about that single source of truth for your data ?

If you have data living in multiple locations or being moved from one location to another, which data should your team members use ?

How do they know what data to use ? What happens when the data is updated ? How can you ensure that you have high quality data that is secure and consumable if you don't have a clear, well-defined single source of truth ?

And finally, with AI, like we mentioned earlier, every organization dreams of being an AI organization but most AI projects don't make it into production for many reasons.

6. Databricks was founded in 2013 by a team of researchers at the University of California Berkeley. This team includes the original creators of Apache Spark, Delta Lake and ML flow.

7. The mission of Databricks is to Democratize Data and AI by helping data teams to solve the world's toughest problems.

8. In 2020, we introduced the world's first and only Lakehouse platform in the cloud, combining the best of data warehouses and data lakes in an open and unified platform for data and AI workloads.

And in 2021, our founders, alomg with individuals from UC Berkeley and Stanford University, coined the term data Lakehouse architecture pioneered by Databricks. The Lakehouse architecture took the worls by storm, and as of today, 74% of global CIOs have reported they utilize the Lakehouse in their data estate.

9. The Data Lakehouse is an open, unified foundation for all your data.

Layers:

(i)   Lakehouse: Data Science and AI; Data Warehousing; Ingest, ETL, Streaming, and Orchestration; Analytics and Business Intelligence

(ii)  Unity Catalog
(iii) Delta Lake, Iceberg, Parquet
(iv)  Open Data Lake
(v)   All Raw Data (Logs, Texts, Audio, Video, Images)

10. 2023: Rise of GenAI

In 2023, GenAI hit the data and AI scene and has since then truly taken over the globe through its prevalence of use rather quickly.

- 91% of organizations are experimenting with or investing in GenAI.
- 75% OF ceoS SAY COMPANIES WITH ADVANCED GenAI will have a competitive advantage
- 40% increase in performance of employees who used GenAI.

11. Data Lakehouse(An open, unified foundation for all your data) + Generative AI (Easily scale and use data and AI) = Data Intelligence Platform (Democratize data + AI across your entire organization)

12. There is no data intelligence without a lakehouse foundation. A lakehouse is a foundation and is essential for a data intelligence platform. 

13. Data Management Systems:
    
A. Data Warehouse: A traditional data warehouse is a structured repository that stores data from various sources in a well organized manner. It aims to provide a single source of truth for business intelligence and analytics. Data is cleaned, transformed and integrated into a structure that is optimized for querying and analysis. 

Traditional data warehouse work well with structured data. Think of data stored in an Excel format for one example with rows and columns but what about other types of data ? Things like images, audio files, videos ? Data warehouses can't support unstructured and semi-structured data such as videos, images and large amount of freeform text. 

Traditional data warehouses are also very expensive to scale up due to vendor costs for compute power and storage capacities and they're often proprietary and have very closed data formats. Think of the different file formats that are native to a company. They have specific encoding schemas and can often only be decoded by the hardware created by that company. 

So,

#### Strengths of Data Warehouses:

- Purpose-built for BI and reporting
- Meant to unify disparate systems
- House structured, clean data with a standardized schema
  
#### Downsides of Data Warehouses:

- No support for unstructured and semi-structured data
- Poor support for data science, AI and streaming use cases
- Uses closed and proprietary data formats
- Expensive to scale up

B. Data Lakes:

A data lake is an unstructured or semi-structured data repository that allows for the storage of vast amounts of raw data in its original format.

Data links are designed to ingest and store all types of data, structured data like in a data warehouse but also semi-structured or unstructured data, which is critical for today's machine learning and advanced analytics use cases and data can be stored without any predefined schema. 

Data lakes are often used to consolidate all of an organizations's data into a single central location. 

In a data lake, data is in all stages of the refinement process that it can be in stored in. 

That means there's raw data that can be ingested and stored right alongside with an organization's structured data sources like database tables as well as intermediate data tables generated in the process of refining that raw data. 

However, a data lake has a few drawbacks. First, they are difficult to set up for users, more familiar with data warehouse technology. Second, since data can be stored in all stages of its refinefent process, it's often un-validated and dirty or not usable for BI. If setup incorrectly, it will be too lax of a design and a data lake could become more of a data swamp of large amount of dirty data in unverified and uncontrolled groups making some governance and security issues. 

#### Strengths of Data Lakes:

- Store any kind of data
- Inexpensive storage
- Good starting point
- Support for GenAI and streaming use cases

#### Downsides of Data Lakes:

- Complex to set up
- Poor BI performance
- Can become unreliable data swamps
- Governance concerns
- Warehouses still needed

14. Data Lakehouse:

You can think of a data lake house as the best of both worlds. It is built on a data lake, meaning that it can store all data of any type together, and it implements similar data structures and data management features that are found in data warehouses.

Data lakehouses are also open environments built in the cloud, preventing vendor lock-in. And because they use cheap cloud storage as a foundation, they are cost efficient and scalable. 

Merging together data warehouses and data lakes into a single systems means that data teams can move faster as they have one singular unified architecture for all of their data and AI needs. This means that data practitioners can work in one place with their diverse workloads from data analytics to BI to machine learning, data engineering, generative AI and more.

Second, they are able to use data without needing to access multiple systems. 

And third, they have the most complete and up-to-date available for data science, machine learning and business analyst reports. 

So, Lakehouse is the combination of both data warehouse and data lakes.

Lakehouse:

A. All machine learning, SQL, BI and streaming use cases
B. One security and governance approach for all data assets on all clouds
C. An open and reliable data platform to efficiently handle all data types

15. So, what is data intelligence ?

Data intelligence is the process of using AI systems to learn, understand and reason on an organization's data, enabling the creation of custom AI applications and democratizing access to data across the enterprise. 

16. Where your data lives?

Cloud Data Storage providers supported by Databricks: Amazon Web Services(AWS), Microsoft Azure, Google Cloud Provider. 

17. Serverless compute to power workloads:

#### Benefits:

- Simple and Fast: No knobs, Fast startup, For any practitioner
- Efficient: Fully managed and versionless, Paying only what you use, Strong cost governance
- Reliable: Secure by default, Stable with smart fail-overs

DB SQL,Lakeflow,AI/BI,Mosaic AI --> Serverless Compute (Hands-off auto optimized compute managed by Databricks) --> Storage

Databricks Compute refers to the selection of computing resources available in Databricks.

Serverless compute on Databricks is a system designed to eliminate complexities associated with managing infrastructure, making it accessible even to those without technical expertise.

18. Databricks is a unified platform created for all data practitioners to do their work in one place. 

Databricks Data Intelligence Platform contains services related to Data Science, Machine Learning, Generative AI, Orchestration and ETL, Data Engineering, Data Analysis, Data Warehousing, Data Governance etc. 

##### 4  product pillars of the Databricks data intelligence platform:

- Lakehouse: Ingest, ETL, Streaming
- Databricks SQL: Data Warehousing
- AI/BI: Business Intelligence
- Mosaic AI: Artificial Intelligence

Your data stored in an open, broadly accessible lakehouse format.

19. Achieving data intelligence begins with getting your data into the platform, which is the realm of data engineering and for this databricks offers:

- Lakeflow: Reliable and automated dataflow from systems-of-record. "Connect" provides support for connecting to your business data sources. "DLT" makes creating reliable data pipelines a simple and efficient process and "Jobs" allows you to orchestrate everything within the platform for analytics and AI needs. 

Lakeflow connect offers no code connectors making it simple to get data into Databricks. This ensures that data pipelines are safe and secure by providing full observability.

Lakeflow connect utilizes smart resource allocation through its ability to autoscale for production workloads.

DLT is the first ETL framework that uses a simple declarative approach to building reliable data pipelines. DLT automatically manages your infrastructure at scale. So, data analysts and engineers can spend less time on tooling and focus on getting value from data.

With DLT, engineers are able to treat their data as code and apply modern software engineering best practices like testing, error handling, monitoring and documentation to deploy reliable data pipelines at scale and unlike other products that force you to deal with streaming and batch workloads separately, DLT supports any type of data workload with a single API. So, data engineers and analysts alike can build cloud scale data pipelines faster and without needing to have advanced data engineering skills while supporting both python and SQL.

And the last feature in lake flow is jobs. Lakeflow jobs allows you to orchestrate all types of jobs within the platform with real-time triggers, predefined schedules and on-demand execution. Any data practitioner can make use of lake flow jobs for their work. With realtime monitoring built into the system, users can monitor, diagnose, and resolve errors within pipelines quickly and efficiently. Users simply choose the type of task to complete, define how that task should be executed in the control flow, and set the type of trigger necessary to kick off the job. 

20. What is data intelligence for analytics and BI ?

Once you have all your data in, now you need to make use of that data through analysis and business intelligence.

For data warehousing analytics, Databricks offer databricks sql. Databricks SQL is a collection of tools for BI and data analytics. On the surface, it supports the use of ANSI SQL through a full featured SQL editing environment within the platform. However, under the cover, Databricks SQL has been optimized specifically for SQL workloads and production environments offering world-class price performance. Paired wih a unified storage layer, Databricks SQL provides you with the support for both batch and streaming workloads for many enterprise level use cases in data analytics and BI. With alerts and schedules, you are able to keep track of how your queries are performing and automatically refresh results as needed. The best part of this, it is all available in a single platform, keeping your data and users across teams together to avoid working in silos. And with AI integrated directly into the platform, users can get answers quicker through the use of natural language queries. 

21. Complete data warehousing capabilities:

##### Foundational Functionality:

- Serverless Warehouses
- 1P/3P Connectors
- CDC Support
- Streaming Tables
- Materialized Views
- Autoloader for ingest
- Scheduled Workflows
- 1P/3P Orchestration
- SQL Editor
- Python/Go Connectors
- SQL Rest API
- Views/Temp Views
- SQL Scripting
- H3 GeoSpatial
- Spatial SQL (ST_)
- Foreign/Primary Keys
- Lateral Col Alias
- Named Arguments
- HyperLogLog
- Array Functions
- Identifier Clause
- Variant Data Type
- ANSI SQL
- SQL UDFs
- Session Vars
- SQL Alerts
- Dashboards
- Dashboard Sharing
- Publish to Tableau
- Cloud Fetch
- Python UDFs
- Row Level Concurrency

##### Governance and Administration:

- Data Quality Monitoring
- Table ACLs
- Lakehouse Federation
- HMS Federation
- Table Lineage
- Entity Relation Diagram
- Row/Col Security
- OAuth
- ABAC
- Marketplace
- 100K+ User Support
- Monitor Permissions
- Billing System Tables
- Internet On/Off
- Queries System Table
- Warehouse Sys Table
- WH Events Sys Table
- Query Duration Limits
- Foreign/Primary Keys
- Query History
- Query Profiling
- Warehouse Monitoring

21. AI/BI:

Databricks currently has two AI/BI tools to support these endeavors:

- AI/BI Dashboards to analyze and visualize data (Get useful results with AI-powered understanding): It is a built-in environment for presenting and reviewing data analytics and BI work. 
- AI/BI Genie: It is a space where users can ask questions directly to the data itself using natural language prompts. This essentially allows users to talk to the data, removing the analyst as the middleman between the end user and the data.

Databricks offers powerbi and tableau integrations.

22. What is data intelligence for AI applications?

- Mosaic AI: Create domain-specific agentic applications

In 2023, Databricks acquired Mosaic ML. 

Mosaic AI is a end-to-end support for GenAI and ML model development and serving.

DSML=Data Science and Machine Learning

One of the key capabilities under the Mosaic AI umbrella that serves the needs of both DSML and GenAI is our model serving capability.

Mosaic AI model serving provides an environment for delivering both traditional and large language models to production. With a single interface, you can manage all your model deployments from one location, govern and monitor them all while managing their costs with autoscaling and optimization.

Serving acts as a catalyst for getting models to production. In a typical ML or GenAI model lifecycle, serving is tightly integrated with model registry. The model registry allows efficient management and staging of models while model serving facilitates deployment of any version of the model through rest endpoints, providing flexibility and ease of use for real-time applications. And all of this is based on the implementation of mlflow through the databricks platform.

23. General Intelligence vs Data Intelligence:

General Intelligence means large models trained on the entire web leveraging scaling laws.

Data Intelligence means AI agents that reason on your data and solve domain-specific problems.

24. Databricks is built to support the data format you choose in an open source based storage layer. This storage layer enhances data lakes by adding reliability, performance, governance and quality. It achieves this by implementing a transactional layer on top of the open parquet, iceberg or delta data format, enabling the lakehouse paradigm that strengths of data lakes and data warehouses. This storage layer allows you to unify your data across your entire ecosystem in one location, allowing you to break free from vendor specific formats. 

25. Delta Sharing:

It is an open cross-platform sharing tool easily allowing you to share existing data in delta iceberg or parquet format without having to establish new ingestion processes to consume data.

26. Databricks Marketplace:
It is a open marketplace for all your data, analytics and AI.

It is an open exchange for all data products:

- Datasets
- Notebooks
- Dashboards
- ML Models
- Solution Accelerators
- Data Files
- Data Tables 

etc..

It is powered by Delta Sharing

27. 



