"""
Comprehensive Ayurvedic Synonym Dictionary
Bhruhat Trayi AI Assistant by PraKul

Version 2.0 - Expanded with 500+ terms
- All major diseases
- All treatments
- Body systems
- Diagnostic terms
- English ↔ Sanskrit ↔ Devanagari mapping
"""

# =============================================================================
# MASTER AYURVEDIC SYNONYM DICTIONARY
# =============================================================================

AYURVEDIC_SYNONYMS = {
    
    # =========================================================================
    # FUNDAMENTAL CONCEPTS
    # =========================================================================
    
    "ayurveda": ["āyurveda", "आयुर्वेद", "ayurvedam", "veda", "life science"],
    "definition": ["lakṣaṇa", "lakshana", "लक्षण", "paribhāṣā", "paribhasha", "svarūpa"],
    "purpose": ["prayojana", "प्रयोजन", "prayojanam", "artha", "hetu", "phala"],
    "principle": ["siddhānta", "siddhanta", "सिद्धान्त", "tantra"],
    
    # =========================================================================
    # HEALTH & WELLNESS
    # =========================================================================
    
    "health": ["svāsthya", "svasthya", "स्वास्थ्य", "svastha", "स्वस्थ", "ārogya", "arogya", 
               "आरोग्य", "nirāmaya", "niramaya", "sama", "samadoṣa", "समदोष"],
    "healthy": ["svastha", "स्वस्थ", "niroga", "ārogya", "niramaya", "prakṛti"],
    "wellness": ["svāsthya", "svasthya", "स्वास्थ्य", "sukha", "ārogya"],
    "swastha": ["स्वस्थ", "svastha", "healthy", "health", "samadoṣa", "समदोष"],
    
    # =========================================================================
    # DISEASE - GENERAL TERMS
    # =========================================================================
    
    "disease": ["roga", "रोग", "vyādhi", "vyadhi", "व्याधि", "vikāra", "vikara", "विकार",
                "āmaya", "amaya", "आमय", "gada", "गद", "ātaṅka", "atanka"],
    "illness": ["roga", "रोग", "vyādhi", "व्याधि", "vikāra", "āmaya"],
    "disorder": ["vikāra", "vikara", "विकार", "vikṛti", "vikrti", "विकृति", "roga"],
    "pathology": ["vikṛti", "vikrti", "विकृति", "samprapti", "सम्प्राप्ति"],
    
    # =========================================================================
    # TRIDOSHA SYSTEM
    # =========================================================================
    
    "dosha": ["doṣa", "dosa", "दोष", "tridoṣa", "tridosha", "त्रिदोष"],
    "tridosha": ["tridoṣa", "त्रिदोष", "vāta pitta kapha", "त्रय दोष"],
    "doshas": ["doṣa", "दोष", "tridoṣa", "त्रिदोष"],
    
    # Vata
    "vata": ["vāta", "वात", "vāyu", "vayu", "वायु", "anila", "अनिल", "pavana", "पवन", 
             "marut", "मरुत्", "prāṇa"],
    "vayu": ["vāyu", "वायु", "vāta", "वात", "anila", "pavana", "wind"],
    "wind": ["vāyu", "vayu", "वायु", "vāta", "anila", "pavana"],
    
    # Pitta  
    "pitta": ["पित्त", "pittam", "dahana", "दहन", "agni", "pācaka", "pachaka"],
    "bile": ["pitta", "पित्त", "pittam"],
    
    # Kapha
    "kapha": ["कफ", "śleṣma", "śleṣmā", "shleshma", "श्लेष्मा", "श्लेष्म"],
    "phlegm": ["kapha", "कफ", "śleṣma", "shleshma", "श्लेष्मा"],
    "shleshma": ["śleṣmā", "श्लेष्मा", "kapha", "कफ"],
    
    # Dosha states
    "balance": ["sama", "सम", "sāmya", "samya", "साम्य", "samata", "samatva"],
    "imbalance": ["viṣama", "vishama", "विषम", "vaiṣamya", "vaishamya", "vikṛti"],
    "vitiation": ["prakopa", "प्रकोप", "duṣṭi", "dushti", "दुष्टि", "vṛddhi"],
    "aggravation": ["prakopa", "प्रकोप", "kopa", "vṛddhi", "vrddhi", "वृद्धि"],
    "pacification": ["śamana", "shamana", "शमन", "praśamana", "प्रशमन"],
    
    # =========================================================================
    # SAPTA DHATU (SEVEN TISSUES)
    # =========================================================================
    
    "dhatu": ["dhātu", "धातु", "saptadhātu", "sapta dhātu", "सप्तधातु", "tissue"],
    "tissue": ["dhātu", "dhatu", "धातु"],
    "tissues": ["dhātu", "धातु", "saptadhātu", "सप्तधातु"],
    
    "rasa": ["रस", "rasam", "rasa dhātu", "plasma", "lymph", "chyle"],
    "plasma": ["rasa", "रस", "rasam"],
    
    "rakta": ["रक्त", "raktam", "śoṇita", "shonita", "शोणित", "rudhira", "रुधिर", 
              "asṛk", "asrk", "blood"],
    "blood": ["rakta", "रक्त", "raktam", "śoṇita", "shonita", "rudhira", "asṛk"],
    
    "mamsa": ["māṃsa", "मांस", "peśī", "peshi", "पेशी", "muscle", "flesh"],
    "muscle": ["māṃsa", "mamsa", "मांस", "peśī", "peshi"],
    "flesh": ["māṃsa", "mamsa", "मांस"],
    
    "meda": ["मेद", "medas", "मेदस्", "vasā", "vasa", "वसा", "fat", "adipose"],
    "fat": ["meda", "मेद", "medas", "vasā", "vasa", "sneha"],
    "medas": ["मेदस्", "meda", "मेद", "fat", "vasā"],
    
    "asthi": ["अस्थि", "asthim", "bone"],
    "bone": ["asthi", "अस्थि", "asthim"],
    
    "majja": ["मज्जा", "majjā", "marrow", "bone marrow"],
    "marrow": ["majja", "majjā", "मज्जा"],
    
    "shukra": ["śukra", "शुक्र", "sukra", "vīrya", "virya", "वीर्य", "retas", "रेतस्",
               "semen", "reproductive"],
    "semen": ["śukra", "shukra", "शुक्र", "retas"],
    "reproductive": ["śukra", "shukra", "शुक्र", "ārtava", "artava", "आर्तव"],
    
    # =========================================================================
    # AGNI (DIGESTIVE FIRE)
    # =========================================================================
    
    "agni": ["अग्नि", "jaṭharāgni", "jatharagni", "जाठराग्नि", "pācaka", "pachaka", 
             "पाचक", "vahni", "digestive fire"],
    "digestive fire": ["agni", "अग्नि", "jaṭharāgni", "jatharagni"],
    "digestion": ["pācana", "pachana", "पाचन", "agni", "jaraṇa", "jarana"],
    "metabolism": ["agni", "अग्नि", "dhātvagni", "dhatvagni", "धात्वाग्नि"],
    "jatharagni": ["जाठराग्नि", "jaṭharāgni", "agni", "अग्नि", "digestive fire"],
    
    # Agni types
    "mandagni": ["मन्दाग्नि", "mandāgni", "low digestive fire", "weak digestion"],
    "vishamagni": ["विषमाग्नि", "viṣamāgni", "irregular digestion"],
    "tikshnagni": ["तीक्ष्णाग्नि", "tīkṣṇāgni", "tikshna agni", "strong digestion"],
    "samagni": ["समाग्नि", "samāgni", "balanced digestion", "normal agni"],
    
    # Ama
    "ama": ["आम", "āma", "toxin", "undigested", "metabolic waste"],
    "toxin": ["āma", "ama", "आम", "viṣa", "visha"],
    "undigested": ["āma", "ama", "आम", "apakva"],
    
    # =========================================================================
    # MALA (WASTE PRODUCTS)
    # =========================================================================
    
    "mala": ["मल", "purīṣa", "purisha", "मूत्र", "sveda", "waste"],
    "waste": ["mala", "मल", "kiṭṭa", "kitta", "किट्ट"],
    
    "purisha": ["purīṣa", "पुरीष", "śakṛt", "shakrt", "शकृत्", "vit", "stool", "feces"],
    "stool": ["purīṣa", "purisha", "पुरीष", "śakṛt", "shakrt", "vit", "विट्"],
    "feces": ["purīṣa", "purisha", "पुरीष", "śakṛt"],
    
    "mutra": ["mūtra", "मूत्र", "prasrāva", "urine"],
    "urine": ["mūtra", "mutra", "मूत्र", "prasrāva"],
    
    "sweda": ["sveda", "स्वेद", "prasveda", "gharma", "घर्म", "sweat", "perspiration"],
    "sweat": ["sveda", "स्वेद", "prasveda", "gharma"],
    
    # =========================================================================
    # SROTAS (CHANNELS)
    # =========================================================================
    
    "srotas": ["स्रोतस्", "srota", "nāḍī", "nadi", "नाडी", "mārga", "marga", "मार्ग", "channel"],
    "channel": ["srotas", "स्रोतस्", "srota", "nāḍī", "nadi"],
    "channels": ["srotas", "स्रोतस्", "nāḍī", "nadi"],
    
    # =========================================================================
    # MAJOR DISEASES - METABOLIC
    # =========================================================================
    
    # OBESITY
    "obesity": ["sthaulya", "स्थौल्य", "sthūlatā", "sthulata", "स्थूलता", "medoroga", 
                "मेदोरोग", "atisthūla", "atisthula", "अतिस्थूल", "meda roga"],
    "sthaulya": ["स्थौल्य", "obesity", "medoroga", "मेदोरोग", "sthūlatā", "स्थूलता",
                 "atisthūla", "meda vṛddhi"],
    "medoroga": ["मेदोरोग", "sthaulya", "स्थौल्य", "obesity", "meda vikāra"],
    "overweight": ["sthaulya", "स्थौल्य", "atisthūla", "medoroga"],
    "corpulence": ["sthaulya", "स्थौल्य", "medoroga", "मेदोरोग"],
    "fat disorder": ["medoroga", "मेदोरोग", "sthaulya", "स्थौल्य"],
    
    # EMACIATION
    "emaciation": ["kārśya", "karshya", "कार्श्य", "kṛśatā", "krshatā", "कृशता", 
                   "śoṣa", "shosha", "शोष"],
    "karshya": ["कार्श्य", "kārśya", "emaciation", "kṛśatā", "thinness"],
    "thinness": ["kārśya", "karshya", "कार्श्य", "kṛśatā"],
    "wasting": ["śoṣa", "shosha", "शोष", "kṣaya", "kshaya", "क्षय"],
    
    # DIABETES / PRAMEHA
    "diabetes": ["prameha", "प्रमेह", "madhumeha", "मधुमेह", "meha"],
    "prameha": ["प्रमेह", "diabetes", "madhumeha", "मधुमेह", "meha", "मेह",
                "urinary disorder"],
    "madhumeha": ["मधुमेह", "prameha", "प्रमेह", "diabetes mellitus", "honey urine"],
    "urinary disorder": ["prameha", "प्रमेह", "mūtraroga", "mutra roga"],
    
    # =========================================================================
    # MAJOR DISEASES - DIGESTIVE
    # =========================================================================
    
    # INDIGESTION
    "indigestion": ["ajīrṇa", "ajirna", "अजीर्ण", "agnimāndya", "agnimandya", 
                    "अग्निमान्द्य", "āma", "dyspepsia"],
    "ajirna": ["अजीर्ण", "ajīrṇa", "indigestion", "agnimāndya"],
    "agnimandya": ["अग्निमान्द्य", "agnimāndya", "low digestive fire", "indigestion"],
    "dyspepsia": ["ajīrṇa", "ajirna", "अजीर्ण", "agnimāndya"],
    
    # DIARRHEA
    "diarrhea": ["atisāra", "atisara", "अतिसार", "loose motion", "pravāhikā"],
    "atisara": ["अतिसार", "atisāra", "diarrhea", "loose stool"],
    "loose motion": ["atisāra", "atisara", "अतिसार"],
    
    # DYSENTERY
    "dysentery": ["pravāhikā", "pravahika", "प्रवाहिका", "bloody stool"],
    "pravahika": ["प्रवाहिका", "pravāhikā", "dysentery"],
    
    # CONSTIPATION
    "constipation": ["vibandha", "विबन्ध", "malabaddhatā", "mala baddha", "कोष्ठबद्धता",
                     "koṣṭhabaddhatā"],
    "vibandha": ["विबन्ध", "constipation", "malabaddha"],
    
    # IBS / GRAHANI
    "ibs": ["grahaṇī", "grahani", "ग्रहणी", "grahani dosha"],
    "grahani": ["ग्रहणी", "grahaṇī", "ibs", "malabsorption", "sprue"],
    "malabsorption": ["grahaṇī", "grahani", "ग्रहणी"],
    
    # VOMITING
    "vomiting": ["chardi", "छर्दि", "chardī", "vamana", "वमन"],
    "chardi": ["छर्दि", "vomiting", "emesis"],
    
    # HEMORRHOIDS
    "hemorrhoids": ["arśas", "arshas", "अर्शस्", "piles"],
    "piles": ["arśas", "arshas", "अर्शस्", "hemorrhoids"],
    "arshas": ["अर्शस्", "arśas", "hemorrhoids", "piles"],
    
    # FISTULA
    "fistula": ["bhagandara", "भगन्दर", "bhagandar"],
    "bhagandara": ["भगन्दर", "fistula", "fistula in ano"],
    
    # HERNIA
    "hernia": ["āntra vṛddhi", "antra vrddhi", "आन्त्रवृद्धि"],
    
    # =========================================================================
    # MAJOR DISEASES - RESPIRATORY
    # =========================================================================
    
    # FEVER
    "fever": ["jvara", "jwara", "ज्वर", "santāpa", "santapa", "सन्ताप"],
    "jvara": ["ज्वर", "jwara", "fever", "santāpa", "pyrexia"],
    "jwara": ["ज्वर", "jvara", "fever"],
    
    # COUGH
    "cough": ["kāsa", "kasa", "कास"],
    "kasa": ["कास", "kāsa", "cough"],
    
    # COLD
    "cold": ["pratīśyāya", "pratishyaya", "प्रतिश्याय", "pīnasa", "pinasa", "पीनस"],
    "pratishyaya": ["प्रतिश्याय", "pratīśyāya", "cold", "coryza"],
    "rhinitis": ["pratīśyāya", "pratishyaya", "प्रतिश्याय", "pīnasa"],
    
    # ASTHMA / BREATHLESSNESS
    "asthma": ["śvāsa", "shvasa", "श्वास", "tamaka śvāsa", "tamaka shvasa"],
    "shvasa": ["श्वास", "śvāsa", "asthma", "breathlessness", "dyspnea"],
    "breathlessness": ["śvāsa", "shvasa", "श्वास", "dyspnea"],
    "tamaka shvasa": ["तमक श्वास", "tamaka śvāsa", "bronchial asthma"],
    
    # HICCUP
    "hiccup": ["hikkā", "hikka", "हिक्का"],
    "hikka": ["हिक्का", "hikkā", "hiccup"],
    
    # TUBERCULOSIS
    "tuberculosis": ["rājayakṣmā", "rajayakshma", "राजयक्ष्मा", "yakṣmā", "yakshma",
                     "शोष", "śoṣa", "consumption"],
    "rajayakshma": ["राजयक्ष्मा", "rājayakṣmā", "tuberculosis", "consumption"],
    "consumption": ["rājayakṣmā", "rajayakshma", "राजयक्ष्मा", "śoṣa"],
    
    # =========================================================================
    # MAJOR DISEASES - SKIN
    # =========================================================================
    
    "skin disease": ["kuṣṭha", "kushtha", "कुष्ठ", "tvak roga", "त्वग्रोग", "carmāroga"],
    "kushtha": ["कुष्ठ", "kuṣṭha", "skin disease", "leprosy", "dermatosis"],
    "leprosy": ["kuṣṭha", "kushtha", "कुष्ठ"],
    "dermatosis": ["kuṣṭha", "kushtha", "कुष्ठ", "tvak roga"],
    
    "eczema": ["vicarcikā", "vicharchika", "विचर्चिका"],
    "vicharchika": ["विचर्चिका", "vicarcikā", "eczema"],
    
    "psoriasis": ["kitibha", "किटिभ", "ekakuṣṭha"],
    "kitibha": ["किटिभ", "psoriasis"],
    
    "urticaria": ["śītapitta", "shitapitta", "शीतपित्त", "udarda"],
    "shitapitta": ["शीतपित्त", "śītapitta", "urticaria", "hives"],
    
    # =========================================================================
    # MAJOR DISEASES - MUSCULOSKELETAL
    # =========================================================================
    
    # ARTHRITIS
    "arthritis": ["sandhivāta", "sandhivata", "संधिवात", "āmavāta", "amavata", 
                  "आमवात", "joint pain"],
    "sandhivata": ["संधिवात", "sandhivāta", "osteoarthritis", "joint disorder"],
    "amavata": ["आमवात", "āmavāta", "rheumatoid arthritis", "āma + vāta"],
    "joint pain": ["sandhiśūla", "sandhishula", "संधिशूल", "sandhivāta"],
    "osteoarthritis": ["sandhivāta", "sandhivata", "संधिवात"],
    "rheumatoid": ["āmavāta", "amavata", "आमवात"],
    
    # GOUT
    "gout": ["vātarakta", "vatarakta", "वातरक्त", "āḍhyavāta"],
    "vatarakta": ["वातरक्त", "vātarakta", "gout", "gouty arthritis"],
    
    # SCIATICA
    "sciatica": ["gṛdhrasī", "gridhrasi", "गृध्रसी"],
    "gridhrasi": ["गृध्रसी", "gṛdhrasī", "sciatica"],
    
    # LUMBAGO
    "lumbago": ["kaṭiśūla", "katishula", "कटिशूल", "kaṭigraha", "low back pain"],
    "low back pain": ["kaṭiśūla", "katishula", "कटिशूल"],
    "katishula": ["कटिशूल", "kaṭiśūla", "lumbago", "back pain"],
    
    # =========================================================================
    # MAJOR DISEASES - NEUROLOGICAL
    # =========================================================================
    
    # PARALYSIS
    "paralysis": ["pakṣāghāta", "pakshaghata", "पक्षाघात", "pakṣavadha"],
    "pakshaghata": ["पक्षाघात", "pakṣāghāta", "paralysis", "hemiplegia"],
    "hemiplegia": ["pakṣāghāta", "pakshaghata", "पक्षाघात"],
    "stroke": ["pakṣāghāta", "pakshaghata", "पक्षाघात"],
    
    # HEADACHE
    "headache": ["śiraḥśūla", "shirahshula", "शिरःशूल", "śiroroga", "shiroroga"],
    "shirahshula": ["शिरःशूल", "śiraḥśūla", "headache", "cephalalgia"],
    
    # MIGRAINE
    "migraine": ["ardhāvabhedaka", "ardhavabhedaka", "अर्धावभेदक", "sūryāvarta"],
    "ardhavabhedaka": ["अर्धावभेदक", "ardhāvabhedaka", "migraine", "half headache"],
    
    # EPILEPSY
    "epilepsy": ["apasmāra", "apasmara", "अपस्मार"],
    "apasmara": ["अपस्मार", "apasmāra", "epilepsy", "seizure"],
    "seizure": ["apasmāra", "apasmara", "अपस्मार", "ākṣepa"],
    
    # INSANITY
    "insanity": ["unmāda", "unmada", "उन्माद", "mental disorder"],
    "unmada": ["उन्माद", "unmāda", "insanity", "psychosis", "mania"],
    "psychosis": ["unmāda", "unmada", "उन्माद"],
    "mania": ["unmāda", "unmada", "उन्माद"],
    
    # =========================================================================
    # MAJOR DISEASES - URINARY
    # =========================================================================
    
    "urinary": ["mūtrakṛcchra", "mutrakrchra", "मूत्रकृच्छ्र", "mūtra roga"],
    "mutrakrichra": ["मूत्रकृच्छ्र", "mūtrakṛcchra", "dysuria", "painful urination"],
    "dysuria": ["mūtrakṛcchra", "mutrakrchra", "मूत्रकृच्छ्र"],
    
    "kidney stone": ["aśmarī", "ashmari", "अश्मरी", "mūtrāśmarī"],
    "ashmari": ["अश्मरी", "aśmarī", "stone", "calculus", "urolithiasis"],
    "stone": ["aśmarī", "ashmari", "अश्मरी"],
    "calculus": ["aśmarī", "ashmari", "अश्मरी"],
    
    # =========================================================================
    # MAJOR DISEASES - CARDIAC
    # =========================================================================
    
    "heart disease": ["hṛdroga", "hridroga", "हृद्रोग", "hṛdaya roga"],
    "hridroga": ["हृद्रोग", "hṛdroga", "heart disease", "cardiac disorder"],
    "cardiac": ["hṛdroga", "hridroga", "हृद्रोग", "hṛdaya"],
    
    # =========================================================================
    # MAJOR DISEASES - BLEEDING DISORDERS
    # =========================================================================
    
    "bleeding": ["raktapitta", "रक्तपित्त", "rakta pitta", "hemorrhage"],
    "raktapitta": ["रक्तपित्त", "bleeding disorder", "hemorrhage", "rakta + pitta"],
    "hemorrhage": ["raktapitta", "रक्तपित्त", "śoṇitasrava"],
    
    # =========================================================================
    # MAJOR DISEASES - ANEMIA
    # =========================================================================
    
    "anemia": ["pāṇḍu", "pandu", "पाण्डु", "pāṇḍuroga"],
    "pandu": ["पाण्डु", "pāṇḍu", "anemia", "pallor", "chlorosis"],
    "pallor": ["pāṇḍu", "pandu", "पाण्डु"],
    
    # =========================================================================
    # MAJOR DISEASES - SWELLING
    # =========================================================================
    
    "swelling": ["śotha", "shotha", "शोथ", "śvayathu", "shvayathu"],
    "shotha": ["शोथ", "śotha", "swelling", "edema", "inflammation"],
    "edema": ["śotha", "shotha", "शोथ", "śvayathu"],
    
    "ascites": ["jalodara", "जलोदर", "udara roga"],
    "jalodara": ["जलोदर", "ascites", "abdominal dropsy"],
    
    # =========================================================================
    # MAJOR DISEASES - ABDOMINAL
    # =========================================================================
    
    "abdominal tumor": ["gulma", "गुल्म", "phantom tumor"],
    "gulma": ["गुल्म", "abdominal mass", "phantom tumor"],
    
    "splenic disorder": ["plīhodara", "plihodara", "प्लीहोदर"],
    "plihodara": ["प्लीहोदर", "plīhodara", "splenomegaly"],
    
    "udara": ["उदर", "abdomen", "abdominal disease"],
    "abdomen": ["udara", "उदर", "koṣṭha", "koshtha"],
    
    # =========================================================================
    # MAJOR DISEASES - EYE
    # =========================================================================
    
    "eye disease": ["netra roga", "नेत्ररोग", "timira", "akṣiroga"],
    "cataract": ["liṅganāśa", "linganasha", "लिङ्गनाश", "timira"],
    "timira": ["तिमिर", "vision defect", "eye disorder"],
    "night blindness": ["rātryandha", "ratryandha", "रात्र्यन्ध"],
    
    # =========================================================================
    # MAJOR DISEASES - ENT
    # =========================================================================
    
    "ear disease": ["karṇaroga", "karnaroga", "कर्णरोग"],
    "deafness": ["bādhirya", "badhirya", "बाधिर्य"],
    
    "throat": ["kaṇṭha", "kantha", "कण्ठ", "gala"],
    "tonsillitis": ["galagaṇḍa", "galaganda", "गलगण्ड"],
    
    # =========================================================================
    # MAJOR DISEASES - REPRODUCTIVE
    # =========================================================================
    
    "infertility": ["vandhyatva", "वन्ध्यत्व", "vandhyā"],
    "vandhyatva": ["वन्ध्यत्व", "infertility", "sterility"],
    
    "impotence": ["klaibya", "क्लैब्य", "napuṃsaka"],
    "klaibya": ["क्लैब्य", "impotence", "erectile dysfunction"],
    
    "menstrual": ["ārtava", "artava", "आर्तव", "raja"],
    "amenorrhea": ["anārtava", "anartava", "अनार्तव"],
    "dysmenorrhea": ["kaṣṭārtava", "kashtartava", "कष्टार्तव"],
    
    "leucorrhea": ["śvetapradara", "shvetapradara", "श्वेतप्रदर", "pradara"],
    "pradara": ["प्रदर", "leucorrhea", "vaginal discharge"],
    
    # =========================================================================
    # MAJOR DISEASES - PEDIATRIC
    # =========================================================================
    
    "pediatric": ["bālaroga", "balaroga", "बालरोग", "kaumārabhṛtya"],
    "balaroga": ["बालरोग", "bālaroga", "pediatric disease", "child disease"],
    
    # =========================================================================
    # MAJOR DISEASES - POISONING
    # =========================================================================
    
    "poison": ["viṣa", "visha", "विष", "gara"],
    "visha": ["विष", "viṣa", "poison", "toxin"],
    "poisoning": ["viṣa", "visha", "विष"],
    "snakebite": ["sarpavisa", "सर्पविष", "sarpadaṃśa"],
    
    # =========================================================================
    # TREATMENT - GENERAL
    # =========================================================================
    
    "treatment": ["cikitsā", "chikitsa", "चिकित्सा", "upakrama", "upacāra", "upachara"],
    "chikitsa": ["चिकित्सा", "cikitsā", "treatment", "therapy", "management"],
    "therapy": ["cikitsā", "chikitsa", "चिकित्सा", "prayoga"],
    "management": ["cikitsā", "chikitsa", "चिकित्सा", "upakrama"],
    
    "medicine": ["auṣadha", "aushadha", "औषध", "bheṣaja", "bheshaja", "भेषज", "dravya"],
    "drug": ["auṣadha", "aushadha", "औषध", "bheṣaja"],
    "remedy": ["auṣadha", "aushadha", "औषध", "bheṣaja"],
    
    "cure": ["cikitsā", "chikitsa", "चिकित्सा", "ārogya"],
    "healing": ["ropana", "रोपण", "cikitsā"],
    
    # =========================================================================
    # TREATMENT - SHODHANA (PURIFICATION)
    # =========================================================================
    
    "purification": ["śodhana", "shodhana", "शोधन"],
    "shodhana": ["शोधन", "śodhana", "purification", "detoxification", "cleansing"],
    "detoxification": ["śodhana", "shodhana", "शोधन"],
    "cleansing": ["śodhana", "shodhana", "शोधन"],
    
    # PANCHAKARMA
    "panchakarma": ["pañcakarma", "पञ्चकर्म", "five procedures", "śodhana"],
    "panchkarma": ["pañcakarma", "पञ्चकर्म", "panchakarma"],
    "five procedures": ["pañcakarma", "पञ्चकर्म"],
    
    # Vamana
    "vamana": ["वमन", "vamanakarma", "emesis", "therapeutic vomiting"],
    "emesis": ["vamana", "वमन", "therapeutic vomiting"],
    "therapeutic vomiting": ["vamana", "वमन"],
    
    # Virechana
    "virechana": ["विरेचन", "virecana", "purgation", "therapeutic purgation"],
    "purgation": ["virechana", "virecana", "विरेचन"],
    
    # Basti
    "basti": ["बस्ति", "vasti", "bastikarma", "enema"],
    "vasti": ["वस्ति", "basti", "enema"],
    "enema": ["basti", "vasti", "बस्ति", "वस्ति"],
    
    # Nasya
    "nasya": ["नस्य", "nāsya", "nasyakarma", "śirovirecana", "nasal therapy"],
    "nasal": ["nasya", "नस्य", "nāsya"],
    "errhine": ["nasya", "नस्य"],
    
    # Raktamokshana
    "raktamokshana": ["रक्तमोक्षण", "raktamokṣaṇa", "bloodletting"],
    "bloodletting": ["raktamokṣaṇa", "raktamokshana", "रक्तमोक्षण"],
    
    # =========================================================================
    # TREATMENT - SHAMANA (PALLIATIVE)
    # =========================================================================
    
    "palliative": ["śamana", "shamana", "शमन"],
    "shamana": ["शमन", "śamana", "palliative", "pacification"],
    
    # =========================================================================
    # TREATMENT - LANGHANA & BRIMHANA
    # =========================================================================
    
    "langhana": ["लङ्घन", "laṅghana", "lightening", "reducing", "fasting", "depletion"],
    "lightening": ["laṅghana", "langhana", "लङ्घन"],
    "reducing": ["laṅghana", "langhana", "लङ्घन", "karśana"],
    "fasting": ["upavāsa", "upavasa", "उपवास", "laṅghana"],
    "weight loss": ["laṅghana", "langhana", "लङ्घन", "karśana", "कर्शन"],
    
    "brimhana": ["बृंहण", "bṛṃhaṇa", "nourishing", "building", "weight gain"],
    "nourishing": ["bṛṃhaṇa", "brimhana", "बृंहण", "santarpaṇa"],
    "building": ["bṛṃhaṇa", "brimhana", "बृंहण"],
    "weight gain": ["bṛṃhaṇa", "brimhana", "बृंहण"],
    
    # =========================================================================
    # TREATMENT - SNEHANA & SWEDANA
    # =========================================================================
    
    "snehana": ["स्नेहन", "sneha", "oleation", "oil therapy"],
    "oleation": ["snehana", "स्नेहन", "sneha"],
    
    "swedana": ["स्वेदन", "sveda", "sudation", "fomentation", "sweating therapy"],
    "fomentation": ["swedana", "स्वेदन", "sveda"],
    "sudation": ["swedana", "स्वेदन"],
    
    "abhyanga": ["अभ्यङ्ग", "abhyaṅga", "mardana", "massage", "oil massage"],
    "massage": ["abhyaṅga", "abhyanga", "अभ्यङ्ग", "mardana"],
    
    # =========================================================================
    # TREATMENT - RASAYANA & VAJIKARANA
    # =========================================================================
    
    "rasayana": ["रसायन", "rasāyana", "rejuvenation", "anti-aging"],
    "rejuvenation": ["rasāyana", "rasayana", "रसायन"],
    "anti-aging": ["rasāyana", "rasayana", "रसायन", "vayasthāpana"],
    "longevity": ["āyus", "ayus", "आयुस्", "dīrghāyus", "rasāyana"],
    
    "vajikarana": ["वाजीकरण", "vājīkaraṇa", "aphrodisiac", "virility"],
    "aphrodisiac": ["vājīkaraṇa", "vajikarana", "वाजीकरण", "vṛṣya"],
    "virility": ["vājīkaraṇa", "vajikarana", "वाजीकरण"],
    
    # =========================================================================
    # OJAS, BALA, IMMUNITY
    # =========================================================================
    
    "ojas": ["ओजस्", "ojah", "vital essence", "immunity"],
    "immunity": ["vyādhikṣamatva", "vyadhikshamatva", "व्याधिक्षमत्व", "bala", "ojas"],
    "strength": ["bala", "बल", "śakti", "shakti"],
    "bala": ["बल", "strength", "immunity", "ojas"],
    
    # =========================================================================
    # DIET & NUTRITION
    # =========================================================================
    
    "diet": ["āhāra", "ahara", "आहार", "anna", "भोजन", "bhojana", "pathya"],
    "food": ["āhāra", "ahara", "आहार", "anna", "अन्न", "bhakṣya"],
    "nutrition": ["āhāra", "ahara", "आहार", "poṣaṇa", "poshana"],
    
    "pathya": ["पथ्य", "wholesome", "suitable diet", "hita"],
    "wholesome": ["pathya", "पथ्य", "hita", "sātmya", "satmya"],
    
    "apathya": ["अपथ्य", "unwholesome", "unsuitable", "ahita"],
    "unwholesome": ["apathya", "अपथ्य", "ahita", "asātmya"],
    
    # =========================================================================
    # TASTES (RASA)
    # =========================================================================
    
    "taste": ["rasa", "रस", "rasam"],
    "sweet": ["madhura", "मधुर"],
    "sour": ["amla", "अम्ल"],
    "salty": ["lavaṇa", "lavana", "लवण"],
    "pungent": ["kaṭu", "katu", "कटु"],
    "bitter": ["tikta", "तिक्त"],
    "astringent": ["kaṣāya", "kashaya", "कषाय"],
    
    # =========================================================================
    # QUALITIES (GUNA)
    # =========================================================================
    
    "quality": ["guṇa", "guna", "गुण", "property"],
    "property": ["guṇa", "guna", "गुण", "dharma"],
    
    "hot": ["uṣṇa", "ushna", "उष्ण"],
    "cold": ["śīta", "shita", "शीत", "hima"],
    "heavy": ["guru", "गुरु"],
    "light": ["laghu", "लघु"],
    "oily": ["snigdha", "स्निग्ध", "sneha"],
    "dry": ["rūkṣa", "ruksha", "रूक्ष"],
    "sharp": ["tīkṣṇa", "tikshna", "तीक्ष्ण"],
    "dull": ["manda", "मन्द"],
    
    # =========================================================================
    # ETIOLOGY & DIAGNOSIS
    # =========================================================================
    
    "cause": ["hetu", "हेतु", "nidāna", "nidana", "निदान", "kāraṇa", "karana"],
    "etiology": ["nidāna", "nidana", "निदान", "hetu"],
    "nidana": ["निदान", "nidāna", "cause", "etiology"],
    
    "pathogenesis": ["saṃprāpti", "samprapti", "सम्प्राप्ति"],
    "samprapti": ["सम्प्राप्ति", "saṃprāpti", "pathogenesis", "disease process"],
    
    "symptom": ["lakṣaṇa", "lakshana", "लक्षण", "liṅga", "linga", "rūpa", "rupa"],
    "sign": ["lakṣaṇa", "lakshana", "लक्षण", "cihna", "chihna"],
    "lakshana": ["लक्षण", "lakṣaṇa", "symptom", "sign", "characteristic"],
    
    "prognosis": ["sādhyāsādhyatā", "sadhyasadhyata", "upadrava"],
    "curable": ["sādhya", "sadhya", "साध्य"],
    "incurable": ["asādhya", "asadhya", "असाध्य"],
    
    "diagnosis": ["parīkṣā", "pariksha", "परीक्षा", "nidāna"],
    "examination": ["parīkṣā", "pariksha", "परीक्षा"],
    
    # =========================================================================
    # BODY PARTS
    # =========================================================================
    
    "body": ["śarīra", "sharira", "शरीर", "deha", "देह", "kāya", "kaya"],
    "mind": ["manas", "मनस्", "citta", "chitta", "चित्त"],
    "soul": ["ātmā", "atma", "आत्मा", "jīva", "jiva"],
    
    "head": ["śiras", "shiras", "शिरस्", "mastaka", "मस्तक"],
    "heart": ["hṛdaya", "hrdaya", "hridaya", "हृदय"],
    "stomach": ["āmāśaya", "amashaya", "आमाशय", "udara"],
    "liver": ["yakṛt", "yakrt", "यकृत्"],
    "spleen": ["plīhā", "pliha", "प्लीहा"],
    "kidney": ["vṛkka", "vrkka", "वृक्क"],
    "lung": ["phupphusa", "फुप्फुस", "kloma"],
    "joint": ["sandhi", "संधि"],
    
    # =========================================================================
    # HERBS - COMMON
    # =========================================================================
    
    "ashwagandha": ["aśvagandha", "aśvagandhā", "अश्वगन्धा"],
    "brahmi": ["brāhmī", "ब्राह्मी"],
    "tulsi": ["tulasī", "tulasi", "तुलसी"],
    "neem": ["nimba", "निम्ब"],
    "turmeric": ["haridrā", "haridra", "हरिद्रा"],
    "ginger": ["śuṇṭhī", "shunthi", "शुण्ठी", "ārdraka", "ardraka", "आर्द्रक"],
    "pepper": ["marica", "maricha", "मरिच"],
    
    "triphala": ["त्रिफला", "triphalā", "three fruits"],
    "amalaki": ["आमलकी", "āmalakī", "amalaki", "dhātrī"],
    "haritaki": ["हरीतकी", "harītakī", "haritaki"],
    "bibhitaki": ["बिभीतकी", "bibhītakī", "bibhitaki"],
    
    "guduchi": ["गुडूची", "guḍūcī", "giloy", "amrita"],
    "shatavari": ["शतावरी", "śatāvarī"],
    "pippali": ["पिप्पली", "pippalī", "long pepper"],
    
    # =========================================================================
    # PHYSICIAN & PATIENT
    # =========================================================================
    
    "physician": ["vaidya", "वैद्य", "bhiṣak", "bhishak", "भिषक्", "cikitsaka"],
    "doctor": ["vaidya", "वैद्य", "bhiṣak"],
    "patient": ["rogī", "rogi", "रोगी", "ātura", "atura", "आतुर"],
    
    # =========================================================================
    # TIME & SEASONS
    # =========================================================================
    
    "season": ["ṛtu", "rtu", "ritu", "ऋतु"],
    "daily routine": ["dinacaryā", "dinacharya", "दिनचर्या"],
    "seasonal routine": ["ṛtucaryā", "ritucharya", "ऋतुचर्या"],
    
    # =========================================================================
    # MISCELLANEOUS
    # =========================================================================
    
    "life": ["āyu", "ayu", "आयु", "āyus", "jīvana", "prāṇa", "prana"],
    "death": ["mṛtyu", "mrtyu", "मृत्यु", "maraṇa"],
    "sleep": ["nidrā", "nidra", "निद्रा", "svapna"],
    "exercise": ["vyāyāma", "vyayama", "व्यायाम"],
}


