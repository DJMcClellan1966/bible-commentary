"""
Monthly Themes - Life themes woven through the yearly reading plan

Each month has a theme that connects Scripture to your daily life.
The readings are chronological, but the theme helps you see how
the passages speak to that aspect of human experience.
"""

from dataclasses import dataclass
from typing import List, Dict
from datetime import date


@dataclass
class MonthlyTheme:
    """A theme for a month of reading"""
    month: int
    name: str
    description: str
    key_concepts: List[str]
    reflection_questions: List[str]
    key_verses: List[str]


MONTHLY_THEMES: Dict[int, MonthlyTheme] = {
    1: MonthlyTheme(
        month=1,
        name="Beginnings",
        description=(
            "January marks new beginnings - in the calendar and in Scripture. "
            "We start with Creation, the call of Abraham, and the birth of Israel. "
            "What is God beginning in your life?"
        ),
        key_concepts=["creation", "calling", "promise", "covenant", "new starts"],
        reflection_questions=[
            "What is God creating or recreating in your life right now?",
            "Like Abraham, where is God calling you to go in faith?",
            "What promises from God are you standing on?",
            "How does knowing God is the God of beginnings give you hope?"
        ],
        key_verses=[
            "Genesis 1:1 - In the beginning God created",
            "Genesis 12:1-3 - The call of Abraham",
            "Isaiah 43:19 - Behold, I am doing a new thing",
            "2 Corinthians 5:17 - New creation in Christ"
        ]
    ),
    
    2: MonthlyTheme(
        month=2,
        name="Love and Covenant",
        description=(
            "February's theme of love runs deep in Scripture - not sentimentality, "
            "but covenant faithfulness. God's hesed (steadfast love) binds Him to us. "
            "Marriage, family, and divine romance fill these pages."
        ),
        key_concepts=["love", "covenant", "faithfulness", "marriage", "commitment"],
        reflection_questions=[
            "How have you experienced God's steadfast love?",
            "What covenants (commitments) are you called to keep?",
            "How does Christ's love for the Church shape your relationships?",
            "Where is God calling you to deeper faithfulness?"
        ],
        key_verses=[
            "Deuteronomy 6:5 - Love the Lord your God",
            "Hosea 2:19-20 - I will betroth you to me forever",
            "1 Corinthians 13:4-7 - Love is patient, love is kind",
            "Ephesians 5:25 - Christ loved the Church"
        ]
    ),
    
    3: MonthlyTheme(
        month=3,
        name="Wilderness and Testing",
        description=(
            "Aligned with Lent, March takes us through wilderness experiences. "
            "Israel wandered 40 years; Jesus was tempted 40 days. "
            "These are not detours but formation. What wilderness are you in?"
        ),
        key_concepts=["testing", "wilderness", "temptation", "perseverance", "formation"],
        reflection_questions=[
            "What wilderness season are you walking through?",
            "How is God using this difficulty to form you?",
            "What temptations do you face, and how does Scripture help?",
            "Can you trust God's provision even when you don't see it?"
        ],
        key_verses=[
            "Deuteronomy 8:2-3 - He humbled you in the wilderness",
            "Matthew 4:1-11 - Jesus tempted in the wilderness",
            "James 1:2-4 - Testing produces perseverance",
            "Isaiah 43:2 - When you pass through the waters"
        ]
    ),
    
    4: MonthlyTheme(
        month=4,
        name="Redemption and New Life",
        description=(
            "April brings Easter - the heart of our faith. From Passover to Resurrection, "
            "from slavery to freedom, from death to life. This is the central story "
            "of Scripture and of your life."
        ),
        key_concepts=["redemption", "resurrection", "freedom", "new life", "victory"],
        reflection_questions=[
            "From what has Christ redeemed you?",
            "How does the Resurrection change how you face death?",
            "What needs to 'die' in your life so new life can emerge?",
            "How are you living as one who has been set free?"
        ],
        key_verses=[
            "Exodus 12:13 - The blood shall be a sign for you",
            "Isaiah 53:5 - By his wounds we are healed",
            "Romans 6:4 - Walk in newness of life",
            "1 Corinthians 15:55 - O death, where is your sting?"
        ]
    ),
    
    5: MonthlyTheme(
        month=5,
        name="Law and Wisdom",
        description=(
            "May explores Torah and Wisdom literature. God's law is not burden but gift - "
            "showing us how to live well. Proverbs, Ecclesiastes, and the Psalms teach us "
            "the art of living under God."
        ),
        key_concepts=["law", "wisdom", "guidance", "right living", "discernment"],
        reflection_questions=[
            "How do you view God's commands - as burden or gift?",
            "Where do you need wisdom in your life right now?",
            "What does it mean to 'fear the Lord' in your daily decisions?",
            "How can you meditate on Scripture day and night?"
        ],
        key_verses=[
            "Psalm 1:2 - His delight is in the law of the Lord",
            "Psalm 119:105 - Your word is a lamp to my feet",
            "Proverbs 1:7 - The fear of the Lord is the beginning of wisdom",
            "James 1:5 - If any lacks wisdom, let him ask"
        ]
    ),
    
    6: MonthlyTheme(
        month=6,
        name="Prophetic Voice",
        description=(
            "June amplifies the prophets - those who spoke God's truth to power. "
            "They called for justice, warned of judgment, and promised hope. "
            "What is God's prophetic word to our time?"
        ),
        key_concepts=["prophecy", "justice", "truth-telling", "hope", "correction"],
        reflection_questions=[
            "What injustice breaks your heart as it breaks God's?",
            "When is God calling you to speak uncomfortable truth?",
            "How do the prophets help you understand current events?",
            "What prophetic hope do you cling to?"
        ],
        key_verses=[
            "Micah 6:8 - Do justice, love mercy, walk humbly",
            "Isaiah 61:1 - Good news to the poor",
            "Amos 5:24 - Let justice roll down like waters",
            "Jeremiah 29:11 - Plans for welfare and not for evil"
        ]
    ),
    
    7: MonthlyTheme(
        month=7,
        name="Kingdom and Power",
        description=(
            "July explores kingship - from Israel's judges to David's throne to "
            "Christ's eternal reign. Human power corrupts; God's kingdom endures. "
            "How do we live as citizens of an upside-down kingdom?"
        ),
        key_concepts=["kingdom", "authority", "power", "leadership", "service"],
        reflection_questions=[
            "How does Christ's model of servant-leadership challenge you?",
            "Where are you tempted to grasp for power?",
            "What does it mean that God's kingdom is 'not of this world'?",
            "How can you pray 'Your kingdom come' with your life?"
        ],
        key_verses=[
            "1 Samuel 8:7 - They have rejected me as their king",
            "2 Samuel 7:16 - Your throne shall be established forever",
            "Mark 10:43 - Whoever would be great must be servant",
            "Revelation 11:15 - The kingdom of the world has become the kingdom of our Lord"
        ]
    ),
    
    8: MonthlyTheme(
        month=8,
        name="Exile and Return",
        description=(
            "August walks through exile - the devastating loss of everything. "
            "Yet in Babylon, faith deepened. And return came. "
            "What exiles have you known, and how has God met you there?"
        ),
        key_concepts=["exile", "loss", "longing", "return", "restoration"],
        reflection_questions=[
            "What have you lost that you still grieve?",
            "How can you 'seek the welfare of the city' where you're planted?",
            "What restoration are you hoping for?",
            "How has God met you in your own 'Babylon'?"
        ],
        key_verses=[
            "Psalm 137:1 - By the waters of Babylon we wept",
            "Jeremiah 29:7 - Seek the welfare of the city",
            "Isaiah 40:1 - Comfort, comfort my people",
            "Ezra 1:1 - The Lord stirred up the spirit of Cyrus"
        ]
    ),
    
    9: MonthlyTheme(
        month=9,
        name="Work and Calling",
        description=(
            "September, with its back-to-school and work rhythms, explores vocation. "
            "God calls us not just to 'religious' work but to serve Him in all we do. "
            "Your work matters to God."
        ),
        key_concepts=["vocation", "calling", "work", "purpose", "service"],
        reflection_questions=[
            "How do you see your work as service to God?",
            "What unique contribution are you called to make?",
            "How can you do your work 'as unto the Lord'?",
            "Where is God calling you to serve in this season?"
        ],
        key_verses=[
            "Genesis 2:15 - The Lord put him in the garden to work it",
            "Colossians 3:23 - Whatever you do, work heartily, as for the Lord",
            "Ephesians 2:10 - Created for good works",
            "Ecclesiastes 2:24 - Nothing better than to enjoy his work"
        ]
    ),
    
    10: MonthlyTheme(
        month=10,
        name="Community and Church",
        description=(
            "October focuses on the people of God - from Israel to the early Church. "
            "Faith is not solo but communal. We need each other. "
            "How is your life intertwined with God's people?"
        ),
        key_concepts=["community", "church", "fellowship", "unity", "one body"],
        reflection_questions=[
            "Why do you need the Church, and why does she need you?",
            "How are you using your gifts to build up the body?",
            "Where is division that needs healing?",
            "What does it mean to 'bear one another's burdens'?"
        ],
        key_verses=[
            "Acts 2:42-47 - They devoted themselves to fellowship",
            "1 Corinthians 12:12 - One body, many members",
            "Hebrews 10:25 - Not neglecting to meet together",
            "Galatians 6:2 - Bear one another's burdens"
        ]
    ),
    
    11: MonthlyTheme(
        month=11,
        name="Gratitude and Provision",
        description=(
            "November, with Thanksgiving, turns our hearts to gratitude. "
            "Scripture overflows with praise for God's provision - manna, harvest, "
            "daily bread. What has God provided that you've overlooked?"
        ),
        key_concepts=["gratitude", "provision", "thanksgiving", "contentment", "trust"],
        reflection_questions=[
            "What are you most grateful for right now?",
            "Where has God provided when you thought there was no way?",
            "How can you cultivate a thankful heart daily?",
            "What would change if you truly believed God would provide?"
        ],
        key_verses=[
            "Psalm 100:4 - Enter his gates with thanksgiving",
            "Philippians 4:6-7 - With thanksgiving let your requests be made known",
            "Matthew 6:11 - Give us this day our daily bread",
            "1 Thessalonians 5:18 - Give thanks in all circumstances"
        ]
    ),
    
    12: MonthlyTheme(
        month=12,
        name="Promise and Fulfillment",
        description=(
            "December, with Advent, looks backward and forward. "
            "All the promises point to Christ's coming - first in humility, "
            "then in glory. We live between fulfillment and consummation."
        ),
        key_concepts=["promise", "fulfillment", "hope", "waiting", "coming"],
        reflection_questions=[
            "What promises are you waiting for God to fulfill?",
            "How does Christ's first coming assure you of His return?",
            "What does it mean to live in 'Advent' mode - expectant waiting?",
            "How does the hope of His coming shape how you live today?"
        ],
        key_verses=[
            "Isaiah 9:6 - For to us a child is born",
            "Micah 5:2 - From you shall come forth a ruler",
            "Luke 2:10-11 - Good news of great joy",
            "Revelation 22:20 - Come, Lord Jesus!"
        ]
    )
}


def get_theme_for_date(d: date = None) -> MonthlyTheme:
    """Get the theme for a given date (defaults to today)"""
    if d is None:
        d = date.today()
    return MONTHLY_THEMES[d.month]


def get_theme_reflection(month: int) -> str:
    """Get a formatted reflection for a month's theme"""
    theme = MONTHLY_THEMES[month]
    
    lines = [
        f"{'=' * 60}",
        f"MONTHLY THEME: {theme.name.upper()}",
        f"{'=' * 60}",
        "",
        theme.description,
        "",
        "KEY CONCEPTS:",
        "  " + ", ".join(theme.key_concepts),
        "",
        "REFLECTION QUESTIONS:"
    ]
    
    for i, q in enumerate(theme.reflection_questions, 1):
        lines.append(f"  {i}. {q}")
    
    lines.append("")
    lines.append("KEY VERSES:")
    for v in theme.key_verses:
        lines.append(f"  - {v}")
    
    lines.append(f"{'=' * 60}")
    
    return '\n'.join(lines)
