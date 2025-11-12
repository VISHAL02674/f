#!/usr/bin/env python3
"""
Test script for sectionization module
Tests CV section extraction on sample resume texts
"""

from sectionization import parse_cv_sections_improved, extract_entities_improved
import json

# CV Text 1 - Ananth Bhat
CV_TEXT_1 = """## Ananth Bhat
## Cloud DevOps Engineer

### Contact

* **Address**: Bengaluru, KA, 560076
* **Phone**: 974 109 6236
* **E-mail**: ananthsbhat0806@gmail.com

### Professional Summary

A result-oriented professional with 5 Years 3 Months of experience in the field of automation and cloud DevOps in Capital Market Domain and networking domain.
Cohesive team worker, having strong analytical and problem-solving skills. Demonstrated proficient leadership by transferring the knowledge and supporting the team in delivery till project closure. Quickly adaptable to new technologies, environments and domains. Positive attitude and capable of bringing the team together to deliver results.

### Skills

* **DevOps, Cloud-based environments**: Very Good
* **Terraform, Version Control tool (Git)**: Very Good
* **Datadog, Splunk**: Very Good
* **AWS services like EKS,ECS,EC2,S3,cloudwatch, IAM etc**: Very Good
* **Shell script and unix commands**: Very Good
* **Docker, Kubernetes**: Very Good
* **Python**: Good
* **IBM UrbanCode (Udeploy) and Jenkins**: Good
* **Languages**:
  * **English**: Excellent
  * **Kannada**: Excellent

### Work History

#### Cloud DevOps Engineer
* **Company**: Cisco Systems India Pvt Ltd, Bangalore, Karnataka
* **Dates**: 2019-11 - Current
* **Roles and Responsibilities**:
  * Build Monitoring stack for new offers coming in to Cloud platform.
  * Performed many Platform upgrades like EKS Upgrades, Datadog Agent Upgrades, EMR upgrades and Calico Upgrade
  * Created many datadog alerts and dashboards using terraform which helps in detecting issue to maintain SLA.
  * Provide functional support to Kubernetes applications by configuring, deploying and monitoring applications on EKS cluster.
  * Terraformed and developed infra components, alerts and dashboards.
  * Worked on Kubernetes as orchestration methodology which provides clustering mechanism to Docker applications.
  * Deploying applications in production, testing, and Integration environments using YAML file through helm charts.
  * Integrated AWS, pagerduty, kong, tls and many more with datadog and started using metrics to create alerts.
  * Develop Alerting for ECR images in our repo that have about to expire or got expired.
  * Worked extensively on datadog to create separate organisation under one account, which helps in segregating metrics based on user need.

#### DevOps Engineer
* **Company**: Fidelity investments, Bangalore, Karnataka
* **Dates**: 2016-08 - 2019-11
* **Roles and Responsibilities**:
  * **Kubernetes Responsibilities**:
    * Provide functional support to Kubernetes applications by configuring, deploying and monitoring applications.
    * Worked on Kubernetes as orchestration methodology which provides clustering mechanism to Docker applications
    * Deploying applications in production, testing, and Integration environments using YAML file through kubctl commands.
    * Migrated Tomcat/WAS applications to cloud using containers and Kubernetes technologies.
    * Set up Autoscaling for container applications which is hosted on Rancher and PKS using Kubernetes based on CPU utilization of containers.
    * Setup and maintain several different configurations for Kubernetes.
    * Installing SSL certificates for Container applications and having good knowledge on certificates.
  * **Amazon web service Responsibilities**:
    * Provide functional support to AWS applications by configuring, deploying and monitoring applications.
    * Deployed applications using terraform Templates using Python scripts and CLI commands.
    * Created script to auto-scale tasks, rolling recycling of services and create UDeploy process for it.
    * Setup AVI load balancer for AWS applications for GTM setup.
    * Having good Knowledge on EKS, S3, Route53, EC2, PHZ, Load balancers, Certificate Manager and other useful services.
    * Created Python script to Authenticate AWS console and to validate Assume Role Using Boto3 Modules.

### Education

* **Bachelor of Engineering: Electronics And Communications Engineering**
* **University**: Visvesvaraya Technological University - Bangalore
* **Dates**: 2012-08 - 2016-08

### Accomplishments

* **AWARDS**:
  * Won "Spot award" for "Delivering Excellence" in 2017 @Fidelity investments.
  * Nominated twice for "Value Awards" in segments of "Delivering Excellence" and "Execute at Pace" in 2018 @Fidelity investments..
* Having received about 20+ Appreciation mails from Higher Management @Cisco Systems India Pvt Ltd"""