# =============================================================================
# MODERN TERM TO CLASSICAL MAPPING
# =============================================================================

MODERN_TO_CLASSICAL = {
    "obesity": {
        "suggestions": ["sthaulya", "स्थौल्य", "medoroga", "मेदोरोग", "meda"],
        "disclaimer": "Search for 'Sthaulya' or 'Medoroga' for classical obesity references."
    },
    "diabetes": {
        "suggestions": ["prameha", "प्रमेह", "madhumeha", "मधुमेह"],
        "disclaimer": "Search for 'Prameha' or 'Madhumeha' for classical diabetes references."
    },
    "hypertension": {
        "suggestions": ["raktacāpa", "ucca rakta", "vyana vata", "rakta dhatu"],
        "disclaimer": "Blood pressure is a modern concept. Related concepts include Rakta Dhatu and Vyana Vata."
    },
    "cholesterol": {
        "suggestions": ["meda dhatu", "medoroga", "sthaulya", "āma"],
        "disclaimer": "Cholesterol is modern. Related concepts include Meda Dhatu and Medoroga."
    },
    "calcium": {
        "suggestions": ["asthi dhatu", "asthi", "kshira", "dugdha"],
        "disclaimer": "Mineral chemistry is modern. Related concept is Asthi Dhatu (bone tissue)."
    },
    "protein": {
        "suggestions": ["mamsa dhatu", "mamsa", "bala", "poshana"],
        "disclaimer": "Macronutrients are modern. Related concept is Mamsa Dhatu (muscle tissue)."
    },
    "vitamin": {
        "suggestions": ["rasayana", "ojas", "bala", "poshana"],
        "disclaimer": "Vitamins are modern. Related concepts include Rasayana and Ojas."
    },
    "antibiotic": {
        "suggestions": ["krimighna", "jantughna", "vishghna"],
        "disclaimer": "Antibiotics are modern. Related concept is Krimighna (anti-parasitic)."
    },
    "inflammation": {
        "suggestions": ["shotha", "daha", "pitta prakopa", "vidaha"],
        "disclaimer": "Related concepts include Shotha (swelling) and Daha (burning)."
    },
    "cancer": {
        "suggestions": ["arbuda", "granthi", "gulma", "dushta vrana"],
        "disclaimer": "Modern oncology differs. Related concepts include Arbuda and Granthi."
    },
    "tumor": {
        "suggestions": ["arbuda", "granthi", "gulma"],
        "disclaimer": "Related concepts include Arbuda (tumor) and Granthi (cyst/growth)."
    },
    "allergy": {
        "suggestions": ["asatmya", "viruddha ahara", "pratiloma"],
        "disclaimer": "Related concept is Asatmya (incompatibility)."
    },
    "depression": {
        "suggestions": ["vishada", "manasa roga", "unmada", "avasada"],
        "disclaimer": "Related concepts include Vishada (dejection) and Manasa Roga."
    },
    "anxiety": {
        "suggestions": ["chittodvega", "bhaya", "manasa vikara", "vata prakopa"],
        "disclaimer": "Related concepts include Chittodvega and Vata Prakopa."
    },
    "stress": {
        "suggestions": ["manasa ayasa", "shrama", "kshaya"],
        "disclaimer": "Related concepts include Manasa Ayasa (mental exertion) and Shrama."
    },
    "migraine": {
        "suggestions": ["ardhavabhedaka", "shirahshula", "suryavarta"],
        "disclaimer": "Ardhavabhedaka is the classical condition resembling migraine."
    },
    "acidity": {
        "suggestions": ["amlapitta", "vidagdha", "pitta prakopa"],
        "disclaimer": "Amlapitta is the classical acid-related disorder."
    },
}


