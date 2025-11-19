"""
Final validation test on complete resumes from the user's 15 samples
"""
from sectionization import parse_cv_sections_improved

# Resume 4: Ahmed (has objective, work experience, education details, etc.)
CV_AHMED = """devOps Engineer

Contact Details:
Name: Ahmed
Email: Ahmed7854775@gmail.com
Phone Number: + 91 -8904395414

Objective:
A challenging job that utilizes my skills with a reputable company where I can make a significant contribution and build my career with your domain.

Professional Experience:

Having 3.2+ years of experience in Build process, Software Product Development, Process Automation, Build & Release Management, Source Code repository & Environment management. Change/Incident Management and Cloud Management.

Responsible for administering and supporting source code management tool (GIT) on Linux.

Extensive experience using MAVEN as build tool for the building of deployable artifacts from source code.

Work Experience:
Working as DevOps Engineer at Amazon from Jan 2019 to Jan 2022

Education Details:
Bachelor of Technology in Osmania University 2019.

Technical Skills:
Version Control : Git
Build Tool : Maven
Continuous Integration : Jenkins
Operating System : Windows 7, LINUX(RHEL)
Static code analysis tool : SonarQube

Projects:

PROJECT#2:
Project Name: Air Liquide.
Client Name: Amazon
Role: DevOps Engineer

Responsibilities:

Jenkins continuous integration server installation and configuration for all GIT Repositories.
Developed and implemented Software Release Management strategies for various applications according to the Agile methodologies."""

# Resume 5: Amarnath
CV_AMARNATH = """Contact Information

AMARNATH
Bangalore, Karnataka, India. PIN - 560066
(+91)9515674318
amarnathgoal01@gmail.com

PROFILE SUMMARY

Having 3+ years of Experience in IT Industry with 1.1years SQL developer and 2+years as a DevOps and Microsoft azure engineer(cloud).
Extensive experience in Azure Cloud, Kubernetes, Docker, Git, GitLab, Azure DevOps with CI/CD, Deployment and Monitoring.

EMPLOYMENT

DevOps Engineer IBM Pvt. Ltd., Bangalore Dec2019 - Present

Involved in right from analysis to implementation of new ci/cd pipelines using GitLab and azure DevOps.
Resolved many live issues related branching strategy, SonarQube & Coverity setup and logging.

Technical Skills

Programming Languages – C# Basics and Python Basics
DevOps Tools– GitLab and Azure DevOps,
Cloud Tools – Azure and AWS(Basics)
Database – SQL Server

EDUCATION

Bachelor of Science in Computers (2014 – 2017) from Sri Venkateshwara University, Tirupati, Andhra Pradesh, India.

PERSONAL DETAILS

Date Of Birth: 18-06-1997
Marital Status: Un-Married
Nationality: Indian
Languages Known: English (Proficient), Telugu (Native)

ACHIEVEMENTS AND RESPONSIBILITIES

Conducted and provided knowledge sharing session on Branching Strategy.
Actively participated in Hackathon and other organizational events."""

# Resume 13: Ashika Nair
CV_ASHIKA = """ASHIKA NAIR
Automation Test Engineer
nairashikaofficial@gmail.com
+91 - 8921791769

Career Objective
An enthusiastic python developer with 4 years of total expertise working in Agile Projects.

Work Experiences
System Engineer at TCS
Nov 2017 - Jan 2022
Automation Test engineer in a Norway based project for RESTFUL Web API Functional testing.

Projects
DNB https://www.dnb.no/sparing/spare-app
Wealth Management- A project aiming at providing customers a feasible solution to manage their funds.

Skills
Python
Selenium
pytorch
ScikitLearn
Docker
Jenkins

Educations
College/school University/Board Degree/Standard Passing Date Percentage/Pointer
FISAT Mahatma Gandhi University B.Tech. 2017 8.2

Certificates Awards & Achievements
TCS internal level certifications on Python,Machine Learning,Java etc.
School level topper in CBSE 12th Grade.

Personal Information
Date Of Birth 23-11-1995
Nationality India
Languages Hindi,English,Malayalam"""

test_cases = [
    ("Ahmed - DevOps Engineer", CV_AHMED),
    ("Amarnath - Azure DevOps", CV_AMARNATH),
    ("Ashika Nair - Test Engineer", CV_ASHIKA),
]

print("=" * 100)
print("FINAL VALIDATION TEST - COMPLETE RESUMES")
print("=" * 100)

for i, (name, cv_text) in enumerate(test_cases, 1):
    print(f"\n{'='*100}")
    print(f"RESUME {i}: {name}")
    print(f"{'='*100}")

    raw_sections, sections = parse_cv_sections_improved(cv_text)

    # Count sections
    non_empty_sections = {k: v for k, v in sections.items() if v}

    print(f"\nDetected {len(non_empty_sections)} sections:")
    for section_name in sorted(non_empty_sections.keys()):
        print(f"  ✓ {section_name}")

    print(f"\nDetailed content:")
    for section_name, content in sorted(sections.items()):
        if content:  # Only show non-empty sections
            print(f"\n[{section_name.upper()}]")
            print(f"Lines: {len(content)}")
            for line in content[:3]:  # Show first 3 lines
                print(f"  - {line}")
            if len(content) > 3:
                print(f"  ... and {len(content) - 3} more lines")

    print()
