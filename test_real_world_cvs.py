#!/usr/bin/env python3
"""
Extended test suite for real-world CV formats
Tests sectionization on 9 diverse resume formats to validate pipeline readiness
"""

from sectionization import parse_cv_sections_improved, extract_entities_improved
import json

# CV 1: Anand Kishore Lakhera
CV_1_ANAND = """# Anand Kishore Lakhera
## Contact Information:
- **Email:** anandkishore.lakhera@gmail.com
- **Contact No:** +91-8770047544

## SUMMARY:
Over 3.4+ Years of experience in software development while creating and maintaining Applications, Automated building, Automated testing, Automated deployments, and Automated source control integration environments.
Participated within an Agile/Scrum team, extensive hands-on experience with quality assurance methods.

Expertise in setting up project-specific environments on Linux/Unix and Windows platforms that involves CM branching, merging, labelling, Baseline, and development work areas.

Comprehensive experience in the design and implementation of Continuous Integration, Continuous Deployment, Continuous Delivery, and DevOps Operations for Agile projects, working with technologies and platforms including UNIX/Linux, Java, Swift, Git, Ant, Maven, Sonar, Nexus, Jenkins, Openshift, Flyway, Ansible, Kubernetes, Docker, Apache 2.4, Banking, and Service Sector.

## TECHNICAL SKILLS:

- **Programming Language:** Java ( Core )
- **Scripting Languages:** Bash shell scripting,
- **Application Server:** Glassfish3 and glassfish 4 (payara), webLogic12.
- **CI Tools:** Jenkins, Ansible.
- **Build Tools:** Maven, Ant, Gradle, Flyway
- **Version Control Tool:** Confluence.
- **Operating Systems:** Linux, Unix, Windows.

## PROFESSIONAL EXPERIENCE:

### **Application Developer - Core Java**
**IBM - Bank (Munich) | May-2016 to Nov-2016 | Team: Iko-II**

- **Responsibilities:**
  - Analyzed the business requirements.
  - Added functionality in the application to fetch the data from the database and generate xls/xslt files.

### **DevOps Engineer / Build & Release Engineer**
**IBM India pvt ltd | Team: BWINT | Client: BMW-Bank (Munich) | Nov-2016 to Jan-2018**

- **Responsibilities:**
  - Responsible for day-to-day management of all Development, Test, Stage, and Production environments.
  - Created branches and managed the source code for various applications in GIT."""

# CV 2: Ananth Bhat (already tested, keeping for comparison)
CV_2_ANANTH = """## Ananth Bhat
## Cloud DevOps Engineer

### Contact

* **Address**: Bengaluru, KA, 560076
* **Phone**: 974 109 6236
* **E-mail**: ananthsbhat0806@gmail.com

### Professional Summary

A result-oriented professional with 5 Years 3 Months of experience in the field of automation and cloud DevOps.

### Skills

* **DevOps, Cloud-based environments**: Very Good
* **Terraform, Version Control tool (Git)**: Very Good

### Work History

#### Cloud DevOps Engineer
* **Company**: Cisco Systems India Pvt Ltd, Bangalore, Karnataka

### Education

* **Bachelor of Engineering: Electronics And Communications Engineering**"""

# CV 3: Aniket Pachpute
CV_3_ANIKET = """Aniket Pachpute
Lead Engineer at Nokia
+91-8668429937  aniketpachpute27@gmail.com

IT Professional with 3 years of experience in customizing the open source components and deployment.

## PROFESSIONAL EXPERIENCE

### Nokia
#### Software Engineer | Mar'19 – Present

## Project Description:

### 1) JUPYTER (March'19-July 21) :
The Jupyter Notebook is an open-source web application that allows you to create and share documents.

* **Roles And Responsibilities :**
  > Development of new features into existing open source application
  > Customization of existing features as per the requirement

* **Tools,Technologies and Web Servers :**
  > Docker
  > Kubernetes
  > Python

## Agile Tools :Jira

## Extra Curricular Activities:
* Working as a member of Fun@Work team.

## Interests:
* Travelling, Bike Riding, Watching News

## Educational Details :

| Sr No | College | Degree/Diploma | Percentage/CGPA | Year of Passing |
| --- | --- | --- | --- | --- |
| 1. | CDAC ACTS Headquarters Pune | PG Diploma in Advanced Computing | 78.6% | 2019 |"""