# CV Text 2 - Anil Kumar Annem
CV_TEXT_2 = """Anil Kumar Annem
Email: anilkumarscjp@gmail.com
Ph: +91-7349450050

CAREER SUMMARY

13+ years of software engineering experience and proficient knowledge in AWS, Kubernetes, Openshift, Ansible, Rundeck, API Gateway, OAuth, LogStash, Elasticseach, SOA, Web Services, REST, Web Methods, JMS, Java, Python.

4 years into building AWS infra, Kubernetes Container applications, Devops, Gito ps and CICD Automation.

4 years working as Engineering Manager/Lead owning responsibility to deliver end to end Design, Architecture and Dev Engineering.
Strong Technical expertise in IaC, PaaS, Containers, Devops, Deployment Automation on, REST API, SOA, Integration Patterns.
Good Knowledge in different Software Lifecycle methodologies like Classic, Unified SDM and Scrum framework using Agile Practices.

CERTIFICATION & EDUCATION

* Certified Kubernetes Application Developer (CKAD®) - 2020
* M.E. in Computer Science – 2006.
* B.Tech in Electronics and Instrumentation Engineering – 2003.

JOB HISTORY

* Goldman Sachs from Jan 2021 to till date.
* Standard Chartered GBS from July 2016 to Jan 2021.
* Royal Bank of Scotland from June 2015 to July 2016.
* Ford Technology Services India from October 2009 to May 2015.
* Geometric Ltd from Sep 2007 to October 2009.

TECHNICAL SKILLS

* Operating System: Windows, Linux
* Programming Languages: Java, Python, Go.
* Web Technologies: SOAP & REST Web Services, Servlets, JSP, Ajax
* Devops: AWS, Terraform, Kubernetes, Docker/Podman Rundeck, Ansible, JIRA, Jenkins, Artifactory.
* Logging & Monitoring: ELK, Prometheus and Grafana.
* Integration areas: WebMethods 9.5, JMS (Sync & Async), MQ, Web Services, REST Framework: JAX-ws, Struts, SpringBoot, Jdbc, Toplink.
* Application/Web Server: WebSphere, Apache Tomcat, Integration Server.
* IDE Tools: IBM RSA 8.5, IntelliJ, VS Code, Eclipse & SQL Developer.
* Version Control Tools: Gitlab, BitBucket, Clear Case, Accurev.

PROJECT SUMMARY

### Project #1
* **Title**: Cloud Platform Engineering - Jan 2020 to till date – TS 4
* **Skillset**: AWS, Terraform, ECS, FARGATE, Docker, Gitlab, Python.
* **Role**: Engineering Manager/Lead
* **Responsibilities**:
  * Cloud Containers Engineering: Define, Drive and Contribute to Devops, Containers Road Map on AWS for Business Unit.
  * Solution Design and Support: Design, Solution, Develop and Support Blue/Green Deployments, Container AutoScaling , Exec, Application Solutions, Datadog Observability metrics.
  * Collaborate: Contribute in bringing serverless solutions, Automation features for r adoption.

### Project #2
* **Title**: Platform and API Engineering - Sep 2018 to till date – TS 6
* **Skillset**: AWS, Terraform, Openshift/Kubernetes, Docker, Podman, Ansible, Rundeck, Jenkins, BitBucket, Micro Services Routing, Kong API Gateway, WSO2 ID Management, LogStash, Elastic Beats and ElasticSearch.
* **Role**: Engineering Manager/Lead
* **Responsibilities**:
  * Micro service router Platform: Overall responsibility to Design, Develop, Test and Deliver Smart-Router, Layer-7 monitoring and logging to production.
  * Api Gateway Platform: Lead the Design, Architecture and Development of API Gateway Platform on AWS.
  * Openbanking Platform: Design CICD for OpenBanking Platform – Rundeck, Ansible, Jenkins and Gradle.
  * Drive discussions with Business Stakeholders, Product Owner and CTMs on features , benefits and test results.
  * Complete Ownership in delivery of CICD platform for OpenBanking Platform in concurrence with Standards and Product Owner.

### Project #3
* **Title**: Enterprise Data Integration (EDMI) - June 2016 to Aug 2018 – TS 11
* **Skillset**: WebMethods, Java, SOAP WebServices, REST, JMS, MQ Adapter, TCP Adapter, Message Broker, Security (Authn, Authz, SSL/TLS).
* **Role**: Technical Manager.
* **Responsibilities**:
  * Solution Design – Responsible for Design and presenting of Integration solution.
  * Development and Release – Adhere to design. Ownership of end to end lifecycle of integration solution.
  * Delivery Management – Handle delivery timelines, conflicts, people management, solution risks.

### Project #4 - Royal Bank of Scotland
* **Title**: Security Platform Enabler - May 2015 to June 2016 – TS 3
* **Services**: Signing Service, Policy Information Service, Credentials and Account Management Service"""

