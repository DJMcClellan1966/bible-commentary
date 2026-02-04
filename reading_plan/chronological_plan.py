"""
Chronological Reading Plan - 365 Days Through Salvation History

This plan takes you through the Bible in roughly chronological order,
following the story of salvation from Creation to New Creation.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import date, timedelta
import json
import os


@dataclass
class ReadingDay:
    """A single day's reading"""
    day_number: int  # 1-365
    date: Optional[date]
    passages: List[str]  # e.g., ["Genesis 1-2", "Psalm 104"]
    title: str
    summary: str
    salvation_history_context: str  # Where this fits in the big story
    key_verse: str
    connection_to_christ: str  # How this points to/reveals Christ


# The chronological reading plan organized by salvation history periods
SALVATION_HISTORY_PERIODS = {
    "creation_fall": {
        "name": "Creation and Fall",
        "days": (1, 7),
        "description": "God creates all things good; humanity falls into sin; the promise of redemption is given."
    },
    "patriarchs": {
        "name": "The Patriarchs",
        "days": (8, 35),
        "description": "God calls Abraham and establishes His covenant with the fathers of Israel."
    },
    "exodus_wilderness": {
        "name": "Exodus and Wilderness",
        "days": (36, 75),
        "description": "God delivers Israel from Egypt, gives the Law, and leads them through the wilderness."
    },
    "conquest_judges": {
        "name": "Conquest and Judges",
        "days": (76, 100),
        "description": "Israel enters the Promised Land and cycles through rebellion and deliverance."
    },
    "united_kingdom": {
        "name": "United Kingdom",
        "days": (101, 140),
        "description": "Samuel, Saul, David, and Solomon - Israel becomes a kingdom."
    },
    "divided_kingdom": {
        "name": "Divided Kingdom",
        "days": (141, 200),
        "description": "The kingdom splits; prophets call for repentance; exile looms."
    },
    "exile_return": {
        "name": "Exile and Return",
        "days": (201, 235),
        "description": "Babylon destroys Jerusalem; the remnant returns and rebuilds."
    },
    "intertestamental_wisdom": {
        "name": "Wisdom Literature",
        "days": (236, 265),
        "description": "Job, Psalms, Proverbs, Ecclesiastes, Song - the heights and depths of life with God."
    },
    "life_of_christ": {
        "name": "The Life of Christ",
        "days": (266, 320),
        "description": "God becomes flesh; Jesus teaches, heals, dies, and rises again."
    },
    "early_church": {
        "name": "The Early Church",
        "days": (321, 350),
        "description": "The Spirit comes; the Church spreads; the apostles teach."
    },
    "consummation": {
        "name": "Consummation",
        "days": (351, 365),
        "description": "Letters of hope, the vision of Revelation, and the promise of Christ's return."
    }
}