# CV 4: Anindya Sudhir
CV_4_ANINDYA = """## Anindya Sudhir
### Machine Learning Developer/Software Developer/Data Scientist

## Contact
- Address: Pune, MH, 411057
- Phone: 703 041 9955
- E-mail: anindyasudhir@gmail.com

## Professional Summary
Machine Learning Developer/Data Scientist/Software Developer having 7 years of experience in IT industry.

## Work History

### Machine Learning Developer
IBM, Pune, MH
2019-04 - Current
- Built Fine Tuned BERT models using Huggingface and SimpleTransformers libraries.

### Software Developer
IBM, Pune, MH
2017-04 - 2019-03
- Developed robust Java code for IBM asset management applications.

## Education

### Master of Science: Machine Learning & AI
Liverpool John Moores University - Liverpool , England
2020-04 - Current

### Bachelor of Engineering: Information Technology
Birla Institute of Technology, Mesra - Ranchi
2009-04 - 2013-04

## Skills
- Machine learning: Excellent
- Python: Excellent
- Java: Excellent

## Certifications
- 2019-08: Machine Learning, by Stanford University"""

# CV 5: Arjun Suri
CV_5_ARJUN = """ARJUN SURI
Bangalore, India
+91- 9463594061
arjun.suri.7@gmail.com

EMPLOYMENT

Support Engineer – 1
Amazon India Development Centre  Sept 2020-Present
* Developed, scaled and maintained Amazon Easyship returns services

Cyber Risk Analyst
Deloitte USI  June 2019-August 2020
* Worked on Customer Identity and Access Management tool (Forgerock)

EDUCATION

Punjab, India  Chandigarh Group Of Colleges  2015-2019
* B. Tech in Computer Science and Engineering  CGPA-8.8/10

PERSONAL PROJECTS

Donors Society  HTML, CSS, JAVASCRIPT,PHP,MYSQL  Jan-March, 2016
* A blood donation website

ADDITIONAL EXPERIENCE AND AWARDS

* Among top 5000 coders in India on HackerRank

LANGUAGES, TOOLS AND TECHNOLOGIES

* HTML,CSS, Javascript, React, Java, Spring, Spring Boot"""

# CV 6: Ashika Nair
CV_6_ASHIKA = """# ASHIKA NAIR
Automation Test Engineer
nairashikaofficial@gmail.com
+91 - 8921791769

## Career Objective
An enthusiastic python developer with 4 years of total expertise working in Agile Projects.

## Work Experiences
### System Engineer at TCS
Nov 2017 - Jan 2022
* Automation Test engineer in a Norway based project

### Automation Test Engineer at IBM ISL(Product wing)
Jan 2022 - Present
* Handling system level testing for ARM Tool-Turbonomic

## Projects
### DNB | https://www.dnb.no/sparing/spare-app
* Wealth Management- A project aiming at providing customers a feasible solution

## BFSI Sustainable Banking solutions
* Viridi-It is a sustainable banking solution

## Skills
* Python
* Selenium
* pytorch

## Educations
| College/school | University/Board | Degree/Standard | Passing Date | Percentage/Pointer |
| FISAT | Mahatma Gandhi University | B.Tech. | 2017 | 8.2 |

## Certificates Awards & Achievements
* TCS internal level certifications on Python,Machine Learning,Java etc."""

# CV 7: Ashu Chandra
CV_7_ASHU = """## Ashu Chandra
Experience without being explicitly programmed.

### Contact Details
- Email: ashuchandraashu@gmail.com
- Phone: +91 7988349995

## EXPERIENCE: 4 years and 2 months

### IBM, Pune — Senior System Engineer
July 2021 - PRESENT

#### Airport Operations Technology (AOT)
Client: Delta Airline
Role: Java Developer

##### Project Description:
Container Sheets Production

##### My Role and Contribution:
- Gather all the requirements from business

### Atos Syntel, Pune — Associate Consultant
March 2018- July 2021

#### Linehaul Modernization (Atos Syntel)
Client: Fedex Ground

## SKILLS
- Java 8
- Spring Boot
- Micro services

## AWARDS
- Got Kudos Award from Atos Syntel

## TRAININGS
- Got training in Spring, Spring Boot and Microservices from Udemy

## LANGUAGES
- Hindi
- English

## EDUCATION
### Bachelor of technology (B.Tech) in Computer Science - 2017
Maharishi Markandeshwar University"""

