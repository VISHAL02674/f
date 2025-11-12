# > imports
import re
from datetime import datetime

# > DICTIONARIES AND CONFIGURATION
# > main section keywords dictionary -> covers most resume sections
KEYWORDS_DICT = {
    "projects": ["project name", "project title", "projects", "personal projects", "key projects"],
    "introduction": ["introduction", "contact", "details", "personal", "basic information", "personal information"],
    "courses": ["courses", "coursework", "related coursework", "workshops", "training", "professional development", "certified courses"],
    "skills": ["skills", "competencies", "expertise", "strength", "technical skills", "core competencies", "skill set", "technologies"],
    "summary": ["summary", "overview", "profile", "profile summary", "professional summary", "career summary"],
    "achievements": ["accomplishments", "achievements", "awards", "honors", "recognition", "accolades"],
    "affiliations": ["affiliations", "memberships", "associations", "professional memberships"],
    "objective": ["objectives", "career objective", "professional objective", "goal"],
    "interests": ["interests", "hobbies", "personal interests", "activities"],
    "certifications": ["certify", "license", "qualify", "chartered", "register", "accredit", "diploma", "fellow", "certifications", "certificates", "professional certifications", "certified courses"],
    "references": ["references", "recommendations", "testimonials", "endorsements"],
    "publications": ["publications", "conferences", "journals", "meets", "summits", "seminars", "talks", "presentations", "patents", "research papers"],
    "activities": ["activities", "participations", "involvement", "service", "volunteer", "engagement", "extracurricular", "community service"],
    "D.O.B": ["date of birth", "dob", "d.o.b", "birth date"],
    "gender": ["gender", "sex"],
    "experience": ["professional experience", "work experience", "employment history", "career history", "experience", "work history", "employment", "appointments", "previous positions", "business exposure", "current profile", "job profile", "professional background"]
}

# > resume sections with regex patterns for flexible matching
RESUME_SECTIONS_DICT = {
    "experience": [
        r"work[\s]{1,}experience[s]?",
        r".*workexperience.*",
        r"professional[\s]{0,}experience[s]?",
        r"organisational contour",
        r"employment scan",
        r"employment background",
        r"career[\s]{0,}history",
        r"employment[\s]{0,}history",
        r"experience[s]?",
        r"work[\s]{0,}history",
        r"appointments",
        r"previous[\s]{0,}positions",
        r"business[\s]{0,}exposure",
        r"current[\s]{0,}profile",
        r"job[\s]{0,}profile",
        "experience",
        "professional experience",
        "work experience",
        "employment history",
        "career background",
        "professional background"
    ],
    "education": [
        r"education(al)?",
        r"academic[\s]{0,}background",
        r"academic[\s]{0,}history",
        r"qualifications",
        r"academic[s]?",
        r"education(al)?[\s]{0,}qualification[s]?",
        r"scholastic[\s]{0,}achievements",
        "highest education",
        "professional qualification",
        "education history",
        "scholastics",
        "scholastic",
        "academia",
        "ducation",
        "cgpa",
        "b.tech",
        "cation",
        "academic record",
        r"academic[\s]{0,}record",
        "educational background",
        "academic qualifications",
        "degrees"
    ],
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "competencies",
        "expertise",
        # "technologies", # work experience massup ->
        "skill set",
        "technical expertise",
        "core skills",
        "key skills",
        "professional skills"
    ],
    "projects": [
        "projects",
        "project",
        "key projects",
        "personal projects",
        "academic projects",
        "professional projects",
        "project experience"
    ]
}

# > stop words for text cleaning
STOP_WORDS = [
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which",
    "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "through", "during", "before", "after", "above", "below", "up", "down", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when",
    "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t",
    "can", "will", "just", "don", "should", "now"
]

# > strong section indicators - high confidence keywords
STRONG_SECTION_KEYWORDS = [
    # > experience related
    "experience", "professional experience", "work experience", "employment history",
    "career history", "work history", "professional background", "employment background",

    # > education related
    "education", "educational background", "academic background", "qualifications",
    "academic qualifications", "degrees", "academic record",

    # > skills related
    "skills", "technical skills", "core competencies", "competencies", "expertise",
    "skill set", "technical expertise", "core skills", "key skills",

    # > projects related
    "projects", "key projects", "personal projects", "academic projects", "project experience",

    # > other common sections
    "achievements", "accomplishments", "awards", "certifications", "certificates",
    "summary", "profile", "objective", "interests", "activities", "publications",
    "references", "contact", "personal information", "courses", "certified courses"
]