# =============================================================================
# SPELLING CORRECTIONS
# =============================================================================

SPELLING_CORRECTIONS = {
    # Dosha
    "vaat": "vāta",
    "vat": "vāta",
    "vaata": "vāta",
    "pitha": "pitta",
    "pita": "pitta",
    "kaff": "kapha",
    "kafa": "kapha",
    "kaf": "kapha",
    "dosh": "doṣa",
    "dosha": "doṣa",
    
    # Dhatu
    "dhaat": "dhātu",
    "dhat": "dhātu",
    
    # Agni
    "agini": "agni",
    "aam": "āma",
    
    # Health
    "swasthya": "svāsthya",
    "swasth": "svastha",
    "arogya": "ārogya",
    
    # Ayurveda
    "ayurved": "āyurveda",
    "ayurvaid": "āyurveda",
    
    # Panchakarma
    "pachakarma": "pañcakarma",
    "panchkarma": "pañcakarma",
    
    # Diseases
    "staulya": "sthaulya",
    "medaroga": "medoroga",
    "jwara": "jvara",
    "jwar": "jvara",
    "kushth": "kuṣṭha",
    "kushtha": "kuṣṭha",
    "prameh": "prameha",
    
    # Treatment
    "rasayan": "rasāyana",
    "vajikaran": "vājīkaraṇa",
    "virechan": "virecana",
    "vaman": "vamana",
    "langhan": "laṅghana",
    "brimhan": "bṛṃhaṇa",
    
    # Others
    "oja": "ojas",
    "ojus": "ojas",
    "srota": "srotas",
    "nidan": "nidāna",
    "chikitsa": "cikitsā",
    "aushadh": "auṣadha",
}


