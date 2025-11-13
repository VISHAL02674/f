#!/usr/bin/env python3
"""
Comparison: Original CV Sections vs Detected Sections
Analyzes what sections are actually present vs what our code detected
"""

from sectionization import parse_cv_sections_improved

# CV texts with manual section identification
CVS_WITH_MANUAL_ANALYSIS = [
    {
        "name": "CV #1: Anand Kishore Lakhera",
        "text": """# Anand Kishore Lakhera
## Contact Information:
- **Email:** anandkishore.lakhera@gmail.com
- **Contact No:** +91-8770047544

## SUMMARY:
Over 3.4+ Years of experience in software development while creating and maintaining Applications.

## TECHNICAL SKILLS:

- **Programming Language:** Java ( Core )
- **Scripting Languages:** Bash shell scripting,

## PROFESSIONAL EXPERIENCE:

### **Application Developer - Core Java**
**IBM - Bank (Munich) | May-2016 to Nov-2016 | Team: Iko-II**

- **Responsibilities:**
  - Analyzed the business requirements.

### **DevOps Engineer / Build & Release Engineer**
**IBM India pvt ltd | Team: BWINT | Client: BMW-Bank (Munich) | Nov-2016 to Jan-2018**""",
        "expected_sections": {
            "introduction": ["name", "contact information"],
            "summary": ["SUMMARY section"],
            "skills": ["TECHNICAL SKILLS section"],
            "experience": ["PROFESSIONAL EXPERIENCE section with 2 roles"]
        }
    },
    {
        "name": "CV #2: Ananth Bhat",
        "text": """## Ananth Bhat
## Cloud DevOps Engineer

### Contact

* **Address**: Bengaluru, KA, 560076
* **Phone**: 974 109 6236

### Professional Summary

A result-oriented professional with 5 Years 3 Months of experience.

### Skills

* **DevOps, Cloud-based environments**: Very Good

### Work History

#### Cloud DevOps Engineer
* **Company**: Cisco Systems India Pvt Ltd

### Education

* **Bachelor of Engineering: Electronics And Communications Engineering**

### Accomplishments

* **AWARDS**:
  * Won "Spot award" """,
        "expected_sections": {
            "introduction": ["name", "title", "Contact"],
            "summary": ["Professional Summary"],
            "skills": ["Skills section"],
            "experience": ["Work History"],
            "education": ["Education"],
            "achievements": ["Accomplishments/AWARDS"]
        }
    },
    {
        "name": "CV #3: Aniket Pachpute",
        "text": """Aniket Pachpute
Lead Engineer at Nokia
+91-8668429937  aniketpachpute27@gmail.com

IT Professional with 3 years of experience.

## PROFESSIONAL EXPERIENCE

### Nokia
#### Software Engineer | Mar'19 – Present

## Project Description:

### 1) JUPYTER (March'19-July 21) :
The Jupyter Notebook is an open-source web application.

* **Roles And Responsibilities :**
  > Development of new features

* **Tools,Technologies and Web Servers :**
  > Docker
  > Kubernetes

## Agile Tools :Jira

## Extra Curricular Activities:
* Working as a member of Fun@Work team.

## Interests:
* Travelling, Bike Riding

## Educational Details :

| Sr No | College | Degree/Diploma |
| --- | --- | --- |
| 1. | CDAC ACTS | PG Diploma |""",
        "expected_sections": {
            "introduction": ["name", "title", "contact", "summary"],
            "experience": ["PROFESSIONAL EXPERIENCE"],
            "projects": ["Project Description with JUPYTER"],
            "skills": ["Tools,Technologies and Web Servers - NOT DETECTED!"],
            "activities": ["Agile Tools, Extra Curricular Activities"],
            "interests": ["Interests"],
            "education": ["Educational Details"]
        }
    },
    {
        "name": "CV #5: Arjun Suri",
        "text": """ARJUN SURI
Bangalore, India
+91- 9463594061

EMPLOYMENT

Support Engineer – 1
Amazon India Development Centre  Sept 2020-Present

Cyber Risk Analyst
Deloitte USI  June 2019-August 2020

EDUCATION

Punjab, India  Chandigarh Group Of Colleges  2015-2019
* B. Tech in Computer Science

PERSONAL PROJECTS

Donors Society  HTML, CSS, JAVASCRIPT

ADDITIONAL EXPERIENCE AND AWARDS

* Among top 5000 coders in India

LANGUAGES, TOOLS AND TECHNOLOGIES

* HTML,CSS, Javascript, React, Java""",
        "expected_sections": {
            "introduction": ["name", "contact"],
            "experience": ["EMPLOYMENT"],
            "education": ["EDUCATION"],
            "projects": ["PERSONAL PROJECTS"],
            "achievements": ["ADDITIONAL EXPERIENCE AND AWARDS"],
            "skills": ["LANGUAGES, TOOLS AND TECHNOLOGIES - NOT DETECTED!"]
        }
    },
    {
        "name": "CV #7: Ashu Chandra",
        "text": """## Ashu Chandra

### Contact Details
- Email: ashuchandraashu@gmail.com

## EXPERIENCE: 4 years and 2 months

### IBM, Pune — Senior System Engineer
July 2021 - PRESENT

#### Airport Operations Technology (AOT)
Client: Delta Airline

### Atos Syntel, Pune — Associate Consultant
March 2018- July 2021

## SKILLS
- Java 8
- Spring Boot

## AWARDS
- Got Kudos Award from Atos Syntel

## TRAININGS
- Got training in Spring, Spring Boot

## LANGUAGES
- Hindi
- English

## EDUCATION
### Bachelor of technology (B.Tech) in Computer Science - 2017""",
        "expected_sections": {
            "introduction": ["name", "Contact Details"],
            "experience": ["EXPERIENCE: 4 years... - NOT DETECTED AS HEADER!"],
            "skills": ["SKILLS"],
            "achievements": ["AWARDS"],
            "courses": ["TRAININGS"],
            "interests": ["LANGUAGES - might be detected as languages"],
            "education": ["EDUCATION"]
        }
    }
]