# > words that indicate content rather than headers -> (negative indicators)
CONTENT_INDICATORS = [
    # > dates and time
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december", "jan", "feb", "mar", "apr",
    "jun", "jul", "aug", "sep", "oct", "nov", "dec", "present", "current",

    # > contact info indicators
    "@", "http", "www", "gmail", "email", "phone", "mobile", "linkedin",

    # > common job description words
    "responsible", "managed", "developed", "implemented", "created", "designed",
    "worked", "led", "coordinated", "supervised", "maintained", "performed",

    # > location indicators
    "city", "state", "country", "address", "location", "based", "located"
]

# > common section header patterns (regex)
SECTION_HEADER_PATTERNS = [
    r'^[A-Z\s&-]{2,20}$',  # > ALL CAPS headers like "WORK EXPERIENCE"
    r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # > Title Case like "Work Experience"
    r'^[A-Za-z\s]+:$',  # > headers ending with colon like "Skills:"
    r'^\d+\.\s*[A-Za-z\s]+$',  # > numbered headers like "1. Experience"
    r'^•\s*[A-Za-z\s]+$',  # > bulleted headers like "• Technical Skills"
    r'^-+\s*[A-Za-z\s]+\s*-+$',  # > dashed headers like "--- Skills ---"
]

# > HELPER FUNCTIONS
def clean_text(text):
    """Clean text by removing punctuation and stop words"""
    if not text or text.lower() == "na":
        return "NA"
    # > remove punctuation
    text = re.sub(r"[^\w\s]", "", text)
    # > remove symbols and stop words, and split into words
    words = re.findall(r"\b\w+\b", text.lower())
    cleaned_words = [word for word in words if word not in STOP_WORDS]
    return " ".join(cleaned_words)

def contains_keyword(text, keywords):
    """Check if text contains any of the given keywords with flexible matching"""
    if not text:
        return False

    cleaned_text = clean_text(text)
    for keyword in keywords:
        # > handle both string patterns and regex patterns
        if isinstance(keyword, str):
            # > for regular strings, create flexible pattern
            if keyword.startswith(r'') or '\\' in keyword:
                # > it's already a regex pattern
                try:
                    if re.search(keyword, cleaned_text, re.I):
                        return True
                except:
                    # > fallback to simple search if regex fails
                    if keyword.lower() in cleaned_text.lower():
                        return True
            else:
                # > create flexible pattern for plain text
                pattern = r"\b" + re.sub(r"\s+", r"[\s\-\:]*", re.escape(keyword)) + r"\b"
                if re.search(pattern, cleaned_text, re.I):
                    return True
    return False

def matched_section(line_words, keyword_list):
    """Check if any words in line match the keyword list"""
    if not line_words or not keyword_list:
        return None

    for word in line_words:
        if word.lower() in [k.lower() for k in keyword_list]:
            return word
    return None

def is_preceded_by_empty_line(text_lines, current_index, lookback=2):
    """Check if line is preceded by empty lines (indicates section break)"""
    if current_index == 0:
        return True  # > first line gets bonus

    empty_count = 0
    for i in range(max(0, current_index - lookback), current_index):
        if not text_lines[i].strip():
            empty_count += 1

    return empty_count > 0

def has_content_following(text_lines, current_index, lookahead=3):
    """Check if meaningful content follows this line"""
    if current_index >= len(text_lines) - 1:
        return False

    for i in range(current_index + 1, min(len(text_lines), current_index + lookahead + 1)):
        line = text_lines[i].strip()
        if line and len(line.split()) > 3:  # > has substantial content
            return True

    return False

def contains_strong_section_keywords(line):
    """Check for high-confidence section keywords"""
    if not line:
        return False

    line_lower = line.lower().strip()

    # > check against strong keywords
    for keyword in STRONG_SECTION_KEYWORDS:
        if keyword.lower() in line_lower:
            return True

    return False

