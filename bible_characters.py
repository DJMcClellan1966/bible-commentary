"""
Bible Character Models
Quantum-based character models for Moses, David, Solomon, Paul, and John
Trained on their actual Bible writings
"""
from quantum_character import QuantumCharacter, create_quantum_character
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Bible texts attributed to each character
BIBLE_CHARACTER_TEXTS = {
    "Moses": [
        # Genesis (attributed to Moses)
        "In the beginning God created the heavens and the earth.",
        "And God said, Let there be light: and there was light.",
        "And God saw every thing that he had made, and, behold, it was very good.",
        "And the Lord God formed man of the dust of the ground, and breathed into his nostrils the breath of life.",
        "And the Lord God said, It is not good that the man should be alone.",
        "Therefore shall a man leave his father and his mother, and shall cleave unto his wife.",
        "And God blessed them, and God said unto them, Be fruitful, and multiply, and replenish the earth.",
        # Exodus
        "And God said, I am the Lord thy God, which have brought thee out of the land of Egypt.",
        "Thou shalt have no other gods before me.",
        "Thou shalt not make unto thee any graven image.",
        "Thou shalt not take the name of the Lord thy God in vain.",
        "Remember the sabbath day, to keep it holy.",
        "Honour thy father and thy mother.",
        "Thou shalt not kill.",
        "Thou shalt not commit adultery.",
        "Thou shalt not steal.",
        "Thou shalt not bear false witness.",
        "Thou shalt not covet.",
        # Deuteronomy
        "Hear, O Israel: The Lord our God is one Lord.",
        "And thou shalt love the Lord thy God with all thine heart, and with all thy soul, and with all thy might.",
        "And these words, which I command thee this day, shall be in thine heart.",
        "The Lord thy God, he is God, the faithful God, which keepeth covenant and mercy.",
        "Man doth not live by bread only, but by every word that proceedeth out of the mouth of the Lord.",
        "The Lord is my strength and song, and he is become my salvation.",
        "The eternal God is thy refuge, and underneath are the everlasting arms.",
    ],
    
    "David": [
        # Psalms attributed to David
        "The Lord is my shepherd; I shall not want.",
        "He maketh me to lie down in green pastures: he leadeth me beside the still waters.",
        "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake.",
        "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me.",
        "Thy rod and thy staff they comfort me.",
        "Thou preparest a table before me in the presence of mine enemies.",
        "Surely goodness and mercy shall follow me all the days of my life.",
        "The Lord is my light and my salvation; whom shall I fear?",
        "The Lord is the strength of my life; of whom shall I be afraid?",
        "One thing have I desired of the Lord, that will I seek after; that I may dwell in the house of the Lord all the days of my life.",
        "Wait on the Lord: be of good courage, and he shall strengthen thine heart.",
        "Create in me a clean heart, O God; and renew a right spirit within me.",
        "Cast me not away from thy presence; and take not thy holy spirit from me.",
        "Restore unto me the joy of thy salvation; and uphold me with thy free spirit.",
        "The sacrifices of God are a broken spirit: a broken and a contrite heart, O God, thou wilt not despise.",
        "Bless the Lord, O my soul: and all that is within me, bless his holy name.",
        "Bless the Lord, O my soul, and forget not all his benefits.",
        "Who forgiveth all thine iniquities; who healeth all thy diseases.",
        "The Lord is merciful and gracious, slow to anger, and plenteous in mercy.",
        "As far as the east is from the west, so far hath he removed our transgressions from us.",
        "I will praise thee, O Lord, with my whole heart; I will shew forth all thy marvellous works.",
        "The Lord is nigh unto all them that call upon him, to all that call upon him in truth.",
    ],
    
    "Solomon": [
        # Proverbs
        "The fear of the Lord is the beginning of knowledge: but fools despise wisdom and instruction.",
        "Trust in the Lord with all thine heart; and lean not unto thine own understanding.",
        "In all thy ways acknowledge him, and he shall direct thy paths.",
        "Be not wise in thine own eyes: fear the Lord, and depart from evil.",
        "Wisdom is the principal thing; therefore get wisdom: and with all thy getting get understanding.",
        "Exalt her, and she shall promote thee: she shall bring thee to honour, when thou dost embrace her.",
        "She shall give to thine head an ornament of grace: a crown of glory shall she deliver to thee.",
        "A soft answer turneth away wrath: but grievous words stir up anger.",
        "A merry heart doeth good like a medicine: but a broken spirit drieth the bones.",
        "Train up a child in the way he should go: and when he is old, he will not depart from it.",
        "Pride goeth before destruction, and an haughty spirit before a fall.",
        "Better is a little with righteousness than great revenues without right.",
        "The way of the Lord is strength to the upright: but destruction shall be to the workers of iniquity.",
        "He that walketh with wise men shall be wise: but a companion of fools shall be destroyed.",
        "As iron sharpeneth iron; so a man sharpeneth the countenance of his friend.",
        # Ecclesiastes
        "Vanity of vanities, saith the Preacher, vanity of vanities; all is vanity.",
        "To every thing there is a season, and a time to every purpose under the heaven.",
        "A time to be born, and a time to die; a time to plant, and a time to pluck up that which is planted.",
        "He hath made every thing beautiful in his time.",
        "I know that there is no good in them, but for a man to rejoice, and to do good in his life.",
        "Remember now thy Creator in the days of thy youth.",
        "Let us hear the conclusion of the whole matter: Fear God, and keep his commandments: for this is the whole duty of man.",
        # Song of Solomon
        "I am the rose of Sharon, and the lily of the valleys.",
        "My beloved is mine, and I am his.",
        "Many waters cannot quench love, neither can the floods drown it.",
    ],
    
    "Paul": [
        # Romans
        "For I am not ashamed of the gospel of Christ: for it is the power of God unto salvation to every one that believeth.",
        "For the wrath of God is revealed from heaven against all ungodliness and unrighteousness of men.",
        "For all have sinned, and come short of the glory of God.",
        "Being justified freely by his grace through the redemption that is in Christ Jesus.",
        "Therefore being justified by faith, we have peace with God through our Lord Jesus Christ.",
        "For when we were yet without strength, in due time Christ died for the ungodly.",
        "But God commendeth his love toward us, in that, while we were yet sinners, Christ died for us.",
        "For I am persuaded, that neither death, nor life, nor angels, nor principalities, nor powers, nor things present, nor things to come, nor height, nor depth, nor any other creature, shall be able to separate us from the love of God, which is in Christ Jesus our Lord.",
        "I beseech you therefore, brethren, by the mercies of God, that ye present your bodies a living sacrifice, holy, acceptable unto God, which is your reasonable service.",
        "And be not conformed to this world: but be ye transformed by the renewing of your mind.",
        # 1 Corinthians
        "For the preaching of the cross is to them that perish foolishness; but unto us which are saved it is the power of God.",
        "But God hath chosen the foolish things of the world to confound the wise; and God hath chosen the weak things of the world to confound the things which are mighty.",
        "And now abideth faith, hope, charity, these three; but the greatest of these is charity.",
        "Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up.",
        "For now we see through a glass, darkly; but then face to face: now I know in part; but then shall I know even as also I am known.",
        # Galatians
        "I am crucified with Christ: nevertheless I live; yet not I, but Christ liveth in me.",
        "For in Jesus Christ neither circumcision availeth any thing, nor uncircumcision; but faith which worketh by love.",
        "But the fruit of the Spirit is love, joy, peace, longsuffering, gentleness, goodness, faith, meekness, temperance.",
        # Ephesians
        "For by grace are ye saved through faith; and that not of yourselves: it is the gift of God.",
        "For we are his workmanship, created in Christ Jesus unto good works.",
        "Put on the whole armour of God, that ye may be able to stand against the wiles of the devil.",
        # Philippians
        "For to me to live is Christ, and to die is gain.",
        "I can do all things through Christ which strengtheneth me.",
        # Colossians
        "For in him dwelleth all the fulness of the Godhead bodily.",
        # 1 Thessalonians
        "Rejoice evermore. Pray without ceasing. In every thing give thanks: for this is the will of God in Christ Jesus concerning you.",
        # 1 Timothy
        "For there is one God, and one mediator between God and men, the man Christ Jesus.",
        "Fight the good fight of faith, lay hold on eternal life.",
        # 2 Timothy
        "For God hath not given us the spirit of fear; but of power, and of love, and of a sound mind.",
        "All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness.",
    ],
    
    "John": [
        # Gospel of John
        "In the beginning was the Word, and the Word was with God, and the Word was God.",
        "The same was in the beginning with God.",
        "All things were made by him; and without him was not any thing made that was made.",
        "In him was life; and the life was the light of men.",
        "And the Word was made flesh, and dwelt among us, and we beheld his glory.",
        "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        "For God sent not his Son into the world to condemn the world; but that the world through him might be saved.",
        "Jesus said unto her, I am the resurrection, and the life: he that believeth in me, though he were dead, yet shall he live.",
        "Jesus saith unto him, I am the way, the truth, and the life: no man cometh unto the Father, but by me.",
        "Greater love hath no man than this, that a man lay down his life for his friends.",
        "Peace I leave with you, my peace I give unto you: not as the world giveth, give I unto you.",
        "I am the vine, ye are the branches: He that abideth in me, and I in him, the same bringeth forth much fruit.",
        # 1 John
        "That which was from the beginning, which we have heard, which we have seen with our eyes, which we have looked upon, and our hands have handled, of the Word of life.",
        "God is light, and in him is no darkness at all.",
        "If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness.",
        "Beloved, let us love one another: for love is of God; and every one that loveth is born of God, and knoweth God.",
        "He that loveth not knoweth not God; for God is love.",
        "In this was manifested the love of God toward us, because that God sent his only begotten Son into the world, that we might live through him.",
        "Herein is love, not that we loved God, but that he loved us, and sent his Son to be the propitiation for our sins.",
        "Beloved, if God so loved us, we ought also to love one another.",
        "There is no fear in love; but perfect love casteth out fear: because fear hath torment.",
        "We love him, because he first loved us.",
        "And this is the confidence that we have in him, that, if we ask any thing according to his will, he heareth us.",
        # 2 John
        "And this is love, that we walk after his commandments.",
        # 3 John
        "Beloved, I wish above all things that thou mayest prosper and be in health, even as thy soul prospereth.",
        # Revelation
        "I am Alpha and Omega, the beginning and the ending, saith the Lord, which is, and which was, and which is to come, the Almighty.",
        "Behold, I stand at the door, and knock: if any man hear my voice, and open the door, I will come in to him, and will sup with him, and he with me.",
        "And God shall wipe away all tears from their eyes; and there shall be no more death, neither sorrow, nor crying, neither shall there be any more pain: for the former things are passed away.",
        "And he said unto me, It is done. I am Alpha and Omega, the beginning and the end.",
    ]
}