def analyze_section_in_text(text, section_name):
    """Check if a section header appears in the text"""
    text_upper = text.upper()

    # Common section patterns
    patterns = {
        "summary": ["SUMMARY", "PROFESSIONAL SUMMARY", "CAREER SUMMARY"],
        "experience": ["EXPERIENCE", "PROFESSIONAL EXPERIENCE", "WORK HISTORY", "EMPLOYMENT"],
        "skills": ["SKILLS", "TECHNICAL SKILLS", "TOOLS", "TECHNOLOGIES"],
        "education": ["EDUCATION", "EDUCATIONAL", "ACADEMIC"],
        "projects": ["PROJECTS", "PROJECT"],
        "achievements": ["ACHIEVEMENTS", "ACCOMPLISHMENTS", "AWARDS"],
        "interests": ["INTERESTS", "HOBBIES"],
        "activities": ["ACTIVITIES", "EXTRA CURRICULAR"],
        "courses": ["TRAININGS", "TRAINING", "COURSES"]
    }

    if section_name in patterns:
        for keyword in patterns[section_name]:
            if keyword in text_upper:
                return True, keyword

    return False, None


def compare_cv_sections():
    """Compare expected vs detected sections for each CV"""

    print("\n" + "="*80)
    print("COMPARISON: ORIGINAL CVs vs DETECTED SECTIONS")
    print("="*80)

    total_expected = 0
    total_detected = 0
    total_matched = 0
    total_missed = 0

    for cv_data in CVS_WITH_MANUAL_ANALYSIS:
        print("\n" + "-"*80)
        print(f"📄 {cv_data['name']}")
        print("-"*80)

        # Get detected sections
        raw_sections, final_sections = parse_cv_sections_improved(cv_data['text'])

        # Count expected sections
        expected = cv_data['expected_sections']
        detected = list(final_sections.keys())

        print(f"\n📋 EXPECTED SECTIONS (from manual analysis):")
        for section, description in expected.items():
            present, keyword = analyze_section_in_text(cv_data['text'], section)
            status = "✅ Found in text" if present else "ℹ️  Inferred"
            if present:
                print(f"   • {section}: {description[0]} [{keyword}] {status}")
            else:
                print(f"   • {section}: {description[0]} {status}")

        print(f"\n🤖 DETECTED SECTIONS (by our code):")
        for section in detected:
            print(f"   • {section}: {len(final_sections[section])} lines")

        # Find matches and misses
        matched = set(expected.keys()) & set(detected)
        missed = set(expected.keys()) - set(detected)
        extra = set(detected) - set(expected.keys())

        print(f"\n📊 COMPARISON:")
        print(f"   ✅ Matched: {len(matched)}/{len(expected)} sections")
        if matched:
            print(f"      {', '.join(matched)}")

        if missed:
            print(f"   ❌ Missed: {len(missed)} sections")
            for section in missed:
                present, keyword = analyze_section_in_text(cv_data['text'], section)
                if present:
                    print(f"      • {section} (present as '{keyword}' in original)")
                else:
                    print(f"      • {section}")

        if extra:
            print(f"   ➕ Extra: {len(extra)} sections (detected but not explicitly expected)")
            print(f"      {', '.join(extra)}")

        # Update totals
        total_expected += len(expected)
        total_detected += len(detected)
        total_matched += len(matched)
        total_missed += len(missed)

        # Accuracy for this CV
        accuracy = (len(matched) / len(expected) * 100) if expected else 0
        print(f"\n   🎯 Accuracy: {accuracy:.1f}%")

    # Overall summary
    print("\n" + "="*80)
    print("📊 OVERALL COMPARISON SUMMARY")
    print("="*80)

    print(f"\nTotals across all CVs:")
    print(f"   Expected sections: {total_expected}")
    print(f"   Detected sections: {total_detected}")
    print(f"   Matched correctly: {total_matched}")
    print(f"   Missed sections: {total_missed}")

    overall_accuracy = (total_matched / total_expected * 100) if total_expected else 0
    print(f"\n🎯 Overall Detection Accuracy: {overall_accuracy:.1f}%")

    # Common issues
    print(f"\n❌ COMMON MISSED PATTERNS:")
    print(f"   1. 'Tools,Technologies and Web Servers' → Should be 'skills'")
    print(f"   2. 'LANGUAGES, TOOLS AND TECHNOLOGIES' → Should be 'skills'")
    print(f"   3. 'EXPERIENCE: 4 years and 2 months' → Should be 'experience' header")
    print(f"   4. 'PROFESSIONAL EXPERIENCE:' → Should be 'experience'")

    print(f"\n✅ WHAT WORKS WELL:")
    print(f"   • Standard headers: SKILLS, EDUCATION, EXPERIENCE")
    print(f"   • Markdown headers: ## Section Name")
    print(f"   • Title case: Professional Summary, Work History")
    print(f"   • Introduction/contact always detected")

    if overall_accuracy >= 90:
        print(f"\n🎉 Status: EXCELLENT - Production ready!")
    elif overall_accuracy >= 75:
        print(f"\n✅ Status: GOOD - Minor improvements recommended")
    else:
        print(f"\n⚠️  Status: NEEDS IMPROVEMENT")

    print("\n" + "="*80)


if __name__ == "__main__":
    compare_cv_sections()