def has_section_keywords(line):
    """Check if line contains any section-related keywords"""
    if not line:
        return False

    # > check RESUME_SECTIONS_DICT
    for key in RESUME_SECTIONS_DICT:
        if contains_keyword(line, RESUME_SECTIONS_DICT[key]):
            return True

    # > check KEYWORDS_DICT
    line_processed = [wp for wp in [re.sub(r"[^.\-\w\s]", "", w.strip()) for w in line.lower().split()] if wp]
    for key in KEYWORDS_DICT:
        if matched_section(line_processed, KEYWORDS_DICT[key]):
            return True

    return False

def contains_content_indicators(line):
    """Check if line contains indicators that suggest it's content rather than a header"""
    if not line:
        return False

    line_lower = line.lower()

    # > check existing content indicators
    for indicator in CONTENT_INDICATORS:
        if indicator in line_lower:
            return True

    # > additional checks for sentence-like patterns
    # > check for common verbs that indicate content
    content_verbs = ['worked', 'developed', 'managed', 'created', 'implemented',
                     'designed', 'led', 'coordinated', 'performed', 'handled',
                     'responsible', 'collaborated', 'contributed', 'focused',
                     'utilized', 'reported', 'participated', 'proficient']

    if any(verb in line_lower for verb in content_verbs):
        return True

    # > check for phrases that indicate sentences
    if line_lower.startswith(('i am', 'i have', 'i was', 'the ', 'a ', 'an ')):
        return True

    return False

def matches_header_pattern(line):
    """Check if line matches common section header patterns"""
    if not line:
        return False

    line_stripped = line.strip()

    for pattern in SECTION_HEADER_PATTERNS:
        if re.match(pattern, line_stripped):
            return True

    return False

# > fix for false positives
# ( eg. "TECHNICAL SKILLS" being detected as company names or company names being detected as skills)
def looks_like_company_name(line):
    """Detect if line looks like a company/organization name"""
    if not line:
        return False

    line_lower = line.strip().lower()

    # > company suffixes and indicators
    company_indicators = [
        'inc', 'llc', 'ltd', 'corp', 'corporation', 'company', 'co.',
        'pvt', 'private', 'limited', 'technologies', 'solutions', 'systems',
        'group', 'services', 'consulting', 'associates', 'partners',
        'enterprises', 'india', 'usa', 'gmbh', 's.a.', 'ag', 'plc'
    ]

    # > check for company indicators
    for indicator in company_indicators:
        if indicator in line_lower:
            # > make sure it's not just the word "technologies" in "TECHNICAL SKILLS"
            if line.isupper() and len(line.split()) <= 3:
                continue  # > skip all-caps short phrases (likely section headers)
            return True

    return False


