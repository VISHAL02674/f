# > imports
import re
from datetime import datetime

# > DICTIONARIES AND CONFIGURATION
# > main section keywords dictionary -> covers most resume sections
# > COMPREHENSIVE - handles all possible naming variations
KEYWORDS_DICT = {
    "projects": ["project name", "project title", "projects", "personal projects", "key projects",
                 "academic projects", "professional projects", "project experience", "project work",
                 "project details", "project description", "major projects", "relevant projects"],

    "introduction": ["introduction", "contact", "details", "personal", "basic information",
                     "personal information", "contact information", "contact details", "about me",
                     "personal details", "bio", "biography"],

    "courses": ["courses", "coursework", "related coursework", "workshops", "training",
                "professional development", "certified courses", "relevant coursework",
                "academic coursework", "trainings", "course work", "training programs",
                "certifications and training"],

    "skills": ["skills", "competencies", "expertise", "strength", "technical skills",
               "core competencies", "skill set", "technologies", "tools and technologies",
               "languages tools and technologies", "tools technologies", "technologies and tools",
               "technical expertise", "core skills", "key skills", "professional skills",
               "technical proficiency", "areas of expertise", "technology stack", "tech stack",
               "languages and tools", "tools", "programming languages", "technology skills",
               "languages tools technologies", "tools technologies web servers"],

    "summary": ["summary", "overview", "profile", "profile summary", "professional summary",
                "career summary", "executive summary", "career overview", "professional profile",
                "career profile", "about", "objective summary", "introduction summary"],

    "achievements": ["accomplishments", "achievements", "awards", "honors", "recognition",
                     "accolades", "awards and honors", "awards and achievements",
                     "honors and awards", "recognitions", "certificates awards achievements"],

    "affiliations": ["affiliations", "memberships", "associations", "professional memberships",
                     "professional affiliations", "memberships and affiliations"],

    "objective": ["objectives", "career objective", "professional objective", "goal",
                  "career goals", "career aspiration", "professional goals", "objective"],

    "interests": ["interests", "hobbies", "personal interests", "hobbies and interests",
                  "extra curricular", "extracurricular activities", "personal hobbies"],

    "certifications": ["certify", "license", "qualify", "chartered", "register", "accredit",
                       "diploma", "fellow", "certifications", "certificates",
                       "professional certifications", "certified courses", "licenses",
                       "certification", "professional licenses", "credentials"],

    "references": ["references", "recommendations", "testimonials", "endorsements",
                   "professional references", "reference"],

    "publications": ["publications", "conferences", "journals", "meets", "summits", "seminars",
                     "talks", "presentations", "patents", "research papers", "papers",
                     "research", "published work", "conference papers"],

    "activities": ["activities", "participations", "involvement", "service", "volunteer",
                   "engagement", "extracurricular", "community service", "volunteer work",
                   "extra curricular activities", "extracurricular activities",
                   "volunteer experience", "community involvement", "agile tools"],

    "D.O.B": ["date of birth", "dob", "d.o.b", "birth date", "date of birth"],

    "gender": ["gender", "sex"],

    "experience": ["professional experience", "work experience", "employment history",
                   "career history", "experience", "work history", "employment", "appointments",
                   "previous positions", "business exposure", "current profile", "job profile",
                   "professional background", "job experience", "work", "career",
                   "employment background", "work experiences", "job history", "career background",
                   "professional work", "job experiences", "working experience", "work exp"]
}