# CV Text 3 - Ashwini Thombre
CV_TEXT_3 = """# Ashwini Thombre
+91 7892591830| ashwini.thombre7392@gmail.com

## Professional Summary
- 5.10 years of experience in IT industry with focus on Software Configuration, Integration, Build/Release Management and Devops for several market driven international organizations for around 3.5+ years and as BigFix admin for 2.4 years.
- Good experience in Version Control/Source Code Management tools like GIT and hosting/client tool like Git-Hub.
- Experienced in Jenkins by installing, configuring and maintaining for purpose of continuous Integration (CI) and for end-to-end automation for all build and deployments and creating Jenkins CI pipelines.
- Experience in executing parallel jobs with Jenkins Master-Slave Architecture.
- Hands-on Experience on Binary Repository Manager like Nexus for artifact storage and for monitoring artifacts for deploying it to application servers.
- Good experience in creating and configuring new Build jobs, Plug-ins Management, distributed builds using Master/Slaves and other administration tasks in Jenkins.
- Having good Experience in Configuration Management tools such as Ansible for Deployment on Multiple platforms.
- Experience on Container based technologies like Docker and creating Docker Images using Docker Files.
- Worked on Kubernetes cluster setup, deployments, rolling updates and Kubernetes objects.
- Deployed AWS services using Terraform modules, resources.
- Worked on layers of AWS offering and integration and migration of existing solution into virtualized hosting environments using EC2, S3, VPC, ELB, autoscaling with CloudWatch metrics integration.
- Configured Network architecture on AWS with VPC, Subnets, Internet gateway, NAT, Route tables to ensure a secure zone for organization in AWS public cloud
- Design roles and groups for users and resources using AWS Identity Access Management (IAM).
- Launching Amazon EC2 Cloud Instances using Amazon Images (Linux/Ubuntu) and Configuring launched instances with respect to specific applications
- Create/Manage DNS records on Route53
- Created and configured EC2, elastic load balancers and auto scaling groups to distribute the traffic and to have a cost efficient, fault tolerant and highly available environment.
- Experienced in creating multiple VPC's and public, private subnets as per requirement and distributed them as groups into various availability zones of the VPC.
- Used security groups, network ACL's, internet gateways and route tables to ensure a secure zone for organization in AWS public cloud.
- Worked on IBM configuration tool BigFix for installation, implementation, customization and performance tuning of BigFix components.
- Maintaining the monitoring Infra (BigFix server, Relays, clients).
- Experience in scheduling BigFix patching over windows servers.
- Experience in troubleshooting Besclient and Relay issues.
- Experience with Agile Development Methodology.

## Technical Expertise

| Cloud Environments & Services | AWS (EC2, Route53, S3 ,ELB, VPC, Auto scaling groups ,Cloud Front, Cloud watch, IAM) |
| Configuration management tool | Ansible |
| CI/CD & Build tool | Jenkins, Maven |
| Containerization Tools | Docker, Kubernetes |
| Version Control Tools | Git, GitHub |
| Scripting | Shell |
| Monitoring | Prometheus |

## Work History

### Service Delivery Specialist: AWS-DevOps
Kyndryl Solutions Private Limited-(IBM)
May 2018 to Till Date

- Maintain Git Repositories, Handling Releases and Branching activities for Git.
- Handle multiple builds from Development team, create build jobs in Jenkins and perform deployment activities.
- Implemented a Continuous delivery pipeline with Ansible, Docker, Jenkins, and Kubernetes.
- Created Jenkins job for automation of build and deployment process as part of continuous integration strategy.
- Responsible for continuous integration (CI) and continuous delivery (CD) process implementation using Jenkins along with Shell scripts to automate routine jobs.
- Worked on various migrations of docker volumes.
- Involved in Writing Docker files to build customized images for creating containers.
- Worked on Docker container to create Docker images for different environments.
- As most of the infrastructure is hosted in AWS cloud, I am responsible for creating and managing EC2 Instances Instance using Amazon Images (Linux/Ubuntu) and Configuring launched instances with respect to specific applications.
- Built S3 buckets and managed policies for S3 buckets and used S3 bucket and Glacier for storage and backup on AWS.
- Install IIS on windows servers and configure it run as a website.
- Implemented cross region replication in s3 buckets to provide low latency for compliance requirement.
- Experienced in configuring SQS service to trigger lambda function.
- Created snapshots to take backups of the volumes and images to store launch configurations of the EC2 instances.
- Create/Manage DNS records on Route53.

### Service Delivery Specialist
Kyndryl Solutions Private Limited-(IBM)
Jan 2016 – May 2018

- Providing solutions to issues in a steady state environment.
- Business communication and requirement gathering.
- Acting as a focal for multiple customer accounts.
- Accountable for end-to-end service delivery.
- Manage project meetings, RFS requests etc.
- Performing Daily Health checks on the Infra servers.
- Providing knowledge transfer to the teams.

### Project:
Client : FCA-Chrysler
Tools Used : BigFix

- Responsible for installation, implementation, customization and performance tuning of BigFix components.
- Maintained BigFix infrastructure (BigFix server, Console and Relays).
- Experience in scheduling BigFix patching over windows servers.
- Experience in troubleshooting Besclient and Relay issues.
- Generating patch scan reports for windows and Unix server with the help of web reports.
- Installing Besclient agents with the help of platform teams.
- Supporting Platform team for creating Baseline for monthly patching.
- Creating custom Fixlet and Analysis based on platform team requirement.
- Working on Service now tickets for higher CPU utilization and space for Besclient.
- Help in running automation scripts through IEM console.
- Identify, manage, and monitor for vulnerabilities that may affect compliance requirements and change management procedures.

## Education

2014 BE from Sagar institute of research, technology and science, Bhopal
2010 Intermediate from Bal Bharati Public School, Bhopal
2008 SSC from Bal Bharati Public School, Bhopal

I hereby declare that all information furnished above is true to the best of my knowledge and belief.

Ashwini Thombre"""