# Complete 365-day reading plan
READING_PLAN: List[ReadingDay] = [
    # CREATION AND FALL (Days 1-7)
    ReadingDay(1, None, ["Genesis 1:1-2:3"], "In the Beginning", 
               "God creates the heavens and the earth - all things good.",
               "Creation establishes God as the sovereign Creator and humanity as His image-bearers.",
               "Genesis 1:1 - In the beginning God created the heaven and the earth.",
               "John 1:1-3 reveals Christ was present at creation - 'All things were made through him.'"),
    
    ReadingDay(2, None, ["Genesis 2:4-25"], "The Garden",
               "God creates Adam and Eve, places them in Eden, and establishes marriage.",
               "Humanity is given purpose (work) and relationship (marriage) in the presence of God.",
               "Genesis 2:18 - It is not good that the man should be alone.",
               "Christ is the Second Adam, and the Church is His bride (Ephesians 5:31-32)."),
    
    ReadingDay(3, None, ["Genesis 3:1-24"], "The Fall",
               "The serpent tempts; humanity falls; death enters; promise is given.",
               "Sin breaks relationship with God, but immediately God promises redemption.",
               "Genesis 3:15 - He shall bruise your head, and you shall bruise his heel.",
               "This is the Protoevangelium - the first gospel. Christ is the seed who crushes the serpent."),
    
    ReadingDay(4, None, ["Genesis 4:1-26"], "Cain and Abel",
               "The first murder; sin spreads; yet worship continues.",
               "Sin's effects spread immediately, yet a line of worship persists.",
               "Genesis 4:26 - Then men began to call upon the name of the Lord.",
               "Abel's blood cries from the ground; Christ's blood speaks a better word (Hebrews 12:24)."),
    
    ReadingDay(5, None, ["Genesis 5:1-32", "Genesis 6:1-8"], "Generations of Adam",
               "The genealogy from Adam to Noah; humanity's corruption grows.",
               "Even as sin spreads, God preserves a line through which redemption will come.",
               "Genesis 5:24 - Enoch walked with God, and he was not, for God took him.",
               "Through this line, Christ will eventually come (Luke 3:36-38)."),
    
    ReadingDay(6, None, ["Genesis 6:9-7:24"], "The Flood",
               "God judges the earth but saves Noah and his family through the ark.",
               "Judgment and salvation appear together - a pattern repeated throughout Scripture.",
               "Genesis 6:8 - But Noah found grace in the eyes of the Lord.",
               "The ark prefigures baptism and the Church as the vessel of salvation (1 Peter 3:20-21)."),
    
    ReadingDay(7, None, ["Genesis 8:1-9:17"], "New Beginning",
               "The flood recedes; God makes a covenant with Noah.",
               "After judgment comes new creation and covenant - God will never again destroy by flood.",
               "Genesis 9:13 - I do set my bow in the cloud.",
               "This covenant points to God's ultimate promise of no condemnation in Christ (Romans 8:1)."),
    
    # PATRIARCHS (Days 8-35)
    ReadingDay(8, None, ["Genesis 9:18-10:32"], "Nations Spread",
               "Noah's descendants spread across the earth; the table of nations.",
               "From Noah's three sons come all the peoples of the earth.",
               "Genesis 10:32 - By these were the nations divided in the earth after the flood.",
               "From all these nations, God will gather a people for Himself through Christ."),
    
    ReadingDay(9, None, ["Genesis 11:1-32"], "Babel and Abraham's Line",
               "Humanity rebels at Babel; God scatters them; Abraham's lineage begins.",
               "Human pride attempts to reach heaven; God will come down instead.",
               "Genesis 11:4 - Let us build us a city and a tower.",
               "At Pentecost, the curse of Babel is reversed as all nations hear in their own tongue."),
    
    ReadingDay(10, None, ["Genesis 12:1-20"], "The Call of Abram",
               "God calls Abram to leave everything and follow; promises blessing to all nations.",
               "Here begins the story of Israel - one man called to bless all families of the earth.",
               "Genesis 12:2-3 - I will bless you... in you all families of the earth shall be blessed.",
               "This promise is fulfilled in Christ, Abraham's seed (Galatians 3:16)."),
    
    ReadingDay(11, None, ["Genesis 13:1-14:24"], "Abram and Lot",
               "Abram and Lot separate; Abram meets Melchizedek.",
               "Abram shows generosity; Melchizedek blesses him with bread and wine.",
               "Genesis 14:18 - Melchizedek king of Salem brought forth bread and wine.",
               "Christ is priest forever after the order of Melchizedek (Hebrews 7)."),
    
    ReadingDay(12, None, ["Genesis 15:1-21"], "Covenant with Abram",
               "God makes a covenant with Abram; counts his faith as righteousness.",
               "God alone passes through the pieces, taking the covenant curse upon Himself.",
               "Genesis 15:6 - He believed in the Lord; and he counted it to him for righteousness.",
               "Paul uses this to show justification by faith (Romans 4:3)."),
    
    ReadingDay(13, None, ["Genesis 16:1-17:27"], "Ishmael and Covenant Sign",
               "Hagar bears Ishmael; God gives circumcision as covenant sign.",
               "Human attempts to fulfill God's promise fail; God's sign marks His people.",
               "Genesis 17:7 - I will establish my covenant between me and you.",
               "Circumcision of the heart is the true sign (Romans 2:29; Colossians 2:11)."),
    
    ReadingDay(14, None, ["Genesis 18:1-33"], "Three Visitors",
               "The Lord appears to Abraham; Sarah laughs; Abraham intercedes for Sodom.",
               "God reveals His plans to Abraham and invites him to intercede.",
               "Genesis 18:25 - Shall not the Judge of all the earth do right?",
               "Christ is our intercessor who stands before God on our behalf (Romans 8:34)."),
    
    ReadingDay(15, None, ["Genesis 19:1-38"], "Sodom Destroyed",
               "Lot is rescued; Sodom and Gomorrah are destroyed.",
               "Judgment falls on wickedness, but God remembers Abraham and saves Lot.",
               "Genesis 19:29 - God remembered Abraham, and sent Lot out.",
               "Lot's deliverance pictures God's rescue of His people from judgment."),
    
    ReadingDay(16, None, ["Genesis 20:1-21:34"], "Isaac Born",
               "Abraham's failure with Abimelech; Isaac is born; Hagar and Ishmael sent away.",
               "The promised child finally comes - laughter after long waiting.",
               "Genesis 21:6 - God has made me laugh.",
               "Isaac is a type of Christ - the promised son given after long waiting."),
    
    ReadingDay(17, None, ["Genesis 22:1-24"], "The Binding of Isaac",
               "God tests Abraham; Isaac is spared; a ram is provided.",
               "This is the supreme test of faith - and the clearest OT picture of the cross.",
               "Genesis 22:8 - God will provide himself a lamb.",
               "Abraham's willingness to sacrifice his only son prefigures the Father's gift of Christ."),
    
    ReadingDay(18, None, ["Genesis 23:1-24:67"], "A Bride for Isaac",
               "Sarah dies; Abraham sends for a bride for Isaac.",
               "The servant seeks a bride - a picture of the Spirit gathering the Church.",
               "Genesis 24:58 - I will go.",
               "Rebekah's willingness pictures the Church's response to Christ's call."),
    
    ReadingDay(19, None, ["Genesis 25:1-34"], "Jacob and Esau",
               "Abraham dies; twins are born; Esau sells his birthright.",
               "The younger will serve the older - God's choice defies human expectation.",
               "Genesis 25:23 - The elder shall serve the younger.",
               "God's election is by grace, not merit (Romans 9:10-13)."),
    
    ReadingDay(20, None, ["Genesis 26:1-33", "Genesis 27:1-46"], "The Stolen Blessing",
               "Isaac blesses Jacob through deception.",
               "God's purposes advance even through human failure and deceit.",
               "Genesis 27:28 - God give you of the dew of heaven.",
               "God's blessing cannot be stolen by our schemes - it is given by grace."),
    
    ReadingDay(21, None, ["Genesis 28:1-22"], "Jacob's Ladder",
               "Jacob flees; dreams of a ladder; God renews the covenant.",
               "Heaven touches earth at Bethel; God promises presence.",
               "Genesis 28:12 - A ladder set up on the earth, the top of it reached to heaven.",
               "Jesus is the true ladder connecting heaven and earth (John 1:51)."),
    
    ReadingDay(22, None, ["Genesis 29:1-30:43"], "Jacob's Wives and Children",
               "Jacob serves for Rachel; Leah and Rachel bear children.",
               "Through dysfunction and favoritism, the twelve tribes begin.",
               "Genesis 29:35 - This time I will praise the Lord.",
               "From Leah's son Judah will come the Lion of Judah, Christ."),
    
    ReadingDay(23, None, ["Genesis 31:1-55"], "Jacob Flees Laban",
               "Jacob leaves Laban; conflict and covenant.",
               "After 20 years, Jacob returns toward the Promised Land.",
               "Genesis 31:3 - Return unto the land of your fathers.",
               "God calls us back from our wanderings to Himself."),
    
    ReadingDay(24, None, ["Genesis 32:1-32"], "Wrestling with God",
               "Jacob wrestles with God; receives the name Israel.",
               "Transformation comes through struggle; Jacob is broken and blessed.",
               "Genesis 32:28 - Your name shall be called Israel.",
               "We too must wrestle with God and be transformed."),
    
    ReadingDay(25, None, ["Genesis 33:1-34:31"], "Reconciliation and Tragedy",
               "Jacob and Esau reconcile; Dinah's tragedy.",
               "Grace enables reconciliation; sin still brings devastating consequences.",
               "Genesis 33:4 - Esau ran to meet him, and embraced him.",
               "Esau's embrace pictures the Father's welcome to the prodigal."),
    
    ReadingDay(26, None, ["Genesis 35:1-29", "Genesis 36:1-43"], "Return to Bethel",
               "Jacob returns to Bethel; Rachel dies; Isaac dies.",
               "The patriarchal era transitions; the focus shifts to Joseph.",
               "Genesis 35:3 - Let us arise, and go up to Bethel.",
               "We must continually return to our first encounter with God."),
    
    ReadingDay(27, None, ["Genesis 37:1-36"], "Joseph Sold",
               "Joseph's dreams; his brothers sell him into slavery.",
               "What is meant for evil, God will use for salvation.",
               "Genesis 37:28 - They sold Joseph to the Ishmaelites for twenty pieces of silver.",
               "Joseph sold for silver prefigures Christ betrayed for silver."),
    
    ReadingDay(28, None, ["Genesis 38:1-30", "Genesis 39:1-23"], "Judah and Joseph",
               "Judah's sin with Tamar; Joseph's faithfulness in Potiphar's house.",
               "Contrast: Judah falls into sin; Joseph flees from it.",
               "Genesis 39:9 - How can I do this great wickedness, and sin against God?",
               "From Judah's flawed line comes Christ; Joseph's righteousness pictures Christ."),
    
    ReadingDay(29, None, ["Genesis 40:1-41:57"], "Dreams Interpreted",
               "Joseph interprets dreams in prison; then Pharaoh's dreams; exalted to power.",
               "From prison to palace - God elevates the humble.",
               "Genesis 41:16 - It is not in me: God shall give Pharaoh an answer.",
               "Joseph's exaltation after suffering prefigures Christ's exaltation."),
    
    ReadingDay(30, None, ["Genesis 42:1-38"], "Brothers Come to Egypt",
               "Joseph's brothers come to buy grain; Joseph tests them.",
               "The brothers who sold Joseph must now bow before him.",
               "Genesis 42:8 - Joseph knew his brethren, but they knew not him.",
               "Joseph's brothers bowing fulfills his dreams - God's word is sure."),
    
    ReadingDay(31, None, ["Genesis 43:1-44:34"], "The Test",
               "Brothers return with Benjamin; Judah offers himself.",
               "Judah, who sold Joseph, now offers himself for Benjamin.",
               "Genesis 44:33 - Let your servant abide instead of the lad.",
               "Judah's substitution points to Christ, the greater Judah."),
    
    ReadingDay(32, None, ["Genesis 45:1-28"], "Joseph Reveals Himself",
               "Joseph reveals himself; forgives his brothers.",
               "What was meant for evil, God used for good.",
               "Genesis 45:5 - God sent me before you to preserve life.",
               "Joseph's forgiveness pictures Christ's forgiveness of those who crucified him."),
    
    ReadingDay(33, None, ["Genesis 46:1-47:31"], "Israel Comes to Egypt",
               "Jacob moves to Egypt; Israel settles in Goshen.",
               "The whole family enters Egypt - setting the stage for the Exodus.",
               "Genesis 46:3 - Fear not to go down into Egypt.",
               "God's people must sometimes sojourn in foreign lands before deliverance."),
    
    ReadingDay(34, None, ["Genesis 48:1-49:33"], "Jacob Blesses His Sons",
               "Jacob blesses his sons with prophetic words.",
               "The twelve tribes receive their destiny; Judah receives the scepter.",
               "Genesis 49:10 - The sceptre shall not depart from Judah.",
               "This prophecy points directly to Christ, the King from Judah."),
    
    ReadingDay(35, None, ["Genesis 50:1-26", "Job 1:1-22"], "Death and Suffering",
               "Joseph dies; Job's trials begin.",
               "Genesis ends with death in Egypt; Job opens the question of suffering.",
               "Genesis 50:20 - You meant evil against me; but God meant it for good.",
               "This is the theme of Scripture: God works all things for good (Romans 8:28)."),
    
    # Continue with remaining days...
    # (Days 36-365 would follow the same pattern)
]

