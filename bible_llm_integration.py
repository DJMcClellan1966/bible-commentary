"""
Best LLM Integration for Bible App
Integrates high-quality LLM with quantum learning system
"""
from typing import Optional, Dict, List
import logging
from agent import BibleCommentaryAgent
from bible_ai_system import BibleAISystem
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BibleLLMIntegration:
    """
    Best LLM integration for Bible app
    Supports multiple LLM providers and quantum learning
    """
    
    def __init__(self, bible_ai_system: BibleAISystem):
        self.bible_ai = bible_ai_system
        self.llm_agent = BibleCommentaryAgent()
        self.llm_provider = None
        self.llm_model = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the best available LLM"""
        # Priority order: OpenAI GPT-4 > GPT-3.5 > Anthropic Claude > Open Source
        
        # Try OpenAI GPT-4 (best for Bible study)
        if os.getenv("OPENAI_API_KEY"):
            try:
                from langchain_openai import ChatOpenAI
                self.llm_provider = "openai"
                self.llm_model = "gpt-4"  # Best quality
                self.llm_agent.llm = ChatOpenAI(
                    model="gpt-4",
                    temperature=0.7,
                    max_tokens=1000
                )
                logger.info("Initialized OpenAI GPT-4 (best quality)")
                return
            except Exception as e:
                logger.warning(f"Could not initialize GPT-4: {e}")
        
        # Try OpenAI GPT-3.5 (faster, cheaper)
        if os.getenv("OPENAI_API_KEY"):
            try:
                from langchain_openai import ChatOpenAI
                self.llm_provider = "openai"
                self.llm_model = "gpt-3.5-turbo"
                self.llm_agent.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    max_tokens=1000
                )
                logger.info("Initialized OpenAI GPT-3.5-turbo")
                return
            except Exception as e:
                logger.warning(f"Could not initialize GPT-3.5: {e}")
        
        # Try Anthropic Claude (good alternative)
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                from langchain_anthropic import ChatAnthropic
                self.llm_provider = "anthropic"
                self.llm_model = "claude-3-opus"  # Best Claude model
                self.llm_agent.llm = ChatAnthropic(
                    model="claude-3-opus-20240229",
                    temperature=0.7,
                    max_tokens=1000
                )
                logger.info("Initialized Anthropic Claude")
                return
            except Exception as e:
                logger.warning(f"Could not initialize Claude: {e}")
        
        # Fallback: No LLM available
        logger.warning("No LLM API key found. Using quantum-only mode.")
        self.llm_provider = None
        self.llm_model = None
    
    def generate_with_llm(self, prompt: str, context: Optional[str] = None) -> Dict:
        """
        Generate text using best available LLM
        Automatically learns from output to improve quantum generation
        """
        if not self.llm_agent.llm:
            return {
                "error": "No LLM available",
                "suggestion": "Use quantum generation instead"
            }
        
        try:
            from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain
            
            # Create Bible-focused prompt
            template = PromptTemplate(
                input_variables=["prompt", "context"],
                template="""You are a Bible study assistant. Given the context and prompt, provide a thoughtful, 
                theologically sound response that helps with Bible study.

                Context: {context}
                Prompt: {prompt}

                Provide a clear, helpful response:"""
            )
            
            chain = LLMChain(llm=self.llm_agent.llm, prompt=template)
            context_text = context or "Bible study"
            result = chain.run(prompt=prompt, context=context_text)
            
            llm_output = result.strip()
            
            # Automatically learn from LLM output
            if self.bible_ai.text_generator:
                learn_result = self.bible_ai.learn_from_llm_output(prompt, llm_output)
                logger.info(f"Learned from LLM output (vocab: {learn_result.get('vocab_size', 0)})")
            
            return {
                "prompt": prompt,
                "generated": llm_output,
                "method": "llm",
                "provider": self.llm_provider,
                "model": self.llm_model,
                "learned": True
            }
            
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return {
                "error": str(e),
                "fallback": "Use quantum generation"
            }
    
    def generate_hybrid(self, prompt: str, use_llm: bool = True, use_quantum: bool = True) -> Dict:
        """
        Generate using both LLM and quantum, combine best results
        """
        results = {}
        
        # LLM generation (if available and requested)
        if use_llm and self.llm_agent.llm:
            llm_result = self.generate_with_llm(prompt)
            results["llm"] = llm_result
        
        # Quantum generation (if requested)
        if use_quantum and self.bible_ai.text_generator:
            quantum_result = self.bible_ai.generate_text(prompt, max_length=50, temperature=0.7)
            results["quantum"] = quantum_result
        
        # Combine results
        if "llm" in results and "quantum" in results:
            return {
                "prompt": prompt,
                "llm_output": results["llm"].get("generated", ""),
                "quantum_output": results["quantum"].get("generated", ""),
                "recommended": results["llm"].get("generated", "") if "llm" in results else results["quantum"].get("generated", ""),
                "method": "hybrid",
                "llm_available": self.llm_agent.llm is not None,
                "quantum_available": self.bible_ai.text_generator is not None
            }
        elif "llm" in results:
            return results["llm"]
        elif "quantum" in results:
            return results["quantum"]
        else:
            return {"error": "No generation method available"}
    
    def translate_with_llm(self, text: str, source_lang: str = "en", target_lang: str = "es") -> Dict:
        """
        Translate using LLM (better quality than quantum for general translation)
        Also learns from LLM output for quantum improvement
        """
        if not self.llm_agent.llm:
            # Fallback to quantum translation
            return self.bible_ai.translate_text(text, source_lang, target_lang)
        
        try:
            from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain
            
            template = PromptTemplate(
                input_variables=["text", "source_lang", "target_lang"],
                template="Translate the following {source_lang} text to {target_lang}. Provide only the translation, no explanation.\n\nText: {text}\n\nTranslation:"
            )
            
            chain = LLMChain(llm=self.llm_agent.llm, prompt=template)
            translation = chain.run(text=text, source_lang=source_lang, target_lang=target_lang)
            
            translation = translation.strip()
            
            # Learn translation pair for quantum
            if self.bible_ai.translator:
                self.bible_ai.translator.add_bilingual_pair(text, translation, source_lang, target_lang)
                logger.info(f"Learned translation pair for quantum")
            
            return {
                "original": text,
                "translation": translation,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "method": "llm",
                "provider": self.llm_provider,
                "model": self.llm_model,
                "quantum_learned": True
            }
            
        except Exception as e:
            logger.error(f"LLM translation error: {e}")
            # Fallback to quantum
            return self.bible_ai.translate_text(text, source_lang, target_lang)
    
    def get_status(self) -> Dict:
        """Get LLM integration status"""
        return {
            "llm_available": self.llm_agent.llm is not None,
            "provider": self.llm_provider,
            "model": self.llm_model,
            "quantum_available": self.bible_ai.text_generator is not None,
            "quantum_translator_available": self.bible_ai.translator is not None,
            "learning_enabled": True
        }


def create_bible_llm_integration(bible_ai_system: BibleAISystem) -> BibleLLMIntegration:
    """Factory function to create Bible LLM Integration"""
    return BibleLLMIntegration(bible_ai_system)