# =============================================================================
# FAMOUS SLOKAS KEYWORDS
# =============================================================================

FAMOUS_SLOKAS_KEYWORDS = {
    "health definition": ["समदोष", "samadoṣa", "स्वस्थ", "svastha", "समाग्नि", "prasanna"],
    "swastha definition": ["समदोष", "samadoṣa", "समाग्नि", "प्रसन्न", "prasanna"],
    "purpose of ayurveda": ["प्रयोजन", "prayojana", "स्वस्थस्य", "रक्षण", "आतुरस्य"],
    "definition of ayurveda": ["हिताहित", "hitāhita", "सुख", "दुःख", "आयु"],
    "physician qualities": ["भिषक्", "bhiṣak", "वैद्य", "चतुष्पाद", "प्राणाभिसर"],
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_synonyms(term: str) -> list:
    """Get synonyms for a given term"""
    term_lower = term.lower()
    return AYURVEDIC_SYNONYMS.get(term_lower, [])


def check_modern_term(term: str) -> dict:
    """Check if term is a modern concept and return suggestions"""
    term_lower = term.lower()
    return MODERN_TO_CLASSICAL.get(term_lower, None)


def check_spelling(term: str) -> str:
    """Check if term needs spelling correction"""
    term_lower = term.lower()
    return SPELLING_CORRECTIONS.get(term_lower, None)


def get_famous_keywords(query: str) -> list:
    """Get keywords for famous slokas based on query"""
    query_lower = query.lower()
    keywords = []
    for concept, kws in FAMOUS_SLOKAS_KEYWORDS.items():
        if any(word in query_lower for word in concept.split()):
            keywords.extend(kws)
    return list(set(keywords))