# For brevity in this file, we'll generate the remaining days programmatically
# In a full implementation, each day would be hand-crafted like the above

def _generate_remaining_days():
    """Generate placeholder readings for remaining days"""
    remaining = []
    
    # Exodus readings (Days 36-60)
    exodus_readings = [
        ("Exodus 1-2", "Israel Oppressed; Moses Born"),
        ("Exodus 3-4", "The Burning Bush"),
        ("Exodus 5-6", "Confronting Pharaoh"),
        ("Exodus 7-8", "Plagues Begin"),
        ("Exodus 9-10", "Plagues Continue"),
        ("Exodus 11-12", "The Passover"),
        ("Exodus 13-14", "Crossing the Red Sea"),
        ("Exodus 15-16", "Songs and Manna"),
        ("Exodus 17-18", "Water and Wisdom"),
        ("Exodus 19-20", "Sinai and Ten Commandments"),
        ("Exodus 21-23", "The Book of the Covenant"),
        ("Exodus 24-27", "Covenant Ratified; Tabernacle Instructions"),
        ("Exodus 28-31", "Priesthood Established"),
        ("Exodus 32-34", "Golden Calf; Covenant Renewed"),
        ("Exodus 35-40", "Tabernacle Built"),
    ]
    
    for i, (passage, title) in enumerate(exodus_readings, 36):
        remaining.append(ReadingDay(
            i, None, [passage], title,
            f"Reading from {passage}",
            "God delivers Israel and establishes worship.",
            "", ""
        ))
    
    # Add more periods similarly...
    # This would be expanded to cover all 365 days
    
    return remaining