# > IMPROVED SECTION DETECTION
def is_section_header_improved(line, text_lines, line_index):
    """
    section header detection
    returns True if line is likely a section header
    """
    if not line or not line.strip():
        return False


    # > check cmpny name first
    if looks_like_company_name(line):
        return False

    # > CRITICAL -> Check for sentence continuation (e.g., "projects." at end of paragraph)
    # > if line ends with period and is short (1-2 words), might be sentence continuation
    if line.strip().endswith('.') and len(line.split()) <= 2:
        # Check if there's NO empty line above (indicates continuation)
        if line_index > 0 and not is_preceded_by_empty_line(text_lines, line_index, lookback=1):
            return False  # > likely a sentence continuation, not a header

        # Check if previous line exists and doesn't end with sentence-ending punctuation
        if line_index > 0:
            prev_line = text_lines[line_index - 1].strip()
            if prev_line and not prev_line[-1] in '.!?:;':
                # Previous line doesn't end properly = this is likely continuation
                return False

    # > Additional check: if line ends with period and starts with lowercase,
    # > it's almost certainly a continuation
    if line.strip().endswith('.') and line.strip()[0].islower():
        return False

    score = 0
    word_count = len(line.split())
    line_stripped = line.strip()
    line_lower = line_stripped.lower()

    # > CRITICAL -> Immediate disqualifiers for obvious content
    # > check for sentence starters that indicate content, not headers
    sentence_starters = ['i am', 'i have', 'i was', 'i worked', 'the ', 'a ', 'an ',
                         'this ', 'responsible for', 'worked on', 'developed',
                         'managed', 'created', 'performed',
                         'experience in', 'experienced in', 'extensive experience']
    if any(line_lower.startswith(starter) for starter in sentence_starters):
        return False  # > immediate rejection

    # > CRITICAL ->  long lines are almost never headers
    if word_count > 12:
        return False

    # > very short non-alphabetic lines are unlikely headers (mostly noise)
    if len(line.strip()) <= 2 and not line.strip().isalpha():
        return False


    # > check for dates in the line (strong content indicator)
    if re.search(r'\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{2,4}', line) or \
       re.search(r'(19|20)\d{2}', line):
        if not line.isupper():  # > unless it's an all-caps section with dates
            return False

    # > direct match for common section headers (highest priority)
    common_sections = ["CERTIFICATIONS", "EDUCATION", "EXPERIENCE", "SKILLS",
                       "PROJECTS", "SUMMARY", "PROFESSIONAL SUMMARY",
                       "EMPLOYMENT HISTORY", "WORK EXPERIENCE", "KEY ACHIEVEMENTS",
                       "STRENGTHS", "COURSES",
                       "RELATED COURSEWORK","COURSEWORK", "RELEVANT COURSEWORK"]


    # >> temo fix
    line_clean = line_stripped.rstrip('.:;,!?').upper()
    if line_clean in common_sections:
        return True
    # >> tempo fix




    if line_stripped.upper() in common_sections:
        score += 0.5  # > very strong boost for exact matches
    # Length scoring
    if 1 <= word_count <= 4:
        score += 0.35  # > strong preference for short headers
    elif word_count <= 6 and has_section_keywords(line):
        score += 0.25
    elif word_count <= 10 and has_section_keywords(line):
        score += 0.1  # > seduced score for longer potential headers
    else:
        score -= 0.3  # > penalty for long lines

    # > context scoring
    if is_preceded_by_empty_line(text_lines, line_index):
        score += 0.2

    if has_content_following(text_lines, line_index):
        score += 0.15

    # > keyword strength scoring - BUT with stricter conditions
    if contains_strong_section_keywords(line):
        # > if line contains "experience" keyword, require it to be very short (likely a header)
        if 'experience' in line_lower and word_count > 5:
            return False
        # > only give keyword bonus if line is reasonably short
        if word_count <= 6:
            score += 0.3
        elif word_count <= 10:
            score += 0.1  # > reduced bonus for longer lines
        # > no bonus for very long lines even with keywords
    elif has_section_keywords(line):
        if word_count <= 6:
            score += 0.15

    # > format scoring
    if line.isupper() and word_count <= 8:
        score += 0.25
    elif line.istitle() and word_count <= 4:
        score += 0.15

    # > pattern matching bonus
    if matches_header_pattern(line):
        score += 0.1

    # > bonus for headers ending with colon
    if line.strip().endswith(':') and word_count <= 4:
        score += 0.15

    # > PENALTY for lines ending with period (headers rarely end with periods)
    # Exception: if it's ALL CAPS or very short and matches known sections
    if line.strip().endswith('.'):
        if not (line.isupper() and word_count <= 3):
            score -= 0.3  # > strong penalty for period-ending lines

    # > CRITICAL -> penalty for content indicators
    if contains_content_indicators(line):
        score -= 0.4
    # > bullet point check
    if line.strip().startswith('•'):
        score -= 0.4

    # > check for lowercase words (headers are usually Title Case or ALL CAPS)
    words = line_stripped.split()
    if len(words) > 3:
        lowercase_count = sum(1 for w in words[1:] if w.islower() and len(w) > 2)
        if lowercase_count > len(words) * 0.3:  # > more than 30% lowercase
            score -= 0.3
    if score >= 0.8:
        return True  # > high score = definitely a header
    elif score >= 0.75 and has_section_keywords(line):
        return True  # > borderline score but has keywords = probably header
    else:
        return False  # > low score or no keywords = not a header

    # > depriciated -> still keeping for testing
    # return score >= 0.75