# CV 8: Ashwini Thombre (already tested)
CV_8_ASHWINI = """# Ashwini Thombre
+91 7892591830| ashwini.thombre7392@gmail.com

## Professional Summary
- 5.10 years of experience in IT industry

## Technical Expertise

| Cloud Environments & Services | AWS |
| Configuration management tool | Ansible |

## Work History

### Service Delivery Specialist: AWS-DevOps
Kyndryl Solutions Private Limited-(IBM)
May 2018 to Till Date

## Education

2014 BE from Sagar institute"""

# CV 9: Ahmed
CV_9_AHMED = """# devOps Engineer

## Contact Details:
- **Name:** Ahmed
- **Email:** Ahmed7854775@gmail.com
- **Phone Number:** + 91 -8904395414

## Objective:
A challenging job that utilizes my skills with a reputable company.

## Professional Experience:

- Having 3.2+ years of experience in Build process, Software Product Development.

## Work Experience:
- Working as DevOps Engineer at Amazon from Jan 2019 to Jan 2022

## Education Details:
- Bachelor of Technology in Osmania University 2019.

## Technical Skills:
- **Version Control** : Git
- **Build Tool** : Maven

## Projects:

### PROJECT#2:
- **Project Name:** Air Liquide.
- **Client Name:** Amazon

### PROJECT#1:
- **Project Name:** UK Card Technology Operations

## Responsibilities:

- Jenkins continuous integration server installation
- Developed and implemented Software Release Management"""


def analyze_section_detection(cv_name, sections):
    """Analyze section detection quality"""
    issues = []
    warnings = []

    # Check for missing common sections
    common_sections = ['experience', 'education', 'skills']
    for section in common_sections:
        if section not in sections:
            warnings.append(f"⚠️  Missing common section: {section}")

    # Check for oversized introduction
    if 'introduction' in sections and len(sections['introduction']) > 15:
        warnings.append(f"⚠️  Large introduction section ({len(sections['introduction'])} lines)")

    # Check if we have reasonable number of sections
    if len(sections) < 3:
        issues.append(f"❌ Too few sections detected: {len(sections)}")
    elif len(sections) > 12:
        warnings.append(f"⚠️  Many sections detected: {len(sections)}")

    return issues, warnings


def print_detailed_results(cv_name, sections, show_content=False):
    """Print detailed section analysis"""
    print("\n" + "="*80)
    print(f"📄 {cv_name}")
    print("="*80)

    # Analyze
    issues, warnings = analyze_section_detection(cv_name, sections)

    # Print summary
    print(f"\n📊 Summary:")
    print(f"   Sections found: {len(sections)}")
    print(f"   Section names: {', '.join(sections.keys())}")
    print(f"   Total lines: {sum(len(content) for content in sections.values())}")

    # Print quality indicators
    if not issues and not warnings:
        print(f"   Quality: ✅ EXCELLENT")
    elif not issues:
        print(f"   Quality: ⚠️  GOOD (with warnings)")
    else:
        print(f"   Quality: ❌ NEEDS IMPROVEMENT")

    # Print issues and warnings
    if issues:
        print(f"\n❌ Issues:")
        for issue in issues:
            print(f"   {issue}")

    if warnings:
        print(f"\n⚠️  Warnings:")
        for warning in warnings:
            print(f"   {warning}")

    # Print section details
    print(f"\n📋 Section Details:")
    for section_name, content in sections.items():
        print(f"   • {section_name}: {len(content)} lines")
        if show_content:
            for i, line in enumerate(content[:3], 1):
                preview = line[:80] + "..." if len(line) > 80 else line
                print(f"      {i}. {preview}")
            if len(content) > 3:
                print(f"      ... and {len(content) - 3} more lines")


