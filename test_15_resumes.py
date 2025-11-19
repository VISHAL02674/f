"""
Test sectionization on 15 real-world resumes that are currently failing
"""

from sectionization import parse_cv_sections_improved

# Resume 1: Anil Kumar Annem
CV_1 = """Anil Kumar Annem
Email: anilkumarscjp@gmail.com
Ph: +91-7349450050

CAREER SUMMARY

13+ years of software engineering experience and proficient knowledge in AWS, Kubernetes, Openshift, Ansible, Rundeck, API Gateway, OAuth, LogStash, Elasticseach, SOA, Web Services, REST, Web Methods, JMS, Java, Python.

4 years into building AWS infra, Kubernetes Container applications, Devops, Gito ps and CICD Automation.

4 years working as Engineering Manager/Lead owning responsibility to deliver end to end Design, Architecture and Dev Engineering.
Strong Technical expertise in IaC, PaaS, Containers, Devops, Deployment Automation on, REST API, SOA, Integration Patterns.
Good Knowledge in different Software Lifecycle methodologies like Classic, Unified SDM and Scrum framework using Agile Practices.

CERTIFICATION & EDUCATION

Certified Kubernetes Application Developer (CKAD®) - 2020
M.E. in Computer Science – 2006.
B.Tech in Electronics and Instrumentation Engineering – 2003.

JOB HISTORY

Goldman Sachs from Jan 2021 to till date.
Standard Chartered GBS from July 2016 to Jan 2021.
Royal Bank of Scotland from June 2015 to July 2016.
Ford Technology Services India from October 2009 to May 2015.
Geometric Ltd from Sep 2007 to October 2009.

TECHNICAL SKILLS

Operating System: Windows, Linux
Programming Languages: Java, Python, Go.
Web Technologies: SOAP & REST Web Services, Servlets, JSP, Ajax
Devops: AWS, Terraform, Kubernetes, Docker/Podman Rundeck, Ansible, JIRA, Jenkins, Artifactory.
Logging & Monitoring: ELK, Prometheus and Grafana.
Integration areas: WebMethods 9.5, JMS (Sync & Async), MQ, Web Services, REST Framework: JAX-ws, Struts, SpringBoot, Jdbc, Toplink.
Application/Web Server: WebSphere, Apache Tomcat, Integration Server.
IDE Tools: IBM RSA 8.5, IntelliJ, VS Code, Eclipse & SQL Developer.
Version Control Tools: Gitlab, BitBucket, Clear Case, Accurev.

PROJECT SUMMARY

Project #1
Title: Cloud Platform Engineering - Jan 2020 to till date – TS 4
Skillset: AWS, Terraform, ECS, FARGATE, Docker, Gitlab, Python.
Role: Engineering Manager/Lead
Responsibilities:
Cloud Containers Engineering: Define, Drive and Contribute to Devops, Containers Road Map on AWS for Business Unit.
Solution Design and Support: Design, Solution, Develop and Support Blue/Green Deployments, Container AutoScaling , Exec, Application Solutions, Datadog Observability metrics.
Collaborate: Contribute in bringing serverless solutions, Automation features for r adoption."""

# Resume 2: Abhay Kumar
CV_2 = """Abhay Kumar
Staff DevOps & Security Engineer
+91-789-354-4027 abhay.krp@gmail.com Hyderabad, India

PROFESSIONAL SUMMARY

A DevOps engineer with 9 years' experience in DevOps Technology and Cloud Security including Cloud Infrastructure Management and Infrastructure Automation, Cloud Security, Configuration Management, CI/CD process, Containerization Techniques and Orchestration Tools like Docker Swarm, Kubernetes, Scripting, Automations etc.

TECH STACK

Cloud AWS, GCP
--- ---
Scripting Shell, Python, Perl
Build/ CICD Tools Gitlab, Jenkins, Bitbucket, CodePipeline, CodeBuild, Ant, Maven
DevOps Tools Ansible, Puppet, Docker, Docker Swarm, ECS, ElasticSearch, Kibana, Docker, , Artifactory, Terraform Cloudformation
Monitoring Tools Zabbix, Grafana, Nagios, New Relic, Cloudhealth, PagerDuty,
Databases MySQL, Dynamodb, MongoDB, Redis
Web Servers Apache Tomcat, Apache HTTP Server, Nginx
Operating Systems Linux Red Hat, Debian, MacOS
Security Tools Rapid7, Burp Suite, Scout2, GuardDuty, AWS Config ,AWS WAF, WebFuzzer, OWASP, Sonarqube, Codacy etc.

EXPERIENCE

Staff DevOps and Security Engineer Electronic Arts Hyderabad, India / Full Time Present"""