# > resume sections with regex patterns for flexible matching
# > COMPREHENSIVE - covers all possible variations and formats
RESUME_SECTIONS_DICT = {
    "experience": [
        r"work[\s]{0,}experience[s]?",
        r".*workexperience.*",
        r"professional[\s]{0,}experience[s]?",
        r"job[\s]{0,}experience[s]?",
        r"employment[\s]{0,}history",
        r"career[\s]{0,}history",
        r"work[\s]{0,}history",
        r"job[\s]{0,}history",
        r"employment[\s]{0,}background",
        r"professional[\s]{0,}background",
        r"career[\s]{0,}background",
        r"experience[\s]*:?[\s]*\d*[\s]*\w*",  # Handles "EXPERIENCE: 4 years"
        r"experience[s]?",
        r"employment",
        r"appointments",
        r"previous[\s]{0,}positions",
        r"business[\s]{0,}exposure",
        r"current[\s]{0,}profile",
        r"job[\s]{0,}profile",
        r"working[\s]{0,}experience",
        r"work[\s]{0,}exp",
        "experience",
        "professional experience",
        "work experience",
        "job experience",
        "employment history",
        "career history",
        "work history",
        "job history",
        "career background",
        "professional background",
        "employment background",
        "work",
        "career",
        "employment",
        "job experiences",
        "work experiences",
        "working experience"
    ],
    "education": [
        r"education(al)?[\s]{0,}",
        r"academic[\s]{0,}background",
        r"academic[\s]{0,}history",
        r"education(al)?[\s]{0,}background",
        r"education(al)?[\s]{0,}qualification[s]?",
        r"education(al)?[\s]{0,}details",
        r"academic[\s]{0,}record",
        r"academic[\s]{0,}qualifications",
        r"scholastic[\s]{0,}achievements",
        r"educational[\s]{0,}history",
        "education",
        "educational",
        "academic background",
        "academic history",
        "qualifications",
        "academic qualifications",
        "educational background",
        "educational qualifications",
        "highest education",
        "professional qualification",
        "education history",
        "scholastics",
        "scholastic",
        "academia",
        "academic record",
        "degrees",
        "academic details",
        "educational details",
        "academics"
    ],
    "skills": [
        r"technical[\s]{0,}skills",
        r"core[\s]{0,}competencies",
        r"tools[\s,]*and[\s,]*technologies",
        r"languages[\s,]*tools[\s,]*and[\s,]*technologies",
        r"languages[\s,]*tools[\s,]*technologies",
        r"tools[\s,]*technologies[\s,]*web[\s,]*servers",
        r"tools[\s,]*technologies",
        r"technology[\s]{0,}stack",
        r"tech[\s]{0,}stack",
        r"programming[\s]{0,}languages",
        "skills",
        "technical skills",
        "core competencies",
        "competencies",
        "expertise",
        "skill set",
        "technical expertise",
        "core skills",
        "key skills",
        "professional skills",
        "technical proficiency",
        "areas of expertise",
        "technology stack",
        "tech stack",
        "tools and technologies",
        "languages and tools",
        "languages tools and technologies",
        "languages tools technologies",
        "tools technologies web servers",
        "tools technologies",
        "tools",
        "programming languages",
        "technology skills",
        "technologies"
    ],
    "projects": [
        r"project[s]?[\s]{0,}",
        r"personal[\s]{0,}project[s]?",
        r"academic[\s]{0,}project[s]?",
        r"professional[\s]{0,}project[s]?",
        r"key[\s]{0,}project[s]?",
        r"project[\s]{0,}experience",
        r"project[\s]{0,}work",
        r"project[\s]{0,}description",
        r"project[\s]{0,}details",
        "projects",
        "project",
        "key projects",
        "personal projects",
        "academic projects",
        "professional projects",
        "project experience",
        "project work",
        "project details",
        "project description",
        "major projects",
        "relevant projects"
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
# > COMPREHENSIVE - all variations for maximum detection
STRONG_SECTION_KEYWORDS = [
    # > experience related (EXPANDED)
    "experience", "professional experience", "work experience", "job experience",
    "employment history", "career history", "work history", "job history",
    "professional background", "employment background", "career background",
    "employment", "work", "career", "job experiences", "work experiences",
    "working experience", "job profile", "work exp", "professional work",

    # > education related (EXPANDED)
    "education", "educational background", "academic background", "qualifications",
    "academic qualifications", "educational qualifications", "degrees", "academic record",
    "educational details", "academic details", "academics", "educational history",
    "academic history", "scholastics", "scholastic", "academia",

    # > skills related (EXPANDED)
    "skills", "technical skills", "core competencies", "competencies", "expertise",
    "skill set", "technical expertise", "core skills", "key skills", "professional skills",
    "technical proficiency", "areas of expertise", "technology stack", "tech stack",
    "tools and technologies", "languages and tools", "languages tools and technologies",
    "languages tools technologies", "tools technologies web servers", "tools technologies",
    "tools", "programming languages", "technology skills", "technologies",

    # > projects related (EXPANDED)
    "projects", "project", "key projects", "personal projects", "academic projects",
    "professional projects", "project experience", "project work", "project details",
    "project description", "major projects", "relevant projects",

    # > summary related (EXPANDED)
    "summary", "professional summary", "career summary", "executive summary",
    "profile", "professional profile", "career profile", "profile summary",
    "career overview", "overview", "about", "introduction summary",

    # > achievements related (EXPANDED)
    "achievements", "accomplishments", "awards", "honors", "recognition", "accolades",
    "awards and honors", "awards and achievements", "honors and awards",
    "additional experience and awards", "certificates awards achievements",

    # > certifications related (EXPANDED)
    "certifications", "certificates", "professional certifications", "licenses",
    "certification", "professional licenses", "credentials", "certified courses",

    # > other common sections (EXPANDED)
    "objective", "career objective", "professional objective", "career goals",
    "interests", "hobbies", "personal interests", "hobbies and interests",
    "activities", "extracurricular activities", "extra curricular activities",
    "volunteer", "volunteer work", "community service", "agile tools",
    "publications", "research", "papers", "conference papers",
    "references", "professional references", "recommendations",
    "contact", "contact information", "contact details", "personal information",
    "courses", "coursework", "training", "trainings", "certified courses",
    "course work", "relevant coursework", "related coursework"
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
# > COMPREHENSIVE - handles all formatting styles
SECTION_HEADER_PATTERNS = [
    r'^[A-Z\s&-]{2,30}$',  # > ALL CAPS headers like "WORK EXPERIENCE"
    r'^[A-Z\s&-]{2,30}:$',  # > ALL CAPS with colon like "WORK EXPERIENCE:"
    r'^[A-Z\s&-]{2,30}:\s*.+$',  # > ALL CAPS with colon and text like "EXPERIENCE: 4 years"
    r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # > Title Case like "Work Experience"
    r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*:$',  # > Title Case with colon
    r'^[A-Za-z\s,&-]+:$',  # > headers ending with colon like "Skills:" or "Tools,Technologies:"
    r'^\*\*[A-Za-z\s]+\*\*$',  # > Bold markdown like "**SKILLS**"
    r'^##\s+[A-Za-z\s]+$',  # > Markdown H2 like "## Skills"
    r'^###\s+[A-Za-z\s]+$',  # > Markdown H3 like "### Skills"
    r'^#\s+[A-Za-z\s]+$',  # > Markdown H1 like "# Skills"
    r'^\d+\.\s*[A-Za-z\s]+:?$',  # > numbered headers like "1. Experience" or "1. Experience:"
    r'^•\s*[A-Za-z\s]+:?$',  # > bulleted headers like "• Technical Skills"
    r'^-\s*[A-Za-z\s]+:?$',  # > dash bullets like "- Skills"
    r'^-+\s*[A-Za-z\s]+\s*-+$',  # > dashed headers like "--- Skills ---"
    r'^\*\s*[A-Za-z\s]+:?$',  # > asterisk bullets like "* Skills"
    r'^[A-Z][A-Z\s,&-]{2,30}$',  # > Mixed caps like "TOOLS,TECHNOLOGIES"
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

    # Remove markdown, bold markers, and colons for matching
    line_clean = line.strip()
    line_clean = re.sub(r'^[#\*\-•\s]+', '', line_clean)  # Remove markdown/bullets at start
    line_clean = re.sub(r'\*\*', '', line_clean)  # Remove bold markers
    line_clean = line_clean.rstrip(':.,;!?')  # Remove trailing punctuation
    line_stripped = line_clean.upper().strip()

    # > COMPREHENSIVE direct matches (handles variations with/without colons, etc.)

    # Experience variations
    if line_stripped in ["EXPERIENCE", "WORK EXPERIENCE", "JOB EXPERIENCE", "PROFESSIONAL EXPERIENCE",
                         "EMPLOYMENT HISTORY", "CAREER HISTORY", "WORK HISTORY", "JOB HISTORY",
                         "EMPLOYMENT", "CAREER", "WORK", "EMPLOYMENT BACKGROUND", "CAREER BACKGROUND",
                         "PROFESSIONAL BACKGROUND", "WORKING EXPERIENCE", "JOB EXPERIENCES",
                         "WORK EXPERIENCES"]:
        return "experience"

    # Handle "EXPERIENCE: X years" pattern
    if line_stripped.startswith("EXPERIENCE") and ("YEAR" in line_stripped or "MONTH" in line_stripped):
        return "experience"

    # Skills variations
    if line_stripped in ["SKILLS", "TECHNICAL SKILLS", "CORE COMPETENCIES", "COMPETENCIES",
                         "SKILL SET", "TECHNICAL EXPERTISE", "CORE SKILLS", "KEY SKILLS",
                         "PROFESSIONAL SKILLS", "TOOLS AND TECHNOLOGIES", "TECHNOLOGIES",
                         "LANGUAGES AND TOOLS", "LANGUAGES TOOLS AND TECHNOLOGIES",
                         "LANGUAGES TOOLS TECHNOLOGIES", "TOOLS TECHNOLOGIES WEB SERVERS",
                         "TOOLS TECHNOLOGIES", "TOOLS", "PROGRAMMING LANGUAGES",
                         "TECHNOLOGY STACK", "TECH STACK", "TECHNICAL PROFICIENCY",
                         "AREAS OF EXPERTISE"]:
        return "skills"

    # Handle comma-separated skills headers
    if "TOOLS" in line_stripped and "TECHNOLOG" in line_stripped:
        return "skills"
    if "LANGUAGE" in line_stripped and "TOOLS" in line_stripped:
        return "skills"

    # Education variations
    if line_stripped in ["EDUCATION", "EDUCATIONAL BACKGROUND", "ACADEMIC BACKGROUND",
                         "QUALIFICATIONS", "ACADEMIC QUALIFICATIONS", "EDUCATIONAL QUALIFICATIONS",
                         "DEGREES", "ACADEMIC RECORD", "EDUCATIONAL DETAILS", "ACADEMIC DETAILS",
                         "ACADEMICS", "EDUCATIONAL HISTORY", "ACADEMIC HISTORY", "EDUCATIONAL",
                         "EDUCATION HISTORY", "EDUCATION DETAILS"]:
        return "education"

    # Projects variations
    if line_stripped in ["PROJECTS", "PROJECT", "KEY PROJECTS", "PERSONAL PROJECTS",
                         "ACADEMIC PROJECTS", "PROFESSIONAL PROJECTS", "PROJECT EXPERIENCE",
                         "PROJECT WORK", "PROJECT DETAILS", "PROJECT DESCRIPTION",
                         "MAJOR PROJECTS", "RELEVANT PROJECTS", "PROJECT SUMMARY"]:
        return "projects"

    # Summary variations
    if line_stripped in ["SUMMARY", "PROFESSIONAL SUMMARY", "CAREER SUMMARY", "EXECUTIVE SUMMARY",
                         "PROFILE", "PROFESSIONAL PROFILE", "CAREER PROFILE", "PROFILE SUMMARY",
                         "CAREER OVERVIEW", "OVERVIEW", "ABOUT", "CAREER OBJECTIVE"]:
        return "summary"

    # Courses/Training variations
    if line_stripped in ["COURSES", "COURSEWORK", "RELATED COURSEWORK", "RELEVANT COURSEWORK",
                         "ACADEMIC COURSEWORK", "COURSE WORK", "TRAINING", "TRAININGS",
                         "TRAINING PROGRAMS", "PROFESSIONAL DEVELOPMENT", "WORKSHOPS",
                         "CERTIFICATIONS AND TRAINING"]:
        return "courses"

    # Certifications variations
    if line_stripped in ["CERTIFICATIONS", "CERTIFICATES", "PROFESSIONAL CERTIFICATIONS",
                         "LICENSES", "CERTIFICATION", "PROFESSIONAL LICENSES", "CREDENTIALS",
                         "CERTIFIED COURSES"]:
        return "certifications"

    # Achievements variations
    if line_stripped in ["ACHIEVEMENTS", "ACCOMPLISHMENTS", "AWARDS", "HONORS", "RECOGNITION",
                         "ACCOLADES", "AWARDS AND HONORS", "AWARDS AND ACHIEVEMENTS",
                         "HONORS AND AWARDS", "ADDITIONAL EXPERIENCE AND AWARDS",
                         "CERTIFICATES AWARDS ACHIEVEMENTS"]:
        return "achievements"

    # Activities/Interests variations
    if line_stripped in ["ACTIVITIES", "EXTRACURRICULAR ACTIVITIES", "EXTRA CURRICULAR ACTIVITIES",
                         "VOLUNTEER", "VOLUNTEER WORK", "COMMUNITY SERVICE", "AGILE TOOLS"]:
        return "activities"

    if line_stripped in ["INTERESTS", "HOBBIES", "PERSONAL INTERESTS", "HOBBIES AND INTERESTS"]:
        return "interests"

    # Other sections
    if line_stripped in ["OBJECTIVE", "CAREER OBJECTIVE", "PROFESSIONAL OBJECTIVE", "GOAL"]:
        return "objective"

    if line_stripped in ["PUBLICATIONS", "RESEARCH", "PAPERS", "CONFERENCE PAPERS"]:
        return "publications"

    if line_stripped in ["REFERENCES", "PROFESSIONAL REFERENCES", "RECOMMENDATIONS"]:
        return "references"

    if line_stripped in ["CONTACT", "CONTACT INFORMATION", "CONTACT DETAILS"]:
        return "introduction"

    # > Fallback: check RESUME_SECTIONS_DICT with regex
    section_name = None
    for key in RESUME_SECTIONS_DICT:
        if contains_keyword(line, RESUME_SECTIONS_DICT[key]):
            section_name = key
            break

    # > Final fallback: infer from keywords in line
    if not section_name:
        line_lower = line_clean.lower()

        # Experience keywords
        if any(term in line_lower for term in ["experience", "employment", "work history",
                                                 "job history", "career", "work"]):
            section_name = "experience"
        # Education keywords
        elif any(term in line_lower for term in ["education", "academic", "qualification",
                                                   "degree", "scholastic"]):
            section_name = "education"
        # Skills keywords
        elif any(term in line_lower for term in ["skill", "competenc", "technical", "expertise",
                                                   "tools", "technolog", "programming"]):
            section_name = "skills"
        # Projects keywords
        elif any(term in line_lower for term in ["project"]):
            section_name = "projects"
        # Courses keywords
        elif any(term in line_lower for term in ["coursework", "course work", "training"]):
            section_name = "courses"
        # Certifications keywords
        elif any(term in line_lower for term in ["certification", "certificate", "license"]):
            section_name = "certifications"
        # Achievements keywords
        elif any(term in line_lower for term in ["achievement", "accomplishment", "award", "honor"]):
            section_name = "achievements"
        # Summary keywords
        elif any(term in line_lower for term in ["summary", "profile", "overview"]):
            section_name = "summary"
        # Activities keywords
        elif any(term in line_lower for term in ["activities", "volunteer", "extracurricular"]):
            section_name = "activities"
        # Interests keywords
        elif any(term in line_lower for term in ["interest", "hobbies"]):
            section_name = "interests"

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
