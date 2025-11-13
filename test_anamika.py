#!/usr/bin/env python3
"""
Test the Anamika Singh CV to see section detection
"""

from sectionization import parse_cv_sections_improved

CV_ANAMIKA = """# ANAMIKA SINGH
+91-8874650189 || anamikasingh7789.as@gmail.com || https://www.linkedin.com/in/anamika-singh-556aa114b/

## SUMMARY:
Versed Automation Engineer with experience in DevOps or CI/CD.

## JOB PROFILE:

## WORK EXPERIENCE:
- Working at Wipro Technologies, Bangalore from June 2019 to till date.
- A creative & innovative professional with more than 2 years of working experience.

## QUALIFICATION:
- B. TECH in Computer Science and Engineering, GLA University, Mathura in 2019.

## SKILL SET:
- Database : SQL
- Scripting Languages : Python Shell scripting

## Project Title: EO-Staging Automation:

### Organization
Wipro Technologies, Bangalore, India.

## Project Synopsis:
Develop and maintain the automated deployment.

## Roles and Responsibilities:
- Develop test strategies.
- Automated tests using behave and pytest frameworks."""

# Test current detection
raw_sections, final_sections = parse_cv_sections_improved(CV_ANAMIKA)

print("DETECTED SECTIONS:")
print("="*80)
for section_name, content in final_sections.items():
    print(f"\n[{section_name.upper()}]")
    print(f"Lines: {len(content)}")
    for line in content[:5]:
        print(f"  - {line[:100]}")
    if len(content) > 5:
        print(f"  ... and {len(content)-5} more lines")