# Resume 3: Adarsh Patnaik
CV_3 = """Adarsh Patnaik
DevOps Engineer Email: adarshzup@gmail.com Cell: +91 9692199376 Linked In: inkd.in/Adarsh

A dynamic IT professional with 4 years of IT experience which includes experience in Cloud services and Devops Engineer. Experience in planning, commissioning and managing applications on cloud. Good awareness on devops tools. Hands-on experience working with AWS & IBM Cloud for both windows and linux servers.

Experience automating deployment in Microservice architecture, Node JS.
Expertise in tools like Git, Maven, Jenkins, Ansible and Sonarqube. Implemented Shell scripting and Cronjobs.
Good knowledge in maintaining Git Repositories such as Git and GITHUB. Strong background in Branching, Merging, Tagging, and maintaining the version across the environments.
Worked on Jenkinsfile and Yaml script for continuous integration and for automation for all build and deployments.
Good interaction with developers, managers and team members to coordinated job tasks and strong commitment to work.

TCS
Role: System Engineer
Duration: Mar, 2018 – Sep, 2021

IBM
Role: Senior System Engineer
Duration: Sep, 2021 - Present

Completed Bachelor of Science in Information Technology degree in 2017 from Utka IUniversity, Bhubaneswar.

Area of Expertise:
Roles & Responsibilities:

System Engineer at TCS
Mar 2018 – Sept 2021
Administered over all configuration of Insurance Apps from on-prem to AWS EC2 and Azure VM.
Performance Tuning of Oracle Databases by monitoring AWR, ADDM report, implementing migration and data restoration and patching.
Security tools like Splunk for the monitoring data log. Used Splunk for the monitoring data log.
Applied shell scripts (bash) and Cron-jobs for the scheduled automated tasks

Senior System at IBM
Oct 2021 – Till now
Handled Build and release in multiple client engagement supporting both Linux and Windows
Upgraded the application server and dependencies for client engagement
Worked with developers and clients to ensure smooth deliveries with zero defects.
Helped Teams to learn about Devops and implement CI/CD though Jenkins and ansible playbook
Having good understanding on Docker containerized tool and Kubernetes.

Certifications:
Azure Associate Administrator by Microsoft

Professional Snapshot
Organisational Experience
Educational Qualifications

Skill Sets
SCM Tools GIT, GITHUB
Build Tools Maven, Gradle, Node"""

# Test all CVs
test_cases = [
    ("Anil Kumar Annem", CV_1),
    ("Abhay Kumar", CV_2),
    ("Adarsh Patnaik", CV_3),
]

print("=" * 100)
print("TESTING SECTIONIZATION ON 15 RESUMES")
print("=" * 100)

for i, (name, cv_text) in enumerate(test_cases, 1):
    print(f"\n{'='*100}")
    print(f"RESUME {i}: {name}")
    print(f"{'='*100}")

    raw_sections, sections = parse_cv_sections_improved(cv_text)

    for section_name, content in sections.items():
        if content:  # Only show non-empty sections
            print(f"\n[{section_name.upper()}]")
            print(f"Lines: {len(content)}")
            for line in content[:5]:  # Show first 5 lines
                print(f"  - {line}")
            if len(content) > 5:
                print(f"  ... and {len(content) - 5} more lines")

    print()