def run_comprehensive_tests():
    """Run tests on all 9 CV samples"""

    test_cases = [
        ("CV #1: Anand Kishore Lakhera (DevOps Engineer)", CV_1_ANAND),
        ("CV #2: Ananth Bhat (Cloud DevOps Engineer)", CV_2_ANANTH),
        ("CV #3: Aniket Pachpute (Lead Engineer)", CV_3_ANIKET),
        ("CV #4: Anindya Sudhir (ML Developer)", CV_4_ANINDYA),
        ("CV #5: Arjun Suri (Support Engineer)", CV_5_ARJUN),
        ("CV #6: Ashika Nair (Automation Test Engineer)", CV_6_ASHIKA),
        ("CV #7: Ashu Chandra (Senior System Engineer)", CV_7_ASHU),
        ("CV #8: Ashwini Thombre (AWS-DevOps)", CV_8_ASHWINI),
        ("CV #9: Ahmed (DevOps Engineer)", CV_9_AHMED),
    ]

    print("\n" + "🚀 COMPREHENSIVE REAL-WORLD CV TESTING")
    print("="*80)
    print(f"Testing {len(test_cases)} diverse CV formats for pipeline readiness\n")

    results_summary = []

    for cv_name, cv_text in test_cases:
        try:
            # Extract sections
            raw_sections, final_sections = parse_cv_sections_improved(cv_text)

            # Analyze
            issues, warnings = analyze_section_detection(cv_name, final_sections)

            # Store results
            results_summary.append({
                'name': cv_name,
                'sections_count': len(final_sections),
                'total_lines': sum(len(content) for content in final_sections.values()),
                'sections': list(final_sections.keys()),
                'issues': len(issues),
                'warnings': len(warnings),
                'quality': 'EXCELLENT' if not issues and not warnings else 'GOOD' if not issues else 'POOR'
            })

            # Print detailed results
            print_detailed_results(cv_name, final_sections, show_content=False)

        except Exception as e:
            print(f"\n❌ ERROR processing {cv_name}:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()

            results_summary.append({
                'name': cv_name,
                'error': str(e),
                'quality': 'ERROR'
            })

    # Print overall summary
    print("\n" + "="*80)
    print("📊 OVERALL PIPELINE READINESS SUMMARY")
    print("="*80)

    total_cvs = len(results_summary)
    excellent = sum(1 for r in results_summary if r.get('quality') == 'EXCELLENT')
    good = sum(1 for r in results_summary if r.get('quality') == 'GOOD')
    poor = sum(1 for r in results_summary if r.get('quality') == 'POOR')
    errors = sum(1 for r in results_summary if r.get('quality') == 'ERROR')

    print(f"\nResults:")
    print(f"   ✅ Excellent: {excellent}/{total_cvs} ({excellent/total_cvs*100:.1f}%)")
    print(f"   ⚠️  Good: {good}/{total_cvs} ({good/total_cvs*100:.1f}%)")
    print(f"   ❌ Poor: {poor}/{total_cvs} ({poor/total_cvs*100:.1f}%)")
    print(f"   🔥 Errors: {errors}/{total_cvs} ({errors/total_cvs*100:.1f}%)")

    # Section detection statistics
    print(f"\nSection Detection Statistics:")
    all_sections = {}
    for r in results_summary:
        if 'sections' in r:
            for section in r['sections']:
                all_sections[section] = all_sections.get(section, 0) + 1

    print(f"   Sections found across all CVs:")
    for section, count in sorted(all_sections.items(), key=lambda x: x[1], reverse=True):
        print(f"      • {section}: {count}/{total_cvs} CVs ({count/total_cvs*100:.0f}%)")

    # Average sections per CV
    avg_sections = sum(r.get('sections_count', 0) for r in results_summary) / total_cvs
    print(f"\n   Average sections per CV: {avg_sections:.1f}")

    # Common issues
    print(f"\nCommon Patterns:")
    total_issues = sum(r.get('issues', 0) for r in results_summary)
    total_warnings = sum(r.get('warnings', 0) for r in results_summary)
    print(f"   • Total issues: {total_issues}")
    print(f"   • Total warnings: {total_warnings}")

    # Pipeline readiness score
    success_rate = ((excellent + good) / total_cvs) * 100
    print(f"\n🎯 Pipeline Readiness Score: {success_rate:.1f}%")

    if success_rate >= 90:
        print(f"   Status: ✅ READY FOR PRODUCTION")
    elif success_rate >= 75:
        print(f"   Status: ⚠️  READY WITH MINOR IMPROVEMENTS")
    else:
        print(f"   Status: ❌ NEEDS IMPROVEMENTS")

    print("\n" + "="*80)


if __name__ == "__main__":
    run_comprehensive_tests()
