"""
Interconnection Engine - The Heart of Deep Bible Study
Reveals how every passage connects through Scripture:
- Backward links (to Moses, prophets, earlier Scripture)
- Forward links (to Christ, NT fulfillment)
- Typological connections (OT prefigurements of Christ)
- Church Fathers' wisdom
- Historical progression of understanding
"""
import json
import os
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from quantum_kernel import get_kernel, KernelConfig


@dataclass
class Connection:
    """A connection between Scripture passages"""
    reference: str
    text: str
    connection_type: str  # backward, forward, typological, thematic
    explanation: str
    similarity: float
    church_fathers: List[Dict] = None
    

@dataclass
class InterconnectedVerse:
    """A verse with all its deep connections revealed"""
    reference: str
    text: str
    backward_links: List[Connection]  # Earlier Scripture this echoes
    forward_links: List[Connection]   # Later Scripture this points to
    typological: List[Dict]           # Type/antitype relationships
    church_fathers: List[Dict]        # Patristic wisdom
    themes: List[str]                 # Key themes
    historical_perspectives: Dict     # Early, Medieval, Reformation, Modern
    christ_connection: str = ""       # Rich explanation of connection to Christ


class InterconnectionEngine:
    """
    Engine for discovering and presenting the deep interconnections in Scripture.
    
    This is not about surface-level cross-references, but about revealing
    the tapestry: how Moses speaks to Jesus, how Genesis echoes in Revelation,
    how the Church Fathers wrestled with these truths.
    """
    
    def __init__(self, bible_data: Dict = None):
        """
        Initialize the engine.
        
        Args:
            bible_data: Dictionary of {reference: text} for all verses
        """
        self.kernel = get_kernel(KernelConfig(
            embedding_dim=256,
            cache_size=100000,
            enable_caching=True
        ))
        
        self.bible_data = bible_data or {}
        
        # Load curated data
        self.typology_db = self._load_typology()
        self.church_fathers_db = self._load_church_fathers()
        self.connection_explanations = self._load_connection_explanations()
        
        # Book order for determining backward/forward
        self.book_order = self._get_book_order()
        
        # Key theological concepts for thematic linking
        self.theological_concepts = {
            'covenant': ['covenant', 'promise', 'oath', 'agreement', 'testament'],
            'sacrifice': ['sacrifice', 'offering', 'blood', 'lamb', 'altar', 'atonement'],
            'redemption': ['redeem', 'ransom', 'rescue', 'deliver', 'save', 'salvation'],
            'kingdom': ['kingdom', 'reign', 'throne', 'king', 'rule', 'dominion'],
            'love': ['love', 'beloved', 'compassion', 'mercy', 'grace', 'kindness'],
            'faith': ['faith', 'believe', 'trust', 'faithful', 'hope'],
            'righteousness': ['righteous', 'justice', 'just', 'holy', 'pure'],
            'sin': ['sin', 'transgression', 'iniquity', 'evil', 'wicked'],
            'forgiveness': ['forgive', 'pardon', 'cleanse', 'wash', 'purify'],
            'resurrection': ['resurrection', 'rise', 'raised', 'life', 'death conquered'],
            'spirit': ['spirit', 'holy spirit', 'breath', 'wind', 'power'],
            'prophecy': ['prophet', 'prophecy', 'foretold', 'spoken', 'fulfilled'],
            'wisdom': ['wisdom', 'understanding', 'knowledge', 'discernment'],
            'worship': ['worship', 'praise', 'glory', 'honor', 'exalt'],
            'suffering': ['suffer', 'affliction', 'trial', 'persecution', 'tribulation']
        }
    
    def _load_typology(self) -> Dict:
        """Load the typology database"""
        path = os.path.join(os.path.dirname(__file__), 'data', 'typology.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'types': [], 'thematic_connections': {}}
    
    def _load_church_fathers(self) -> Dict:
        """Load Church Fathers quotes database"""
        path = os.path.join(os.path.dirname(__file__), 'data', 'church_fathers_quotes.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'quotes_by_verse': {}, 'quotes_by_theme': {}, 'authors': {}}
    
    def _load_connection_explanations(self) -> Dict:
        """Load rich connection explanations"""
        path = os.path.join(os.path.dirname(__file__), 'data', 'connection_explanations.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'thematic_explanations': {}, 'connection_patterns': {}, 'christ_connections': {}}
    
    def _get_book_order(self) -> Dict[str, int]:
        """Get canonical book order for determining backward/forward links"""
        books = [
            # Old Testament
            'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
            'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel',
            '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
            'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs',
            'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah',
            'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
            'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
            'Haggai', 'Zechariah', 'Malachi',
            # New Testament
            'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans',
            '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
            'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
            '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
            'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
            'Jude', 'Revelation'
        ]
        return {book: i for i, book in enumerate(books)}
    
    def _parse_reference(self, reference: str) -> Tuple[str, int, int]:
        """Parse a reference like 'John 3:16' into (book, chapter, verse)"""
        # Handle various formats
        match = re.match(r'(\d?\s*\w+(?:\s+\w+)?)\s+(\d+):(\d+)', reference)
        if match:
            book = match.group(1).strip()
            chapter = int(match.group(2))
            verse = int(match.group(3))
            return book, chapter, verse
        return None, 0, 0
    
    def _get_book_from_reference(self, reference: str) -> str:
        """Extract book name from reference"""
        book, _, _ = self._parse_reference(reference)
        return book
    
    def _is_old_testament(self, reference: str) -> bool:
        """Check if a reference is in the Old Testament"""
        book = self._get_book_from_reference(reference)
        if book:
            order = self.book_order.get(book, 0)
            return order < 39  # First 39 books are OT
        return False
    
    def _is_new_testament(self, reference: str) -> bool:
        """Check if a reference is in the New Testament"""
        return not self._is_old_testament(reference)
    
    def _comes_before(self, ref1: str, ref2: str) -> bool:
        """Check if ref1 comes before ref2 in canonical order"""
        book1 = self._get_book_from_reference(ref1)
        book2 = self._get_book_from_reference(ref2)
        if book1 and book2:
            return self.book_order.get(book1, 0) < self.book_order.get(book2, 0)
        return False
    
    def get_interconnections(self, reference: str, verse_text: str = None) -> InterconnectedVerse:
        """
        Get all deep interconnections for a verse.
        
        This is the main method - it reveals the full tapestry of connections.
        """
        if verse_text is None and reference in self.bible_data:
            verse_text = self.bible_data[reference]
        
        if not verse_text:
            verse_text = f"[Text for {reference}]"
        
        # Find semantic connections
        all_connections = self._find_semantic_connections(reference, verse_text)
        
        # Separate into backward and forward links
        backward_links = []
        forward_links = []
        
        for conn in all_connections:
            if self._comes_before(conn.reference, reference):
                conn.connection_type = 'backward'
                backward_links.append(conn)
            else:
                conn.connection_type = 'forward'
                forward_links.append(conn)
        
        # Get typological connections
        typological = self._find_typological_connections(reference, verse_text)
        
        # Get Church Fathers quotes
        church_fathers = self._get_church_fathers_quotes(reference, verse_text)
        
        # Extract themes
        themes = self._extract_themes(verse_text)
        
        # Get historical perspectives
        historical = self._get_historical_perspectives(reference, verse_text)
        
        # Get rich Christ connection
        christ_connection = self.get_christ_connection(reference, verse_text)
        
        return InterconnectedVerse(
            reference=reference,
            text=verse_text,
            backward_links=backward_links[:5],  # Top 5
            forward_links=forward_links[:5],
            typological=typological,
            church_fathers=church_fathers,
            themes=themes,
            historical_perspectives=historical,
            christ_connection=christ_connection
        )
    
    def _find_semantic_connections(self, reference: str, verse_text: str) -> List[Connection]:
        """Find semantically related verses"""
        connections = []
        
        if not self.bible_data:
            return connections
        
        # Get all verses except the current one
        candidates = [(ref, text) for ref, text in self.bible_data.items() 
                      if ref != reference]
        
        if not candidates:
            return connections
        
        # Find similar verses
        candidate_texts = [text for _, text in candidates]
        similar = self.kernel.find_similar(verse_text, candidate_texts, top_k=20)
        
        # Create connections
        text_to_ref = {text: ref for ref, text in candidates}
        
        for text, similarity in similar:
            if similarity > 0.5:  # Threshold for meaningful connection
                ref = text_to_ref.get(text, "Unknown")
                # Get Church Fathers (or others) for this linked verse/themes when available
                themes1 = self._extract_themes(verse_text)
                themes2 = self._extract_themes(text)
                common_themes = list(set(themes1) & set(themes2))
                father_quotes = self._get_fathers_for_connection(ref, text, common_themes, max_quotes=2)
                
                explanation = self._explain_connection(verse_text, text, similarity, reference, ref)
                if father_quotes:
                    explanation = explanation + self._format_father_quote(father_quotes[0])
                
                connections.append(Connection(
                    reference=ref,
                    text=text[:200] + "..." if len(text) > 200 else text,
                    connection_type='semantic',
                    explanation=explanation,
                    similarity=similarity,
                    church_fathers=father_quotes or None
                ))
        
        return connections
    
    def _tie_explanation_to_refs(self, generic: str, ref1: str, ref2: str) -> str:
        """Make a generic explanation specific to this pair of references so each connection reads uniquely."""
        if not ref1 or not ref2 or ref1 == "Unknown" or ref2 == "Unknown":
            return generic
        refs = f"{ref1} and {ref2}"
        if generic.strip().lower().startswith("both passages"):
            return generic.replace("Both passages", f"{refs} both", 1).replace("these passages", "these two", 1)
        if generic.strip().lower().startswith("the "):
            return f"Between {refs}: " + generic[0].lower() + generic[1:]
        if generic.strip().lower().startswith("these passages"):
            return generic.replace("These passages", f"{refs}", 1)
        return f"{refs} — " + generic

    def _format_father_quote(self, q: Dict, max_quote_len: int = 120) -> str:
        """Format a Church Father (or other) quote for appending to a connection explanation."""
        quote_text = (q.get('quote') or '').strip()
        if not quote_text:
            return ''
        author = q.get('author') or 'A Church Father'
        work = q.get('work') or ''
        if len(quote_text) > max_quote_len:
            quote_text = quote_text[:max_quote_len].rsplit(' ', 1)[0] + '...'
        if work:
            return f' As {author} wrote in {work}: "{quote_text}"'
        return f' As {author} wrote: "{quote_text}"'

    def _explain_connection(self, text1: str, text2: str, similarity: float, ref1: str = "", ref2: str = "") -> str:
        """Generate a rich theological explanation for why two verses are connected. Each explanation is tied to ref1/ref2 so they are distinct."""
        # Find common themes
        themes1 = self._extract_themes(text1)
        themes2 = self._extract_themes(text2)
        common_themes = set(themes1) & set(themes2)
        
        explanations = []
        
        # Try to get a rich thematic explanation
        if common_themes:
            for theme in common_themes:
                theme_key = theme.lower()
                if theme_key in self.connection_explanations.get('thematic_explanations', {}):
                    thematic_data = self.connection_explanations['thematic_explanations'][theme_key]
                    explanations.append(thematic_data['explanation'])
                    break
        
        # If we have a rich explanation, use it and tie to refs
        if explanations:
            return self._tie_explanation_to_refs(explanations[0], ref1, ref2)
        
        # Otherwise, build a contextual explanation
        if common_themes:
            theme_str = ', '.join(common_themes)
            
            # Provide theme-specific insight
            theme_insights = {
                'Covenant': "Both passages reveal God's covenant faithfulness - His binding commitment to His people that spans all of Scripture.",
                'Sacrifice': "The theme of sacrifice connects these passages, pointing to the ultimate sacrifice of Christ.",
                'Redemption': "Redemption threads through both - God buying back what was lost, rescuing His people from bondage.",
                'Kingdom': "The kingdom of God links these passages - God's reign over His creation and His people.",
                'Love': "Divine love (hesed) connects these - not mere emotion but covenant faithfulness and steadfast commitment.",
                'Faith': "Faith binds these passages - trusting God when circumstances seem impossible.",
                'Righteousness': "Both passages address righteousness - right standing before a holy God.",
                'Sin': "The reality of sin and its consequences connects these passages.",
                'Forgiveness': "God's gracious forgiveness flows through both passages.",
                'Resurrection': "Resurrection hope threads through these - God's power over death itself.",
                'Spirit': "The Spirit of God connects these - His breath that gives life and empowers.",
                'Prophecy': "Prophetic vision links these passages - God revealing His plans before they unfold.",
                'Wisdom': "Wisdom's voice echoes through both - skill in living according to God's design.",
                'Worship': "Worship connects these - the human response to divine revelation.",
                'Suffering': "The mystery of suffering links these passages - finding meaning in pain."
            }
            
            for theme in common_themes:
                if theme in theme_insights:
                    return self._tie_explanation_to_refs(theme_insights[theme], ref1, ref2)
            
            generic = f"These passages are connected through the theme of {theme_str}, which runs like a golden thread throughout Scripture, revealing God's consistent character and redemptive purposes."
            return self._tie_explanation_to_refs(generic, ref1, ref2)
        
        # Determine the connection pattern
        is_ref1_ot = self._is_old_testament(ref1) if ref1 else False
        is_ref2_ot = self._is_old_testament(ref2) if ref2 else True
        
        if is_ref1_ot and not is_ref2_ot:
            return self._tie_explanation_to_refs(
                "The Old Testament passage plants a seed that blossoms in the New Testament. What was promised or prefigured finds its fuller meaning in Christ and His Church.",
                ref1, ref2
            )
        elif not is_ref1_ot and is_ref2_ot:
            return self._tie_explanation_to_refs(
                "The New Testament passage draws from and fulfills the Old. The earlier revelation prepared the way for the later, showing Scripture's unified story.",
                ref1, ref2
            )
        
        # Find shared key concepts for more specific explanation
        words1 = set(w.lower() for w in text1.split() if len(w) > 4)
        words2 = set(w.lower() for w in text2.split() if len(w) > 4)
        common_words = words1 & words2
        
        if common_words:
            # Look for theologically significant shared words
            significant_words = {'lord', 'god', 'faith', 'love', 'grace', 'spirit', 'life', 'death', 
                               'blood', 'lamb', 'king', 'priest', 'temple', 'covenant', 'promise',
                               'salvation', 'redeem', 'holy', 'righteous', 'sin', 'forgive'}
            found_significant = [w for w in common_words if w in significant_words]
            
            if found_significant:
                word = found_significant[0]
                word_explanations = {
                    'lord': "Both passages acknowledge God's lordship - His sovereign authority over all creation and history.",
                    'god': "The character and nature of God connects these passages, revealing who He is and how He acts.",
                    'faith': "Faith links these texts - the trust in God that has always been the means of relationship with Him.",
                    'love': "Divine love connects these passages - God's steadfast, covenant love for His people.",
                    'grace': "Grace runs through both - God's unmerited favor that saves and sustains.",
                    'spirit': "The Spirit of God connects these - His presence and power at work in His people.",
                    'life': "Life - both physical and spiritual - links these passages, pointing to God as the source of all life.",
                    'death': "Death and its defeat connect these passages, pointing to resurrection hope.",
                    'blood': "The blood theme connects these - sacrifice, atonement, and the price of redemption.",
                    'lamb': "The lamb imagery links these passages, pointing to Christ, the Lamb of God.",
                    'king': "Kingship connects these - God's reign and the Messiah's throne.",
                    'priest': "Priesthood links these - mediation between God and humanity.",
                    'temple': "The temple theme connects these - God dwelling among His people.",
                    'covenant': "Covenant faithfulness binds these passages - God's unbreakable commitment.",
                    'promise': "Divine promise connects these - God's word that never fails.",
                    'salvation': "Salvation links these passages - God's rescue of His people.",
                    'redeem': "Redemption connects these - God buying back what was lost.",
                    'holy': "Holiness links these - God's otherness and the call to be set apart.",
                    'righteous': "Righteousness connects these - right standing before God.",
                    'sin': "Sin and its remedy connect these passages.",
                    'forgive': "Forgiveness flows through both - God's gracious pardon."
                }
                if word in word_explanations:
                    return self._tie_explanation_to_refs(word_explanations[word], ref1, ref2)
        
        if similarity > 0.7:
            return self._tie_explanation_to_refs(
                "These passages share deep thematic resonance - the same divine truths expressed in different contexts, revealing Scripture's remarkable unity across time and authors.",
                ref1, ref2
            )
        return self._tie_explanation_to_refs(
            "These passages illuminate each other through complementary truths. Reading them together reveals dimensions of meaning that neither shows alone.",
            ref1, ref2
        )
    
    def get_christ_connection(self, reference: str, verse_text: str) -> str:
        """Get a rich explanation of how this passage connects to Christ"""
        book = self._get_book_from_reference(reference)
        
        # Check for specific book-level Christ connections
        book_connections = self.connection_explanations.get('christ_connections', {})
        
        # Map books to connection keys
        book_to_key = {
            'Genesis': ['creation', 'fall', 'abraham', 'isaac', 'jacob', 'joseph'],
            'Exodus': ['moses', 'passover', 'tabernacle'],
            'Leviticus': ['priesthood', 'sacrifice'],
            'Numbers': ['moses'],
            'Deuteronomy': ['moses'],
            'Joshua': ['moses'],
            'Ruth': ['abraham'],  # Kinsman-redeemer
            '1 Samuel': ['david'],
            '2 Samuel': ['david'],
            '1 Kings': ['temple', 'david'],
            '2 Kings': ['prophets'],
            'Psalms': ['psalms', 'david'],
            'Proverbs': ['wisdom'],
            'Ecclesiastes': ['wisdom'],
            'Isaiah': ['prophets'],
            'Jeremiah': ['prophets', 'exile'],
            'Ezekiel': ['prophets', 'temple', 'exile'],
            'Daniel': ['prophets', 'exile'],
        }
        
        # Find applicable connection
        if book in book_to_key:
            for key in book_to_key[book]:
                if key in book_connections:
                    return book_connections[key]
        
        # Check themes in the verse for Christ connections
        themes = self._extract_themes(verse_text)
        theme_to_key = {
            'Covenant': 'abraham',
            'Sacrifice': 'passover',
            'Redemption': 'passover',
            'Kingdom': 'david',
            'Love': 'creation',
            'Faith': 'abraham',
            'Righteousness': 'priesthood',
            'Resurrection': 'creation',
            'Spirit': 'creation',
            'Prophecy': 'prophets',
            'Wisdom': 'wisdom',
            'Worship': 'temple',
            'Suffering': 'prophets'
        }
        
        for theme in themes:
            if theme in theme_to_key:
                key = theme_to_key[theme]
                if key in book_connections:
                    return book_connections[key]
        
        # Default Christ connection
        if self._is_old_testament(reference):
            return ("Every Old Testament passage points forward to Christ - either through direct prophecy, "
                   "typological foreshadowing, or revealing humanity's need for a Savior. "
                   "The Law shows our need; the sacrifices picture His atonement; the prophets announce His coming; "
                   "the wisdom literature reflects His character. As Jesus said, 'These are the Scriptures that testify about me' (John 5:39).")
        else:
            return ("This New Testament passage reveals Christ directly or through His Church. "
                   "The Gospels show His life; Acts shows His Spirit working; the Epistles explain His work; "
                   "Revelation shows His ultimate triumph. All Scripture centers on Him - the Alpha and Omega, "
                   "the author and finisher of our faith.")
    
    def _find_typological_connections(self, reference: str, verse_text: str) -> List[Dict]:
        """Find typological (type/antitype) connections"""
        connections = []
        
        for type_entry in self.typology_db.get('types', []):
            # Check if this verse is part of a typological relationship
            type_refs = type_entry['type'].get('references', [])
            antitype_refs = type_entry['antitype'].get('references', [])
            
            # Normalize reference format for comparison
            ref_normalized = reference.replace(' ', '').lower()
            
            is_type = any(ref_normalized in r.replace(' ', '').lower() for r in type_refs)
            is_antitype = any(ref_normalized in r.replace(' ', '').lower() for r in antitype_refs)
            
            if is_type or is_antitype:
                connections.append({
                    'type_name': type_entry['type']['name'],
                    'antitype_name': type_entry['antitype']['name'],
                    'type_refs': type_refs,
                    'antitype_refs': antitype_refs,
                    'connection_explanation': type_entry['connection'],
                    'church_fathers': type_entry.get('church_fathers', []),
                    'is_this_verse_type': is_type,
                    'is_this_verse_antitype': is_antitype
                })
            
            # Also check semantic similarity to type/antitype themes
            type_desc = type_entry['type'].get('description', '')
            antitype_desc = type_entry['antitype'].get('description', '')
            
            if type_desc and antitype_desc:
                sim_to_type = self.kernel.similarity(verse_text, type_desc)
                sim_to_antitype = self.kernel.similarity(verse_text, antitype_desc)
                
                if sim_to_type > 0.6 or sim_to_antitype > 0.6:
                    if not any(c['type_name'] == type_entry['type']['name'] for c in connections):
                        connections.append({
                            'type_name': type_entry['type']['name'],
                            'antitype_name': type_entry['antitype']['name'],
                            'type_refs': type_refs,
                            'antitype_refs': antitype_refs,
                            'connection_explanation': type_entry['connection'],
                            'church_fathers': type_entry.get('church_fathers', []),
                            'thematic_match': True,
                            'similarity': max(sim_to_type, sim_to_antitype)
                        })
        
        return connections[:5]  # Top 5 typological connections
    
    def _get_church_fathers_quotes(self, reference: str, verse_text: str) -> List[Dict]:
        """Get relevant Church Fathers quotes"""
        quotes = []
        
        # Direct verse match
        if reference in self.church_fathers_db.get('quotes_by_verse', {}):
            quotes.extend(self.church_fathers_db['quotes_by_verse'][reference])
        
        # Thematic match
        themes = self._extract_themes(verse_text)
        for theme in themes:
            theme_lower = theme.lower()
            if theme_lower in self.church_fathers_db.get('quotes_by_theme', {}):
                quotes.extend(self.church_fathers_db['quotes_by_theme'][theme_lower])
        
        # Remove duplicates based on quote text
        seen = set()
        unique_quotes = []
        for q in quotes:
            if q['quote'] not in seen:
                seen.add(q['quote'])
                unique_quotes.append(q)
        
        return unique_quotes[:5]  # Top 5 quotes
    
    def _get_fathers_for_connection(self, ref: str, verse_text: str, themes: List[str], max_quotes: int = 2) -> List[Dict]:
        """Get Church Fathers (or other) quotes relevant to this linked verse/theme for use in explaining the connection."""
        quotes = []
        # By verse (the connected reference)
        if ref and ref != "Unknown" and ref in self.church_fathers_db.get('quotes_by_verse', {}):
            quotes.extend(self.church_fathers_db['quotes_by_verse'][ref])
        # By theme (shared themes between the two passages)
        for theme in (themes or []):
            theme_lower = theme.lower()
            if theme_lower in self.church_fathers_db.get('quotes_by_theme', {}):
                quotes.extend(self.church_fathers_db['quotes_by_theme'][theme_lower])
        # Dedupe by quote text
        seen = set()
        unique = []
        for q in quotes:
            if q.get('quote') and q['quote'] not in seen:
                seen.add(q['quote'])
                unique.append(q)
        return unique[:max_quotes]
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extract theological themes from text"""
        text_lower = text.lower()
        found_themes = []
        
        for theme, keywords in self.theological_concepts.items():
            if any(kw in text_lower for kw in keywords):
                found_themes.append(theme.title())
        
        return found_themes
    
    def _get_historical_perspectives(self, reference: str, verse_text: str) -> Dict:
        """
        Get how this verse was understood across church history.
        Early Church -> Medieval -> Reformation -> Modern
        """
        # This would ideally pull from a larger database
        # For now, we provide a framework that can be expanded
        
        themes = self._extract_themes(verse_text)
        is_ot = self._is_old_testament(reference)
        
        perspectives = {
            'early_church': {
                'era': '100-500 AD',
                'approach': 'Allegorical and typological reading, seeing Christ throughout Scripture',
                'key_figures': ['Origen', 'Augustine', 'Chrysostom', 'Jerome'],
                'emphasis': 'The spiritual sense alongside the literal'
            },
            'medieval': {
                'era': '500-1500 AD',
                'approach': 'Four senses of Scripture (literal, allegorical, moral, anagogical)',
                'key_figures': ['Thomas Aquinas', 'Bernard of Clairvaux', 'Anselm'],
                'emphasis': 'Synthesis of faith and reason, systematic theology'
            },
            'reformation': {
                'era': '1500-1700 AD',
                'approach': 'Return to literal-grammatical sense, Scripture interprets Scripture',
                'key_figures': ['Luther', 'Calvin', 'Zwingli'],
                'emphasis': 'Sola Scriptura, the plain meaning of the text'
            },
            'modern': {
                'era': '1700-Present',
                'approach': 'Historical-critical methods alongside devotional reading',
                'key_figures': ['Various scholars and pastors'],
                'emphasis': 'Historical context, original audience, contemporary application'
            }
        }
        
        return perspectives
    
    def get_moses_to_jesus_connection(self, reference: str, verse_text: str) -> Dict:
        """
        Special method to trace how a verse connects to Moses and forward to Jesus.
        This addresses the user's specific desire to see these connections.
        """
        connections = {
            'moses_connections': [],
            'jesus_fulfillment': [],
            'connecting_thread': ''
        }
        
        # Find connections to Pentateuch (Moses' books)
        pentateuch = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']
        gospels = ['Matthew', 'Mark', 'Luke', 'John']
        
        for ref, text in self.bible_data.items():
            book = self._get_book_from_reference(ref)
            
            if book in pentateuch:
                sim = self.kernel.similarity(verse_text, text)
                if sim > 0.5:
                    connections['moses_connections'].append({
                        'reference': ref,
                        'text': text[:150] + '...' if len(text) > 150 else text,
                        'similarity': sim,
                        'explanation': self._explain_connection(verse_text, text, sim)
                    })
            
            elif book in gospels:
                sim = self.kernel.similarity(verse_text, text)
                if sim > 0.5:
                    connections['jesus_fulfillment'].append({
                        'reference': ref,
                        'text': text[:150] + '...' if len(text) > 150 else text,
                        'similarity': sim,
                        'explanation': self._explain_connection(verse_text, text, sim)
                    })
        
        # Sort by similarity
        connections['moses_connections'].sort(key=lambda x: x['similarity'], reverse=True)
        connections['jesus_fulfillment'].sort(key=lambda x: x['similarity'], reverse=True)
        
        # Keep top 5 of each
        connections['moses_connections'] = connections['moses_connections'][:5]
        connections['jesus_fulfillment'] = connections['jesus_fulfillment'][:5]
        
        # Generate connecting thread explanation
        if connections['moses_connections'] and connections['jesus_fulfillment']:
            connections['connecting_thread'] = (
                "This passage stands in the great river of salvation history: "
                "what Moses foreshadowed, Christ fulfilled. The types and shadows "
                "of the Old Testament find their substance in Jesus."
            )
        
        return connections
    
    def format_for_display(self, interconnected: InterconnectedVerse) -> str:
        """Format interconnections for display"""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"DEEP INTERCONNECTIONS: {interconnected.reference}")
        lines.append(f"{'='*60}\n")
        
        lines.append(f"TEXT: {interconnected.text}\n")
        
        # Themes
        if interconnected.themes:
            lines.append(f"THEMES: {', '.join(interconnected.themes)}\n")
        
        # Backward Links
        if interconnected.backward_links:
            lines.append("LOOKING BACK (Earlier Scripture this echoes):")
            lines.append("-" * 40)
            for conn in interconnected.backward_links:
                lines.append(f"  -> {conn.reference}")
                lines.append(f"     {conn.text[:100]}...")
                lines.append(f"     Connection: {conn.explanation}")
                lines.append("")
        
        # Forward Links
        if interconnected.forward_links:
            lines.append("LOOKING FORWARD (Later Scripture this points to):")
            lines.append("-" * 40)
            for conn in interconnected.forward_links:
                lines.append(f"  -> {conn.reference}")
                lines.append(f"     {conn.text[:100]}...")
                lines.append(f"     Connection: {conn.explanation}")
                lines.append("")
        
        # Typological
        if interconnected.typological:
            lines.append("TYPOLOGY (Type/Antitype Relationships):")
            lines.append("-" * 40)
            for typ in interconnected.typological:
                lines.append(f"  {typ['type_name']} -> {typ['antitype_name']}")
                lines.append(f"  {typ['connection_explanation']}")
                lines.append("")
        
        # Church Fathers
        if interconnected.church_fathers:
            lines.append("CHURCH FATHERS:")
            lines.append("-" * 40)
            for quote in interconnected.church_fathers:
                lines.append(f"  \"{quote['quote']}\"")
                lines.append(f"  - {quote['author']}, {quote.get('work', '')}")
                lines.append("")
        
        lines.append(f"{'='*60}\n")
        
        return '\n'.join(lines)


# Convenience function
def get_interconnections(reference: str, verse_text: str, bible_data: Dict = None) -> InterconnectedVerse:
    """Get interconnections for a verse"""
    engine = InterconnectionEngine(bible_data)
    return engine.get_interconnections(reference, verse_text)


if __name__ == "__main__":
    # Test the engine
    engine = InterconnectionEngine()
    
    # Test with John 3:16
    result = engine.get_interconnections(
        "John 3:16",
        "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."
    )
    
    print(engine.format_for_display(result))
