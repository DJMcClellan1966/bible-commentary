"""
Configuration settings for the Bible Commentary Agent
"""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bible_commentaries.db")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Web Scraping
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

# Commentary Sources Configuration
COMMENTARY_SOURCES = {
    "church_fathers": [
        "https://www.newadvent.org/fathers/",
        "https://www.ccel.org/fathers.html",
    ],
    "middle_ages": [
        "https://www.ccel.org/",
    ],
    "modern": [
        "https://biblehub.com/commentaries/",
        "https://www.biblestudytools.com/commentaries/",
    ],
    "jewish": [
        "https://www.sefaria.org/",
        "https://www.chabad.org/library/",
    ],
    "popes": [
        "https://www.vatican.va/",
    ],
}

# Bible Books (66 books from Genesis to Revelation)
BIBLE_BOOKS = [
    # Old Testament
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    # New Testament
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"
]

# Agent Settings
AGENT_TEMPERATURE = 0.7
MAX_TOKENS = 2000
ENABLE_WEB_SEARCH = True
ENABLE_LEARNING = True
