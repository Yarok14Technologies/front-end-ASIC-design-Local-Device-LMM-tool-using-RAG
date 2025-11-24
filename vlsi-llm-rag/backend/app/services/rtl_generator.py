from typing import Dict, Any, List
from .llm_service import llm_service
from .rag_service import rag_service
import re

class RTLGenerator:
    def __init__(self):
        self.llm_service = llm_service
        self.rag_service = rag_service
    
    async def generate_from_spec(self, spec_text: str, requirements: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate RTL from specification using RAG-enhanced LLM"""
        
        # Query RAG for relevant context
        rag_context = self.rag_service.query(spec_text)
        context_texts = [item["text"] for item in rag_context]
        
        # Enhance spec with requirements
        enhanced_spec = self._enhance_specification(spec_text, requirements)
        
        # Generate RTL using LLM
        result = await self.llm_service.generate_rtl(enhanced_spec, context_texts)
        
        # Add RAG context information
        result["rag_context"] = rag_context
        result["requirements"] = requirements
        
        return result
    
    def _enhance_specification(self, spec_text: str, requirements: Dict[str, Any]) -> str:
        """Enhance specification with formal requirements"""
        enhanced = spec_text
        
        if requirements:
            req_section = "\n\nFORMAL REQUIREMENTS:\n"
            if requirements.get("interface"):
                req_section += f"Interface: {requirements['interface']}\n"
            if requirements.get("protocol"):
                req_section += f"Protocol: {requirements['protocol']}\n"
            if requirements.get("performance"):
                req_section += f"Performance: {requirements['performance']}\n"
            if requirements.get("power"):
                req_section += f"Power: {requirements['power']}\n"
            
            enhanced += req_section
        
        return enhanced
    
    def validate_rtl_syntax(self, rtl_code: str) -> Dict[str, Any]:
        """Basic RTL syntax validation"""
        issues = []
        
        # Check for module declaration
        if "module" not in rtl_code:
            issues.append("Missing module declaration")
        
        # Check for endmodule
        if "endmodule" not in rtl_code:
            issues.append("Missing endmodule")
        
        # Check for basic syntax patterns
        if "always @" not in rtl_code and "assign" not in rtl_code:
            issues.append("No procedural blocks or continuous assignments found")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warning": "Basic syntax check only - full verification requires professional tools"
        }

rtl_generator = RTLGenerator()
