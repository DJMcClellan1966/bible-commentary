"""
API endpoints for Quantum AI System
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
from models import get_db
from quantum_ai_implementation import QuantumAISystem
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/quantum-ai", tags=["quantum-ai"])

# Global quantum AI system instance
_quantum_ai: Optional[QuantumAISystem] = None


def get_quantum_ai() -> QuantumAISystem:
    """Get or create quantum AI system instance"""
    global _quantum_ai
    if _quantum_ai is None:
        _quantum_ai = QuantumAISystem(num_qubits=12, vocab_size=1000, d_model=256)
        logger.info("Quantum AI system initialized")
    return _quantum_ai


# Pydantic models
class MemoryStoreRequest(BaseModel):
    key: str
    value: str
    importance: float = 1.0


class MemoryRecallRequest(BaseModel):
    query: str
    top_k: int = 5


class ReasoningRequest(BaseModel):
    premises: List[str]
    conclusion: str


class GenerateRequest(BaseModel):
    prompt: str
    use_memory: bool = True
    use_reasoning: bool = True
    max_length: int = 100


class TrainRequest(BaseModel):
    examples: List[Dict[str, str]]  # [{"input": "...", "output": "..."}]
    epochs: int = 5


@router.get("/status")
async def get_status():
    """Get quantum AI system status"""
    try:
        ai = get_quantum_ai()
        return {
            "status": "active",
            "num_qubits": ai.num_qubits,
            "vocab_size": ai.vocab_size if ai.tokenizer else 0,
            "memory_count": len(ai.quantum_memory),
            "tokenizer_initialized": ai.tokenizer is not None,
            "model_initialized": ai.model is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/memory/store")
async def store_memory(request: MemoryStoreRequest):
    """Store information in quantum memory"""
    try:
        ai = get_quantum_ai()
        ai.quantum_memory_store(request.key, request.value, request.importance)
        return {
            "success": True,
            "key": request.key,
            "message": "Memory stored successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/memory/recall")
async def recall_memory(request: MemoryRecallRequest):
    """Recall relevant memories using quantum search"""
    try:
        ai = get_quantum_ai()
        memories = ai.quantum_memory_recall(request.query, request.top_k)
        return {
            "query": request.query,
            "memories": memories,
            "count": len(memories)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memory/list")
async def list_memories(
    limit: int = Query(50, ge=1, le=1000)
):
    """List all stored memories"""
    try:
        ai = get_quantum_ai()
        memories = []
        for key, memory in list(ai.quantum_memory.items())[:limit]:
            memories.append({
                "key": key,
                "text": memory.get("text", ""),
                "importance": memory.get("importance", 1.0)
            })
        return {
            "memories": memories,
            "total": len(ai.quantum_memory),
            "returned": len(memories)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reasoning")
async def quantum_reasoning(request: ReasoningRequest):
    """Perform quantum logical reasoning"""
    try:
        ai = get_quantum_ai()
        result = ai.quantum_reasoning(request.premises, request.conclusion)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_response(request: GenerateRequest):
    """Generate response using full quantum AI system"""
    try:
        ai = get_quantum_ai()
        result = ai.generate_quantum_response(
            request.prompt,
            use_memory=request.use_memory,
            use_reasoning=request.use_reasoning,
            max_length=request.max_length
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train")
async def train_system(request: TrainRequest):
    """Train the quantum AI system"""
    try:
        ai = get_quantum_ai()
        
        # Convert to training format
        training_data = [
            (ex["input"], ex["output"])
            for ex in request.examples
            if "input" in ex and "output" in ex
        ]
        
        if not training_data:
            raise HTTPException(
                status_code=400,
                detail="Invalid training data format. Expected [{'input': '...', 'output': '...'}]"
            )
        
        result = ai.train(training_data, epochs=request.epochs)
        
        return {
            "success": True,
            "examples_processed": len(training_data),
            "efficiency_gain": result.get("efficiency_gain", 0),
            "message": "Training completed successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn")
async def quantum_learn(request: TrainRequest):
    """Efficient quantum learning from examples"""
    try:
        ai = get_quantum_ai()
        
        # Convert to training format
        training_data = [
            (ex["input"], ex["output"])
            for ex in request.examples
            if "input" in ex and "output" in ex
        ]
        
        if not training_data:
            raise HTTPException(
                status_code=400,
                detail="Invalid training data format"
            )
        
        result = ai.quantum_learning(training_data, epochs=request.epochs)
        
        return {
            "success": True,
            "examples_processed": len(training_data),
            "classical_iterations": result.get("classical_iterations", 0),
            "quantum_iterations": result.get("quantum_iterations", 0),
            "efficiency_gain": result.get("efficiency_gain", 0),
            "message": "Quantum learning completed"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/memory/{key}")
async def delete_memory(key: str):
    """Delete a memory by key"""
    try:
        ai = get_quantum_ai()
        if key in ai.quantum_memory:
            del ai.quantum_memory[key]
            return {
                "success": True,
                "key": key,
                "message": "Memory deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Memory not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/memory")
async def clear_all_memories():
    """Clear all memories"""
    try:
        ai = get_quantum_ai()
        count = len(ai.quantum_memory)
        ai.quantum_memory.clear()
        ai.memory_entanglement_matrix = None
        return {
            "success": True,
            "memories_cleared": count,
            "message": "All memories cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
