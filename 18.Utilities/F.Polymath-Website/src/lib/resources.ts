// Curated study resources — standard textbooks (titles + authors are facts,
// not reproduced content) and reputable FREE video-lecture sources. Links point
// to stable official homepages/channels to avoid rot. Edit freely.

export interface Book { title: string; author: string; note?: string }
export interface Lecture { title: string; source: string; url: string }
export interface ExamResources { slug: string; books: Book[]; lectures: Lecture[] }

export const RESOURCES: ExamResources[] = [
  {
    slug: "iit-jee",
    books: [
      { title: "Concepts of Physics (Vol. 1 & 2)", author: "H. C. Verma", note: "The gold standard for JEE physics intuition." },
      { title: "Understanding Physics series", author: "D. C. Pandey", note: "Topic-wise practice with graded problems." },
      { title: "Problems in General Physics", author: "I. E. Irodov", note: "Advanced — for JEE Advanced depth." },
      { title: "NCERT Chemistry (Class XI–XII)", author: "NCERT", note: "Non-negotiable base, especially inorganic." },
      { title: "Concise Inorganic Chemistry", author: "J. D. Lee", note: "Reference for inorganic." },
      { title: "Mathematics series", author: "Cengage (G. Tewani)", note: "Theory + problems, well-paced." },
      { title: "Trigonometry & Coordinate Geometry", author: "S. L. Loney", note: "Classics for the fundamentals." },
    ],
    lectures: [
      { title: "Physics, Chemistry & Maths (free MOOCs)", source: "NPTEL / SWAYAM", url: "https://nptel.ac.in" },
      { title: "Math & science foundations", source: "Khan Academy", url: "https://www.khanacademy.org" },
      { title: "Visual math intuition", source: "3Blue1Brown", url: "https://www.youtube.com/@3blue1brown" },
    ],
  },
  {
    slug: "neet",
    books: [
      { title: "Biology, Physics & Chemistry (Class XI–XII)", author: "NCERT", note: "The single most important source for NEET." },
      { title: "Elementary Biology (Vol. 1 & 2)", author: "Trueman", note: "Popular NCERT companion for biology." },
      { title: "Concepts of Physics", author: "H. C. Verma", note: "Physics clarity for medical aspirants." },
      { title: "Objective Chemistry", author: "MTG / NCERT at Fingertips", note: "MCQ practice aligned to NCERT." },
    ],
    lectures: [
      { title: "Biology, Physics, Chemistry MOOCs", source: "NPTEL / SWAYAM", url: "https://nptel.ac.in" },
      { title: "Biology & chemistry foundations", source: "Khan Academy", url: "https://www.khanacademy.org" },
      { title: "Official NCERT e-content", source: "NCERT", url: "https://ncert.nic.in" },
    ],
  },
  {
    slug: "gate",
    books: [
      { title: "Introduction to Algorithms (CLRS)", author: "Cormen, Leiserson, Rivest, Stein", note: "The definitive algorithms reference." },
      { title: "Operating System Concepts", author: "Silberschatz, Galvin, Gagne", note: "The 'dinosaur book' — OS standard." },
      { title: "Computer Networking: A Top-Down Approach", author: "Kurose & Ross", note: "Clear, intuition-first networks." },
      { title: "Database System Concepts", author: "Silberschatz, Korth, Sudarshan", note: "Core DBMS theory." },
      { title: "Introduction to Automata Theory", author: "Hopcroft, Motwani, Ullman", note: "Theory of computation." },
      { title: "Discrete Mathematics and Its Applications", author: "Kenneth Rosen", note: "Engineering maths foundation." },
    ],
    lectures: [
      { title: "GATE CS/EE/ME courses (free)", source: "NPTEL / SWAYAM", url: "https://nptel.ac.in" },
      { title: "CS subject explainers", source: "Gate Smashers", url: "https://www.youtube.com/@GateSmashers" },
      { title: "Core electronics & CS", source: "Neso Academy", url: "https://www.youtube.com/@nesoacademy" },
    ],
  },
  {
    slug: "isi-cmi",
    books: [
      { title: "Challenge and Thrill of Pre-College Mathematics", author: "V. Krishnamurthy et al.", note: "Olympiad-style depth for ISI/CMI." },
      { title: "Higher Algebra", author: "Hall & Knight", note: "Classic algebra problem set." },
      { title: "Problem-Solving Strategies", author: "Arthur Engel", note: "Build genuine problem-solving skill." },
      { title: "Test of Mathematics at the 10+2 Level", author: "ISI", note: "Closest to the actual ISI exam style." },
    ],
    lectures: [
      { title: "University-level mathematics", source: "MIT OpenCourseWare", url: "https://ocw.mit.edu" },
      { title: "Mathematics MOOCs", source: "NPTEL / SWAYAM", url: "https://nptel.ac.in" },
      { title: "Deep math intuition", source: "3Blue1Brown", url: "https://www.youtube.com/@3blue1brown" },
    ],
  },
  {
    slug: "cat",
    books: [
      { title: "How to Prepare for Quantitative Aptitude", author: "Arun Sharma", note: "Standard for QA, level-graded (LOD 1–3)." },
      { title: "How to Prepare for Data Interpretation & Logical Reasoning", author: "Arun Sharma", note: "DILR practice." },
      { title: "Word Power Made Easy", author: "Norman Lewis", note: "Vocabulary base for VARC." },
      { title: "Quantum CAT", author: "Sarvesh K. Verma", note: "Concept + shortcut heavy QA." },
    ],
    lectures: [
      { title: "CAT quant & DILR (free)", source: "2IIM (YouTube)", url: "https://www.youtube.com/@2IIMonline" },
      { title: "Math fundamentals refresh", source: "Khan Academy", url: "https://www.khanacademy.org" },
      { title: "Official CAT sample material", source: "IIM CAT", url: "https://iimcat.ac.in" },
    ],
  },
  {
    slug: "upsc",
    books: [
      { title: "NCERT textbooks (Class VI–XII)", author: "NCERT", note: "Foundation for every GS subject." },
      { title: "Indian Polity", author: "M. Laxmikanth", note: "The polity standard." },
      { title: "A Brief History of Modern India", author: "Spectrum", note: "Concise modern history." },
      { title: "Indian Economy", author: "Ramesh Singh", note: "Comprehensive economy reference." },
      { title: "Certificate Physical and Human Geography", author: "G. C. Leong", note: "Geography fundamentals." },
    ],
    lectures: [
      { title: "Foundation & optional courses", source: "NPTEL / SWAYAM", url: "https://swayam.gov.in" },
      { title: "Official current-affairs magazines", source: "Yojana / PIB", url: "https://www.pib.gov.in" },
      { title: "NCERT e-content", source: "NCERT", url: "https://ncert.nic.in" },
    ],
  },
];

export const PLATFORMS: Lecture[] = [
  { title: "1000+ free university courses (India)", source: "NPTEL", url: "https://nptel.ac.in" },
  { title: "Free MIT course materials", source: "MIT OpenCourseWare", url: "https://ocw.mit.edu" },
  { title: "Free lessons, math to science", source: "Khan Academy", url: "https://www.khanacademy.org" },
  { title: "Government MOOC platform", source: "SWAYAM", url: "https://swayam.gov.in" },
  { title: "Beautiful visual mathematics", source: "3Blue1Brown", url: "https://www.youtube.com/@3blue1brown" },
  { title: "Official school textbooks (free PDF)", source: "NCERT", url: "https://ncert.nic.in" },
];

export const resourcesFor = (slug: string) => RESOURCES.find((r) => r.slug === slug);