class ChronologicalPlan:
    """
    Manages the chronological reading plan.
    """
    
    def __init__(self, start_date: date = None):
        """
        Initialize the plan.
        
        Args:
            start_date: When to start the plan. Defaults to Jan 1 of current year.
        """
        if start_date is None:
            today = date.today()
            start_date = date(today.year, 1, 1)
        
        self.start_date = start_date
        self.readings = READING_PLAN + _generate_remaining_days()
        
        # Assign dates to readings
        for i, reading in enumerate(self.readings):
            reading.date = start_date + timedelta(days=i)
    
    def get_reading_for_day(self, day_number: int) -> Optional[ReadingDay]:
        """Get reading for a specific day number (1-365)"""
        if 1 <= day_number <= len(self.readings):
            return self.readings[day_number - 1]
        return None
    
    def get_reading_for_date(self, d: date) -> Optional[ReadingDay]:
        """Get reading for a specific date"""
        if d < self.start_date:
            return None
        
        day_number = (d - self.start_date).days + 1
        return self.get_reading_for_day(day_number)
    
    def get_todays_reading(self) -> Optional[ReadingDay]:
        """Get today's reading"""
        return self.get_reading_for_date(date.today())
    
    def get_current_period(self, d: date = None) -> Dict:
        """Get the salvation history period for a date"""
        if d is None:
            d = date.today()
        
        reading = self.get_reading_for_date(d)
        if not reading:
            return None
        
        for period_id, period in SALVATION_HISTORY_PERIODS.items():
            if period['days'][0] <= reading.day_number <= period['days'][1]:
                return {
                    'id': period_id,
                    **period
                }
        
        return None
    
    def get_progress(self, d: date = None) -> Dict:
        """Get reading progress"""
        if d is None:
            d = date.today()
        
        reading = self.get_reading_for_date(d)
        if not reading:
            day_number = 0
        else:
            day_number = reading.day_number
        
        return {
            'day_number': day_number,
            'total_days': 365,
            'percentage': round(day_number / 365 * 100, 1),
            'current_period': self.get_current_period(d)
        }


# Global instance
_plan_instance: Optional[ChronologicalPlan] = None


def get_reading_plan(start_date: date = None) -> ChronologicalPlan:
    """Get or create the global reading plan"""
    global _plan_instance
    if _plan_instance is None:
        _plan_instance = ChronologicalPlan(start_date)
    return _plan_instance