# Personality traits for each character
CHARACTER_PERSONALITIES = {
    "Moses": {
        "authority": 0.9,
        "wisdom": 0.85,
        "leadership": 0.9,
        "reverence": 0.95,
        "teaching": 0.9,
        "depth": 0.85
    },
    "David": {
        "warmth": 0.9,
        "passion": 0.95,
        "worship": 0.95,
        "honesty": 0.9,
        "compassion": 0.9,
        "poetry": 0.95
    },
    "Solomon": {
        "wisdom": 0.95,
        "practicality": 0.9,
        "reflection": 0.9,
        "teaching": 0.9,
        "depth": 0.95,
        "philosophy": 0.9
    },
    "Paul": {
        "passion": 0.95,
        "teaching": 0.95,
        "zeal": 0.9,
        "theology": 0.95,
        "encouragement": 0.9,
        "depth": 0.95
    },
    "John": {
        "love": 0.95,
        "warmth": 0.9,
        "mystery": 0.85,
        "intimacy": 0.95,
        "revelation": 0.9,
        "depth": 0.9
    }
}


class BibleCharacterSystem:
    """System for managing multiple Bible character models"""
    
    def __init__(self):
        self.characters: Dict[str, QuantumCharacter] = {}
        self.initialized = False
    
    def initialize_characters(self):
        """Initialize all Bible character models"""
        if self.initialized:
            return
        
        logger.info("Initializing Bible character models...")
        
        for character_name, texts in BIBLE_CHARACTER_TEXTS.items():
            logger.info(f"Creating {character_name} character model...")
            
            # Expand texts for training
            training_texts = []
            for text in texts:
                # Create conversational pairs
                training_texts.append(text)
                # Add variations
                training_texts.append(f"Question: What does this mean? Answer: {text}")
                training_texts.append(f"Teach me about: {text}")
            
            # Repeat for better training
            training_texts = training_texts * 10
            
            personality = CHARACTER_PERSONALITIES.get(character_name, {})
            knowledge_base = texts  # Use their own writings as knowledge base
            
            try:
                character = create_quantum_character(
                    training_texts,
                    personality_traits=personality,
                    knowledge_base=knowledge_base
                )
                self.characters[character_name] = character
                logger.info(f"{character_name} character model created successfully")
            except Exception as e:
                logger.error(f"Error creating {character_name}: {e}")
        
        self.initialized = True
        logger.info(f"Initialized {len(self.characters)} character models")
    
    def get_character(self, name: str) -> Optional[QuantumCharacter]:
        """Get a character by name"""
        if not self.initialized:
            self.initialize_characters()
        
        return self.characters.get(name)
    
    def chat_with_character(self, character_name: str, message: str) -> Dict:
        """Chat with a specific character"""
        character = self.get_character(character_name)
        
        if not character:
            return {
                "error": f"Character '{character_name}' not found",
                "available": list(self.characters.keys())
            }
        
        # Generate response
        response = character.generate_response(
            message,
            use_quantum_context=True,
            use_knowledge_base=True,
            temperature=0.8
        )
        
        return {
            "character": character_name,
            "message": message,
            "response": response,
            "personality": CHARACTER_PERSONALITIES.get(character_name, {})
        }
    
    def compare_characters(self, question: str) -> Dict:
        """Get responses from all characters for comparison"""
        if not self.initialized:
            self.initialize_characters()
        
        responses = {}
        
        for name, character in self.characters.items():
            try:
                response = character.generate_response(
                    question,
                    use_quantum_context=True,
                    use_knowledge_base=True,
                    temperature=0.8
                )
                responses[name] = {
                    "response": response,
                    "personality": CHARACTER_PERSONALITIES.get(name, {})
                }
            except Exception as e:
                responses[name] = {"error": str(e)}
        
        return {
            "question": question,
            "responses": responses
        }
    
    def get_character_info(self, name: str) -> Dict:
        """Get information about a character"""
        if name not in BIBLE_CHARACTER_TEXTS:
            return {"error": "Character not found"}
        
        return {
            "name": name,
            "personality": CHARACTER_PERSONALITIES.get(name, {}),
            "writings_count": len(BIBLE_CHARACTER_TEXTS[name]),
            "sample_texts": BIBLE_CHARACTER_TEXTS[name][:5]
        }


# Global instance
_bible_characters = None

def get_bible_characters() -> BibleCharacterSystem:
    """Get the global Bible character system instance"""
    global _bible_characters
    if _bible_characters is None:
        _bible_characters = BibleCharacterSystem()
    return _bible_characters