def print_section_results(cv_name, sections, detailed=True):
    """Print the extracted sections in a readable format"""
    print("\n" + "="*80)
    print(f"RESULTS FOR: {cv_name}")
    print("="*80)

    print(f"\n📊 Sections Found: {len(sections)}")
    print(f"Section Names: {list(sections.keys())}")

    if detailed:
        print("\n" + "-"*80)
        for section_name, content in sections.items():
            print(f"\n🔹 SECTION: {section_name.upper()}")
            print(f"   Lines: {len(content)}")
            print(f"   First 5 lines:")
            for i, line in enumerate(content[:5], 1):
                preview = line[:100] + "..." if len(line) > 100 else line
                print(f"   {i}. {preview}")
            if len(content) > 5:
                print(f"   ... and {len(content) - 5} more lines")
        print("-"*80)


def test_all_cvs():
    """Test all three CV samples"""

    test_cases = [
        ("CV #1: Ananth Bhat (Cloud DevOps Engineer)", CV_TEXT_1),
        ("CV #2: Anil Kumar Annem (Engineering Manager)", CV_TEXT_2),
        ("CV #3: Ashwini Thombre (AWS-DevOps Specialist)", CV_TEXT_3)
    ]

    print("\n" + "🚀 STARTING SECTIONIZATION TESTS")
    print("="*80)

    for cv_name, cv_text in test_cases:
        try:
            # Extract sections
            raw_sections, final_sections = parse_cv_sections_improved(cv_text)

            # Print results
            print_section_results(cv_name, final_sections, detailed=True)

            # Print summary statistics
            total_lines = sum(len(content) for content in final_sections.values())
            print(f"\n📈 Summary Statistics:")
            print(f"   Total sections: {len(final_sections)}")
            print(f"   Total content lines: {total_lines}")

        except Exception as e:
            print(f"\n❌ ERROR processing {cv_name}:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*80)
    print("✅ TESTING COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_all_cvs()
