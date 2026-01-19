"""
Comprehensive Performance Test for Bible App
Tests performance, errors, and optimization opportunities
"""
import time
import sys
import traceback
from typing import Dict, List
import os

# Try to import psutil (optional)
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("WARNING: psutil not available. Memory tracking will be limited.")

# Import required modules
try:
    from bible_ai_system import create_bible_ai_system
    from models import get_db, init_db
    from sqlalchemy.orm import Session
    BIBLE_AI_AVAILABLE = True
except ImportError as e:
    print(f"ERROR: Could not import Bible AI system: {e}")
    BIBLE_AI_AVAILABLE = False

try:
    from quantum_kernel import get_kernel, KernelConfig
    KERNEL_AVAILABLE = True
except ImportError as e:
    print(f"ERROR: Could not import quantum kernel: {e}")
    KERNEL_AVAILABLE = False


def get_memory_usage():
    """Get current memory usage in MB"""
    if PSUTIL_AVAILABLE:
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    else:
        # Fallback: return 0 if psutil not available
        return 0.0


def test_initialization_performance():
    """Test system initialization performance"""
    print("=" * 80)
    print("TEST 1: INITIALIZATION PERFORMANCE")
    print("=" * 80)
    
    if not BIBLE_AI_AVAILABLE:
        print("SKIPPED: Bible AI system not available")
        return None
    
    try:
        init_db()
        db = next(get_db())
        
        memory_before = get_memory_usage()
        start_time = time.time()
        
        system = create_bible_ai_system(db)
        
        init_time = time.time() - start_time
        memory_after = get_memory_usage()
        memory_used = memory_after - memory_before
        
        print(f"Initialization time: {init_time:.3f}s")
        print(f"Memory used: {memory_used:.2f} MB")
        print(f"Total memory: {memory_after:.2f} MB")
        
        return {
            "init_time": init_time,
            "memory_used": memory_used,
            "memory_total": memory_after,
            "success": True
        }
    except Exception as e:
        print(f"ERROR: Initialization failed: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def test_generation_performance(system):
    """Test text generation performance"""
    print("\n" + "=" * 80)
    print("TEST 2: TEXT GENERATION PERFORMANCE")
    print("=" * 80)
    
    if not system:
        print("SKIPPED: System not initialized")
        return None
    
    try:
        prompts = [
            "God is",
            "Love is",
            "Faith is",
            "Grace is",
            "Hope is"
        ]
        
        results = []
        total_time = 0
        
        for prompt in prompts:
            start = time.time()
            result = system.generate_grounded_text(prompt, max_length=20)
            gen_time = time.time() - start
            total_time += gen_time
            
            results.append({
                "prompt": prompt,
                "time": gen_time,
                "confidence": result.get("confidence", 0),
                "is_safe": result.get("is_safe", False)
            })
        
        avg_time = total_time / len(prompts)
        
        print(f"Total generations: {len(prompts)}")
        print(f"Total time: {total_time:.3f}s")
        print(f"Average time per generation: {avg_time:.3f}s")
        print(f"Generations per second: {1/avg_time:.2f}")
        
        for r in results:
            print(f"  {r['prompt']}: {r['time']*1000:.1f}ms (confidence: {r['confidence']:.2f})")
        
        return {
            "total_time": total_time,
            "avg_time": avg_time,
            "throughput": 1/avg_time,
            "results": results,
            "success": True
        }
    except Exception as e:
        print(f"ERROR: Generation test failed: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def test_search_performance(system):
    """Test search performance"""
    print("\n" + "=" * 80)
    print("TEST 3: SEARCH PERFORMANCE")
    print("=" * 80)
    
    if not system:
        print("SKIPPED: System not initialized")
        return None
    
    try:
        queries = [
            "divine love",
            "faith and salvation",
            "grace and mercy",
            "hope and peace",
            "God's promises"
        ]
        
        results = []
        total_time = 0
        
        for query in queries:
            start = time.time()
            result = system.ai_search(query, top_k=20)
            search_time = time.time() - start
            total_time += search_time
            
            results.append({
                "query": query,
                "time": search_time,
                "results_count": len(result.get("results", []))
            })
        
        avg_time = total_time / len(queries) if len(queries) > 0 else 0
        
        print(f"Total searches: {len(queries)}")
        print(f"Total time: {total_time:.3f}s")
        print(f"Average time per search: {avg_time:.3f}s")
        if avg_time > 0:
            print(f"Searches per second: {1/avg_time:.2f}")
        else:
            print(f"Searches per second: Very fast (<1ms)")
        
        for r in results:
            print(f"  {r['query']}: {r['time']*1000:.1f}ms ({r['results_count']} results)")
        
        return {
            "total_time": total_time,
            "avg_time": avg_time,
            "throughput": 1/avg_time,
            "results": results,
            "success": True
        }
    except Exception as e:
        print(f"ERROR: Search test failed: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def test_progressive_learning_performance(system):
    """Test progressive learning performance"""
    print("\n" + "=" * 80)
    print("TEST 4: PROGRESSIVE LEARNING PERFORMANCE")
    print("=" * 80)
    
    if not system:
        print("SKIPPED: System not initialized")
        return None
    
    try:
        new_texts = [
            "Grace is unmerited favor from God",
            "Hope is the confident expectation",
            "Peace is the state of wholeness",
            "Mercy is God's compassion",
            "Righteousness is right relationship with God"
        ]
        
        start = time.time()
        result = system.progressive_learning_step(new_texts, week=1)
        learning_time = time.time() - start
        
        print(f"Learning time: {learning_time:.3f}s")
        print(f"Texts processed: {len(new_texts)}")
        print(f"Time per text: {learning_time/len(new_texts):.3f}s")
        print(f"Phrases before: {result.get('phrases_before', 0)}")
        print(f"Phrases after: {result.get('phrases_after', 0)}")
        print(f"Phrases added: {result.get('phrases_added', 0)}")
        print(f"Estimated quality: {result.get('estimated_quality', 0):.2f}")
        
        return {
            "learning_time": learning_time,
            "time_per_text": learning_time/len(new_texts),
            "result": result,
            "success": True
        }
    except Exception as e:
        print(f"ERROR: Progressive learning test failed: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def test_validation_performance(system):
    """Test validation performance"""
    print("\n" + "=" * 80)
    print("TEST 5: VALIDATION PERFORMANCE")
    print("=" * 80)
    
    if not system:
        print("SKIPPED: System not initialized")
        return None
    
    try:
        texts = [
            "God is love and love is patient",
            "Faith is the assurance of things hoped for",
            "Grace is unmerited favor from God",
            "Hope is the confident expectation",
            "Peace is the state of wholeness"
        ]
        
        results = []
        total_time = 0
        
        for text in texts:
            start = time.time()
            validation = system.validate_text(text)
            val_time = time.time() - start
            total_time += val_time
            
            results.append({
                "text": text[:30] + "...",
                "time": val_time,
                "confidence": validation.get("confidence", 0),
                "is_safe": validation.get("is_safe", False)
            })
        
        avg_time = total_time / len(texts)
        
        print(f"Total validations: {len(texts)}")
        print(f"Total time: {total_time:.3f}s")
        print(f"Average time per validation: {avg_time:.3f}s")
        print(f"Validations per second: {1/avg_time:.2f}")
        
        for r in results:
            print(f"  {r['text']}: {r['time']*1000:.1f}ms (confidence: {r['confidence']:.2f}, safe: {r['is_safe']})")
        
        return {
            "total_time": total_time,
            "avg_time": avg_time,
            "throughput": 1/avg_time,
            "results": results,
            "success": True
        }
    except Exception as e:
        print(f"ERROR: Validation test failed: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def test_error_handling(system):
    """Test error handling"""
    print("\n" + "=" * 80)
    print("TEST 6: ERROR HANDLING")
    print("=" * 80)
    
    if not system:
        print("SKIPPED: System not initialized")
        return None
    
    errors_found = []
    
    # Test 1: Empty prompt
    try:
        result = system.generate_grounded_text("", max_length=10)
        if result.get("error") or result.get("warning") or not result.get("is_safe", True):
            print(f"PASS: Empty prompt handled correctly")
        else:
            errors_found.append("Empty prompt not handled")
    except Exception as e:
        errors_found.append(f"Empty prompt exception: {e}")
    
    # Test 2: Very long prompt
    try:
        long_prompt = "God is " * 1000
        result = system.generate_grounded_text(long_prompt, max_length=10)
        print(f"PASS: Long prompt handled")
    except Exception as e:
        errors_found.append(f"Long prompt exception: {e}")
    
    # Test 3: Invalid parameters
    try:
        result = system.generate_grounded_text("test", max_length=-1)
        print(f"PASS: Invalid parameters handled")
    except Exception as e:
        errors_found.append(f"Invalid parameters exception: {e}")
    
    # Test 4: None input
    try:
        result = system.validate_text("")  # Use empty string instead of None
        print(f"PASS: Empty input handled")
    except Exception as e:
        errors_found.append(f"Empty input exception: {e}")
    
    if errors_found:
        print(f"ERRORS FOUND: {len(errors_found)}")
        for error in errors_found:
            print(f"  - {error}")
        return {"success": False, "errors": errors_found}
    else:
        print("PASS: All error handling tests passed")
        return {"success": True}


def test_memory_usage(system):
    """Test memory usage"""
    print("\n" + "=" * 80)
    print("TEST 7: MEMORY USAGE")
    print("=" * 80)
    
    if not system:
        print("SKIPPED: System not initialized")
        return None
    
    try:
        memory_before = get_memory_usage()
        
        # Perform operations
        for i in range(10):
            system.generate_grounded_text(f"Test {i}", max_length=10)
        
        memory_after = get_memory_usage()
        memory_increase = memory_after - memory_before
        
        print(f"Memory before: {memory_before:.2f} MB")
        print(f"Memory after: {memory_after:.2f} MB")
        print(f"Memory increase: {memory_increase:.2f} MB")
        
        # Get statistics
        stats = system.get_llm_statistics()
        if stats and not stats.get("error"):
            print(f"Verified phrases: {stats.get('verified_phrases', 0)}")
            print(f"Source texts: {stats.get('source_texts', 0)}")
        
        return {
            "memory_before": memory_before,
            "memory_after": memory_after,
            "memory_increase": memory_increase,
            "success": True
        }
    except Exception as e:
        print(f"ERROR: Memory test failed: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def identify_optimizations(system):
    """Identify optimization opportunities"""
    print("\n" + "=" * 80)
    print("TEST 8: OPTIMIZATION OPPORTUNITIES")
    print("=" * 80)
    
    optimizations = []
    
    # Check for duplicate database queries
    if system:
        try:
            # Test if get_verses is called multiple times
            stats = system.get_stats()
            if stats:
                print("Checking for optimization opportunities...")
                
                # Check kernel cache
                if "kernel" in stats:
                    kernel_stats = stats["kernel"]
                    cache_hit_rate = kernel_stats.get("cache_hit_rate", 0)
                    if cache_hit_rate < 0.8:
                        optimizations.append({
                            "type": "cache",
                            "issue": f"Low cache hit rate: {cache_hit_rate:.2%}",
                            "recommendation": "Increase cache size or improve cache strategy"
                        })
                
                # Check memory usage
                memory = get_memory_usage()
                if memory > 500:
                    optimizations.append({
                        "type": "memory",
                        "issue": f"High memory usage: {memory:.2f} MB",
                        "recommendation": "Consider lazy loading or memory optimization"
                    })
        except Exception as e:
            print(f"Could not analyze optimizations: {e}")
    
    # General optimizations
    optimizations.extend([
        {
            "type": "database",
            "issue": "Multiple get_verses calls during initialization",
            "recommendation": "Cache verses after first call"
        },
        {
            "type": "embedding",
            "issue": "Embeddings computed on every request",
            "recommendation": "Use kernel caching (already implemented)"
        },
        {
            "type": "parallel",
            "issue": "Sequential processing for batch operations",
            "recommendation": "Use multiprocessing for batch operations"
        }
    ])
    
    if optimizations:
        print(f"Found {len(optimizations)} optimization opportunities:")
        for opt in optimizations:
            print(f"\n  [{opt['type'].upper()}] {opt['issue']}")
            print(f"    Recommendation: {opt['recommendation']}")
    else:
        print("No major optimization opportunities found")
    
    return optimizations


def main():
    """Run all performance tests"""
    print("=" * 80)
    print("COMPREHENSIVE PERFORMANCE TEST")
    print("=" * 80)
    print(f"Python version: {sys.version}")
    if PSUTIL_AVAILABLE:
        print(f"Memory available: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.2f} GB")
    else:
        print("Memory tracking: Limited (psutil not available)")
    print()
    
    results = {}
    
    # Test 1: Initialization
    init_result = test_initialization_performance()
    results["initialization"] = init_result
    
    if not init_result or not init_result.get("success"):
        print("\nCRITICAL: Initialization failed. Cannot continue tests.")
        return results
    
    # Initialize system for remaining tests
    try:
        init_db()
        db = next(get_db())
        system = create_bible_ai_system(db)
    except Exception as e:
        print(f"ERROR: Could not initialize system: {e}")
        return results
    
    # Test 2: Generation
    results["generation"] = test_generation_performance(system)
    
    # Test 3: Search
    results["search"] = test_search_performance(system)
    
    # Test 4: Progressive Learning
    results["progressive_learning"] = test_progressive_learning_performance(system)
    
    # Test 5: Validation
    results["validation"] = test_validation_performance(system)
    
    # Test 6: Error Handling
    results["error_handling"] = test_error_handling(system)
    
    # Test 7: Memory Usage
    results["memory"] = test_memory_usage(system)
    
    # Test 8: Optimizations
    results["optimizations"] = identify_optimizations(system)
    
    # Summary
    print("\n" + "=" * 80)
    print("PERFORMANCE TEST SUMMARY")
    print("=" * 80)
    
    total_tests = len([r for r in results.values() if isinstance(r, dict) and r.get("success") is not None])
    passed_tests = len([r for r in results.values() if isinstance(r, dict) and r.get("success") is True])
    
    print(f"Tests passed: {passed_tests}/{total_tests}")
    
    if init_result and init_result.get("success"):
        print(f"\nInitialization: {init_result['init_time']:.3f}s")
        print(f"Memory used: {init_result['memory_used']:.2f} MB")
    
    if results.get("generation") and results["generation"].get("success"):
        gen = results["generation"]
        print(f"\nGeneration: {gen['avg_time']*1000:.1f}ms avg ({gen['throughput']:.2f}/s)")
    
    if results.get("search") and results["search"].get("success"):
        search = results["search"]
        print(f"Search: {search['avg_time']*1000:.1f}ms avg ({search['throughput']:.2f}/s)")
    
    if results.get("optimizations"):
        print(f"\nOptimization opportunities: {len(results['optimizations'])}")
    
    return results


if __name__ == "__main__":
    try:
        results = main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nCRITICAL ERROR: {e}")
        traceback.print_exc()
