#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Caller — Unified wrapper for OpenRouter API (Gemini 2.0 Flash).
Used by: pt_auto_evidence.py, intercoder_llm.py, temporal_var_refinement.py, sfc_h4_enrichment.py
"""

import sys, json, os, time, requests
sys.stdout.reconfigure(encoding='utf-8')

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Task-specific model routing (Dexter Router pattern)
# PAID MODE: Free tier upstream (Qwen) is rate-limited (429).
# Switched to paid models with best benchmarks. Budget: $9.29 remaining.
# Cost estimate: ~114 codings × 500 tokens × $0.10/M = $0.006 (Gemini Flash)
#                or × $2/M = $0.11 (Gemini Pro)
MODEL_ROUTER = {
    "default":          "google/gemini-2.0-flash-001",       # $0.10/M, reliable, 1M context
    "evidence_extract": "google/gemini-2.0-flash-001",       # $0.10/M, fast + quality
    "legal_reasoning":  "deepseek/deepseek-v3.2",           # $0.26/M, strong reasoning
    "intercoder_code":  "deepseek/deepseek-v3.2",           # $0.26/M, best calibration
    "deep_research":    "google/gemini-3.1-pro-preview",     # $2/M, best quality
    "quick_classify":   "google/gemini-2.0-flash-001",       # $0.10/M, fast
    "sfc_enrich":       "google/gemini-2.0-flash-001",       # $0.10/M, PT quality
    "temporal_assess":  "deepseek/deepseek-v3.2",           # $0.26/M, reasoning
    # Fallbacks
    "fallback_paid":    "google/gemini-2.0-flash-001",       # $0.10/M, reliable
    "fallback_quality": "google/gemini-3.1-pro-preview",     # $2/M, best quality
}

# Quality mode: maximum quality regardless of cost (for critical codings)
# Use with LLMCaller(task="evidence_extract", quality_mode=True)
MODEL_ROUTER_QUALITY = {
    "default":          "google/gemini-3.1-pro-preview",     # $2/M, best overall
    "evidence_extract": "google/gemini-3.1-pro-preview",     # $2/M, 1M context
    "legal_reasoning":  "google/gemini-3.1-pro-preview",     # $2/M, deep reasoning
    "intercoder_code":  "deepseek/deepseek-v3.2",           # $0.26/M, calibration
    "deep_research":    "google/gemini-3.1-pro-preview",     # $2/M, best quality
    "quick_classify":   "google/gemini-2.0-flash-001",       # $0.10/M, fast+quality
    "sfc_enrich":       "deepseek/deepseek-v3.2",           # $0.26/M, quality PT
    "temporal_assess":  "google/gemini-3.1-pro-preview",     # $2/M, reasoning
    "fallback_paid":    "google/gemini-3.1-pro-preview",     # $2/M
    "fallback_quality": "google/gemini-3.1-pro-preview",     # $2/M
}

MODEL = MODEL_ROUTER["default"]

# Add tools to path for hybrid_search
TOOLS_DIR = "os.environ.get("TOOLS_DIR", "./tools")"
sys.path.insert(0, TOOLS_DIR)

class LLMCaller:
    def __init__(self, api_key=OPENROUTER_API_KEY, model=None, task="default",
                 use_mab=False, quality_mode=False):
        self.api_key = api_key
        self.default_task = task
        self.quality_mode = quality_mode
        router = MODEL_ROUTER_QUALITY if quality_mode else MODEL_ROUTER
        self.model = model or router.get(task, MODEL)
        self.total_tokens = 0
        self.total_calls = 0
        self.errors = 0
        self.models_used = {}
        self.use_mab = use_mab
        self._mab_router = None
        if use_mab:
            try:
                from mab_router import get_global_router
                self._mab_router = get_global_router()
                print(f"[MAB] Thompson Sampling router activated")
            except ImportError:
                print("[MAB] mab_router.py not found, falling back to static routing")
                self.use_mab = False

    def _get_model(self, task=None):
        """Get model for task. Priority: MAB > quality_mode > static routing."""
        t = task or self.default_task
        if self.use_mab and self._mab_router:
            arm = self._mab_router.select_model(t)
            return self._mab_router.get_model_id(arm)
        router = MODEL_ROUTER_QUALITY if self.quality_mode else MODEL_ROUTER
        model = router.get(t, MODEL)
        return model

    def _update_mab_reward(self, task, model, reward):
        """Update MAB router with reward signal after a call."""
        if self.use_mab and self._mab_router:
            try:
                from mab_router import ARMS
                arm = None
                for key, cfg in ARMS.items():
                    if cfg["model"] == model:
                        arm = key
                        break
                if arm:
                    self._mab_router.update(task or self.default_task, arm, reward)
            except Exception:
                pass

    def call(self, prompt, system_prompt=None, max_tokens=2000, temperature=0.3, task=None):
        """Call OpenRouter API with Gemini 2.0 Flash."""
        model = self._get_model(task)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=60
            )

            self.total_calls += 1

            if response.status_code == 200:
                data = response.json()
                answer = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                tokens = usage.get("total_tokens", 0)
                self.total_tokens += tokens
                actual_model = data.get("model", model)
                self.models_used[actual_model] = self.models_used.get(actual_model, 0) + 1
                # MAB: reward based on response format quality
                if self.use_mab:
                    from mab_router import MABRouter
                    reward = MABRouter.compute_format_reward(answer)
                    self._update_mab_reward(task, model, reward)
                return answer.strip()
            else:
                self.errors += 1
                # MAB: penalize errors
                if self.use_mab:
                    self._update_mab_reward(task, model, 0.0)
                return f"[ERROR {response.status_code}]: {response.text[:200]}"

        except Exception as e:
            self.errors += 1
            if self.use_mab:
                self._update_mab_reward(task, model, 0.0)
            return f"[ERROR]: {str(e)}"

    def code_fuzzy_variable(self, case_description, calibration_guide, variable_name):
        """LLM as fuzzy coder: returns a 7-point fuzzy score."""
        system = (
            "You are a research assistant coding tailings dam cases for a QCA study. "
            "You must return ONLY a single number from this scale: "
            "0, 0.17, 0.33, 0.50, 0.67, 0.83, 1.00. "
            "No explanations, no text — just the number."
        )
        prompt = (
            f"Case description:\n{case_description}\n\n"
            f"Calibration guide for {variable_name}:\n{calibration_guide}\n\n"
            f"Rate this case on {variable_name}. Return ONLY the fuzzy score."
        )
        answer = self.call(prompt, system_prompt=system, max_tokens=10, temperature=0.1)

        # Parse to float
        try:
            val = float(answer.strip())
            valid = [0, 0.17, 0.33, 0.50, 0.67, 0.83, 1.00]
            closest = min(valid, key=lambda x: abs(x - val))
            return closest
        except:
            return 0.50  # default to crossover if parsing fails

    def search_and_assess(self, query, context=""):
        """Search bibliography + assess evidence quality."""
        system = (
            "You are a research assistant for a doctoral thesis on regulatory catastrophes "
            "in tailings dams. Analyze the search results and extract evidence relevant to "
            "the query. For each piece of evidence, assess:\n"
            "1. Source reliability (primary/secondary)\n"
            "2. Relevance to the mechanism (P1-P4)\n"
            "3. Van Evera test type (hoop, smoking_gun, straw_in_wind, doubly_decisive)\n"
            "4. Sensitivity (0.40-0.95)\n"
            "5. Type I error (0.01-0.30)\n"
            "Return a JSON array of evidence items."
        )
        prompt = f"Query: {query}\n\nContext: {context}\n\nExtract structured evidence."
        return self.call(prompt, system_prompt=system, max_tokens=2000, temperature=0.2)

    def enrich_sfc_response(self, jurisdiction, question, current_response, evidence):
        """Enrich SFC H4 response with new evidence."""
        system = (
            "You are writing responses for a Structured Focused Comparison (SFC) analysis "
            "of tailings dam regulation across jurisdictions. Responses must be in Portuguese, "
            "100-400 characters, and contain classifiable keywords for automated coding."
        )
        prompt = (
            f"Jurisdiction: {jurisdiction}\n"
            f"Question: {question}\n"
            f"Current response: {current_response}\n"
            f"New evidence found: {evidence}\n\n"
            f"Write an improved response in Portuguese that incorporates the new evidence. "
            f"Keep it 100-400 chars and include keywords that match QCA coding rules."
        )
        return self.call(prompt, system_prompt=system, max_tokens=500, temperature=0.3)

    def stats(self):
        """Return usage statistics."""
        cost = self.total_tokens * 0.000002  # ~$0.002 per 1K tokens
        return {
            "total_calls": self.total_calls,
            "total_tokens": self.total_tokens,
            "errors": self.errors,
            "estimated_cost_usd": round(cost, 4)
        }


# Convenience: hybrid_search integration
def search_bibliography(query, n_results=10):
    """Search 1,093 indexed PDFs via hybrid_search."""
    try:
        from hybrid_search import HybridSearchEngine
        engine = HybridSearchEngine()
        results = engine.search(query, n_results=n_results, mode="hybrid")
        return results
    except Exception as e:
        # Fallback: use subprocess
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(TOOLS_DIR, "hybrid_search.py"),
             "search", query, "--top", str(n_results), "--mode", "hybrid"],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=30
        )
        return result.stdout


if __name__ == "__main__":
    # Quick test
    caller = LLMCaller()
    answer = caller.call("What is the capital of Brazil?", max_tokens=20)
    print(f"Test: {answer}")
    print(f"Stats: {caller.stats()}")