def determine_section_name(line):
    """Determine which section this header line represents"""
    if not line:
        return None

    line_stripped = line.strip().upper()

    # > direct matches for common sections (highest priority)
    if line_stripped == "CERTIFICATIONS":
        return "certifications"
    if line_stripped == "EDUCATION":
        return "education"
    if line_stripped == "EXPERIENCE" or line_stripped == "WORK EXPERIENCE":
        return "experience"
    if line_stripped == "SKILLS" or line_stripped == "TECHNICAL SKILLS":
        return "skills"
    if line_stripped == "PROJECTS":
        return "projects"
    if line_stripped == "SUMMARY" or line_stripped == "PROFESSIONAL SUMMARY":
        return "summary"
    if line_stripped in ["RELATED COURSEWORK", "COURSEWORK", "RELEVANT COURSEWORK", "ACADEMIC COURSEWORK"]:
        return "courses"

    # > continue with your existing logic for other cases
    section_name = None

    # > check RESUME_SECTIONS_DICT
    for key in RESUME_SECTIONS_DICT:
        if contains_keyword(line, RESUME_SECTIONS_DICT[key]):
            section_name = key
            break

    # > if still no match, try to infer from strong keywords
    if not section_name:
        line_lower = line.lower().strip()
        if any(term in line_lower for term in ["experience", "work", "employment", "career"]):
            section_name = "experience"
        elif any(term in line_lower for term in ["education", "academic", "qualification", "degree"]):
            section_name = "education"
        elif any(term in line_lower for term in ["skill", "competenc", "technical", "expertise"]):
            section_name = "skills"
        elif any(term in line_lower for term in ["project", "development", "implementation"]):
            section_name = "projects"
        elif any(term in line_lower for term in ["coursework", "course work"]):
            section_name = "courses"  # > specifically for coursework sections
        elif any(term in line_lower for term in ["certification", "certificate"]):
            section_name = "certifications"  # For certifications only
        elif any(term in line_lower for term in ["training", "workshop"]):
            section_name = "courses"  # > training goes to courses
        elif any(term in line_lower for term in ["achievement", "accomplishment", "award", "honor"]):
            section_name = "achievements"
        elif any(term in line_lower for term in ["summary", "profile", "overview","professional summary"]):
            section_name = "summary"
    return section_name


# > MAIN EXTRACTION FUNCTIONS

def extract_entities_improved(text_raw):
    """
    Our main extraction function using improved section header detection
    """
    if not text_raw:
        return {"introduction": []}

    text_lines = [l.strip() for l in text_raw.split("\n")]
    sections = {"introduction": []}
    current_section = "introduction"

    for i, line in enumerate(text_lines):
        if not line:
            continue

        # > check if this line is a section header using improved scoring
        if is_section_header_improved(line, text_lines, i):
            # > determine which section this header represents
            section_name = determine_section_name(line)

            # > if we found a section, switch to it
            if section_name:
                current_section = section_name
                if current_section not in sections:
                    sections[current_section] = []
                continue  # > don't add the header line itself to content

        # > add line to current section
        sections[current_section].append(line)

    return sections

def extract_entities_latest_original(text_raw):
    """
     original extract_entities_latest function for comparison (kept for improvement measures)
    """
    if not text_raw:
        return {"introduction": []}

    text = [l.strip() for l in text_raw.split("\n")]
    r = {"introduction": []}
    section = "introduction"

    for line in text:
        line_processed = [wp for wp in [re.sub(r"[^.\-\w\s]", "", w.strip()) for w in line.lower().split()] if wp]
        sec = ""

        for key in RESUME_SECTIONS_DICT:
            if contains_keyword(line, RESUME_SECTIONS_DICT[key]):
                sec = [key]
                break

        if len(line_processed) < 5 and sec:
            section = " ".join(list(sec))
            if section not in r.keys():
                r[section] = []
        else:
            r[section].append(line) if line else None

    return r

def post_process_sections(sections):
    """
    Post-process sections to handle edge cases and validate content
    """
    if not sections:
        return {}

    processed_sections = {}

    for section_name, content in sections.items():
        if not content:  # > skip empty sections
            continue

        # > clean up content - remove empty lines at start/end
        cleaned_content = []
        for line in content:
            if line and line.strip():
                cleaned_content.append(line)

        if cleaned_content:  # > only add sections with actual content
            processed_sections[section_name] = cleaned_content

    return processed_sections

def parse_cv_sections_improved(cv_text):
    """
    main function to parse CV text into sections using improved detection
    """
    if not cv_text:
        return {}

    # > extract sections using improved method
    raw_sections = extract_entities_improved(cv_text)

    # > post-process to clean up
    final_sections = post_process_sections(raw_sections)

    return raw_sections, final_sections
