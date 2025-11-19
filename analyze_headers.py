"""
Analyze what headers exist in resumes vs what gets detected
"""
import re
from sectionization import parse_cv_sections_improved, is_section_header_improved, determine_section_name

def find_potential_headers(text):
    """Find lines that look like headers in the text"""
    lines = text.split('\n')
    potential_headers = []

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # Check various header patterns
        is_all_caps = line_stripped.isupper() and len(line_stripped.split()) <= 8
        ends_with_colon = line_stripped.endswith(':')
        short_line = len(line_stripped.split()) <= 4
        has_header_keywords = any(kw in line_stripped.upper() for kw in [
            'SUMMARY', 'EXPERIENCE', 'SKILLS', 'EDUCATION', 'WORK', 'JOB',
            'PROJECT', 'CERTIF', 'PROFILE', 'OBJECTIVE', 'CONTACT', 'HISTORY',
            'RESPONSIBILITIES', 'TECH', 'STACK', 'TOOLS', 'EXPERTISE', 'PROFESSIONAL',
            'CAREER', 'QUALIFICATIONS', 'LANGUAGES', 'AWARDS', 'ACHIEVEMENTS'
        ])

        if (is_all_caps or (ends_with_colon and short_line) or
            (has_header_keywords and short_line)):

            # Check if our code detects it
            detected = is_section_header_improved(line, lines, i)
            mapped_to = determine_section_name(line) if detected else None

            potential_headers.append({
                'line': line_stripped,
                'detected': detected,
                'mapped_to': mapped_to
            })

    return potential_headers

# Test Resume 1: Anil Kumar
CV_1 = """Anil Kumar Annem
Email: anilkumarscjp@gmail.com
Ph: +91-7349450050

CAREER SUMMARY

13+ years of software engineering experience

CERTIFICATION & EDUCATION

Certified Kubernetes Application Developer (CKAD®) - 2020

JOB HISTORY

Goldman Sachs from Jan 2021 to till date.

TECHNICAL SKILLS

Operating System: Windows, Linux

PROJECT SUMMARY

Project #1"""

# Test Resume 3: Adarsh Patnaik
CV_3 = """Adarsh Patnaik
DevOps Engineer

Area of Expertise:
Roles & Responsibilities:

System Engineer at TCS
Mar 2018 – Sept 2021

Certifications:
Azure Associate Administrator by Microsoft

Professional Snapshot
Organisational Experience
Educational Qualifications

Skill Sets
SCM Tools GIT, GITHUB"""

# Test Resume 4: Ahmed
CV_4 = """devOps Engineer

Contact Details:
Name: Ahmed

Objective:
A challenging job

Professional Experience:

Having 3.2+ years of experience

Work Experience:
Working as DevOps Engineer

Education Details:
Bachelor of Technology

Technical Skills:
Version Control : Git

Projects:

PROJECT#2:
Project Name: Air Liquide.

Responsibilities:

Jenkins continuous integration server"""

test_cvs = [
    ("Anil Kumar - Resume 1", CV_1),
    ("Adarsh Patnaik - Resume 3", CV_3),
    ("Ahmed - Resume 4", CV_4),
]

for name, cv in test_cvs:
    print(f"\n{'='*100}")
    print(f"{name}")
    print(f"{'='*100}")

    headers = find_potential_headers(cv)

    detected_count = sum(1 for h in headers if h['detected'])
    total_count = len(headers)

    print(f"\nDetection Rate: {detected_count}/{total_count} headers detected\n")

    print("MISSING HEADERS (not detected):")
    for h in headers:
        if not h['detected']:
            print(f"  ❌ {h['line']}")

    print("\nDETECTED HEADERS:")
    for h in headers:
        if h['detected']:
            print(f"  ✓ {h['line']} → {h['mapped_to']}")
