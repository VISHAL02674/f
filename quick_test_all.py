"""Quick test to see what sections are missing in all 15 resumes"""
from sectionization import determine_section_name

# Collect all unique headers from the 15 resumes
all_headers = [
    # Resume 1: Anil Kumar Annem
    "CAREER SUMMARY",
    "CERTIFICATION & EDUCATION",
    "JOB HISTORY",
    "TECHNICAL SKILLS",
    "PROJECT SUMMARY",

    # Resume 2: Abhay Kumar
    "PROFESSIONAL SUMMARY",
    "TECH STACK",
    "EXPERIENCE",

    # Resume 3: Adarsh Patnaik
    "Area of Expertise:",
    "Roles & Responsibilities:",
    "System Engineer at TCS",
    "Certifications:",
    "Professional Snapshot",
    "Organisational Experience",
    "Educational Qualifications",
    "Skill Sets",

    # Resume 4: Ahmed
    "Contact Details:",
    "Objective:",
    "Professional Experience:",
    "Work Experience:",
    "Education Details:",
    "Technical Skills:",
    "Projects:",
    "Responsibilities:",

    # Resume 5: Amarnath
    "PROFILE SUMMARY",
    "EMPLOYMENT",
    "Technical Skills",
    "EDUCATION",
    "PERSONAL DETAILS",
    "ACHIEVEMENTS AND RESPONSIBILITIES",

    # Resume 6: Anamika Singh
    "SUMMARY:",
    "JOB PROFILE:",
    "WORK EXPERIENCE:",
    "QUALIFICATION:",
    "SKILL SET:",

    # Resume 7: Anand Kishore Lakhera
    "SUMMARY:",
    "TECHNICAL SKILLS:",
    "PROFESSIONAL EXPERIENCE:",

    # Resume 8: Anand Shanmugam
    "Summary",
    "Skills",
    "Certifications",
    "Experience",

    # Resume 9: Ananth Bhat
    "Professional Summary",
    "Skills",
    "Work History",

    # Resume 10: Aniket Pachpute
    "PROFESSIONAL EXPERIENCE",
    "Roles And Responsibilities :",
    "Tools,Technologies and Web Servers :",
    "Agile Tools :",
    "Extra Curricular Activities:",
    "Interests:",
    "Educational Details :",

    # Resume 11: Anindya Sudhir
    "Professional Summary",
    "Work History",
    "Education",
    "Skills",
    "Certifications",

    # Resume 12: Arjun Suri
    "EMPLOYMENT",
    "EDUCATION",
    "PERSONAL PROJECTS",
    "ADDITIONAL EXPERIENCE AND AWARDS",
    "LANGUAGES, TOOLS AND TECHNOLOGIES",

    # Resume 13: Ashika Nair
    "Career Objective",
    "Work Experiences",
    "Projects",
    "Skills",
    "Educations",
    "Certificates Awards & Achievements",
    "Personal Information",

    # Resume 14: Ashok Raja
    "EXPERIENCE",
    "SKILLS",
    "EDUCATION",

    # Resume 15: Ashu Chandra
    "Contact Details",
    "EXPERIENCE:",
    "SKILLS",
    "AWARDS",
    "TRAININGS",
    "LANGUAGES",
    "EDUCATION",
]

print("Analyzing all headers from 15 resumes...\n")

unmapped = []
mapped = {}

for header in all_headers:
    section = determine_section_name(header)
    if section is None:
        unmapped.append(header)
    else:
        if section not in mapped:
            mapped[section] = []
        mapped[section].append(header)

print(f"{'='*100}")
print(f"UNMAPPED HEADERS (need to add): {len(unmapped)}")
print(f"{'='*100}")
for h in unmapped:
    print(f"  ❌ {h}")

print(f"\n{'='*100}")
print(f"SUCCESSFULLY MAPPED HEADERS: {len(all_headers) - len(unmapped)}/{len(all_headers)}")
print(f"{'='*100}")
for section, headers in sorted(mapped.items()):
    print(f"\n[{section.upper()}]:")
    for h in headers:
        print(f"  ✓ {h}")
