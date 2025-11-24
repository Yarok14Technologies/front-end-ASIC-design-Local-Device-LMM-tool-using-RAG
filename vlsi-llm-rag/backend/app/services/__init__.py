"""
Services module for VLSI Design AI Tool Backend

This module contains all the core business logic services for the application:
- RAG (Retrieval-Augmented Generation) service for knowledge base operations
- LLM service for AI model interactions
- RTL generator for Verilog/VHDL code generation
- VIP generator for testbench and verification IP
- File service for file operations and management
"""

from .rag_service import rag_service, RAGService
from .llm_service import llm_service, LLMService
from .rtl_generator import rtl_generator, RTLGenerator
from .vip_generator import vip_generator, VIPGenerator
from .file_service import file_service, FileService

__all__ = [
    # Services instances
    "rag_service",
    "llm_service", 
    "rtl_generator",
    "vip_generator",
    "file_service",
    
    # Service classes
    "RAGService",
    "LLMService",
    "RTLGenerator", 
    "VIPGenerator",
    "FileService",
]

# Service initialization status
SERVICES_STATUS = {
    "rag_service": False,
    "llm_service": False,
    "rtl_generator": False,
    "vip_generator": False,
    "file_service": False
}

def initialize_services():
    """
    Initialize all services and check their status
    
    Returns:
        dict: Status of each service initialization
    """
    global SERVICES_STATUS
    
    try:
        # Initialize RAG service
        rag_service._initialize_knowledge_base()
        SERVICES_STATUS["rag_service"] = True
        print("✅ RAG Service initialized successfully")
    except Exception as e:
        print(f"❌ RAG Service initialization failed: {e}")
        SERVICES_STATUS["rag_service"] = False
    
    try:
        # Initialize LLM service
        if hasattr(llm_service, 'model') and llm_service.model is not None:
            SERVICES_STATUS["llm_service"] = True
            print("✅ LLM Service initialized successfully")
        else:
            SERVICES_STATUS["llm_service"] = False
            print("⚠️  LLM Service: No API key configured - using fallback mode")
    except Exception as e:
        print(f"❌ LLM Service initialization failed: {e}")
        SERVICES_STATUS["llm_service"] = False
    
    try:
        # RTL Generator depends on LLM and RAG services
        if SERVICES_STATUS["llm_service"] or SERVICES_STATUS["rag_service"]:
            SERVICES_STATUS["rtl_generator"] = True
            print("✅ RTL Generator initialized successfully")
        else:
            SERVICES_STATUS["rtl_generator"] = False
            print("⚠️  RTL Generator: Limited functionality without LLM/RAG")
    except Exception as e:
        print(f"❌ RTL Generator initialization failed: {e}")
        SERVICES_STATUS["rtl_generator"] = False
    
    try:
        # VIP Generator depends on LLM service
        if SERVICES_STATUS["llm_service"]:
            SERVICES_STATUS["vip_generator"] = True
            print("✅ VIP Generator initialized successfully")
        else:
            SERVICES_STATUS["vip_generator"] = False
            print("⚠️  VIP Generator: Limited functionality without LLM")
    except Exception as e:
        print(f"❌ VIP Generator initialization failed: {e}")
        SERVICES_STATUS["vip_generator"] = False
    
    try:
        # File service should always work
        file_service._create_directories()
        SERVICES_STATUS["file_service"] = True
        print("✅ File Service initialized successfully")
    except Exception as e:
        print(f"❌ File Service initialization failed: {e}")
        SERVICES_STATUS["file_service"] = False
    
    return SERVICES_STATUS

def get_service_status():
    """
    Get the current status of all services
    
    Returns:
        dict: Current status of each service
    """
    return SERVICES_STATUS.copy()

def is_service_available(service_name: str) -> bool:
    """
    Check if a specific service is available
    
    Args:
        service_name: Name of the service to check
        
    Returns:
        bool: True if service is available
        
    Raises:
        ValueError: If service name is invalid
    """
    if service_name not in SERVICES_STATUS:
        raise ValueError(f"Unknown service: {service_name}")
    
    return SERVICES_STATUS.get(service_name, False)

def get_available_services() -> list:
    """
    Get list of all available services
    
    Returns:
        list: Names of available services
    """
    return [name for name, available in SERVICES_STATUS.items() if available]

def get_unavailable_services() -> list:
    """
    Get list of unavailable services
    
    Returns:
        list: Names of unavailable services
    """
    return [name for name, available in SERVICES_STATUS.items() if not available]

# Service descriptions for API documentation
SERVICE_DESCRIPTIONS = {
    "rag_service": {
        "name": "Retrieval-Augmented Generation Service",
        "description": "Manages knowledge base operations and context retrieval for RTL generation",
        "dependencies": ["chromadb", "sentence-transformers"],
        "features": [
            "Vector database for VLSI knowledge",
            "Semantic search for specifications",
            "Context-aware generation"
        ]
    },
    "llm_service": {
        "name": "Large Language Model Service", 
        "description": "Handles AI model interactions for code generation and analysis",
        "dependencies": ["google-generativeai"],
        "features": [
            "Gemini AI integration",
            "Natural language processing",
            "Code generation and analysis"
        ]
    },
    "rtl_generator": {
        "name": "RTL Generator Service",
        "description": "Generates optimized Register-Transfer Level code from specifications",
        "dependencies": ["rag_service", "llm_service"],
        "features": [
            "Spec-to-RTL conversion",
            "PPA optimization focus", 
            "Verilog/VHDL generation",
            "FSM and module generation"
        ]
    },
    "vip_generator": {
        "name": "Verification IP Generator Service",
        "description": "Creates testbenches and verification components for generated RTL",
        "dependencies": ["llm_service"],
        "features": [
            "Testbench generation",
            "SystemVerilog assertions",
            "UVM component templates",
            "Coverage models"
        ]
    },
    "file_service": {
        "name": "File Management Service", 
        "description": "Handles file operations, storage, and project organization",
        "dependencies": [],
        "features": [
            "File upload and storage",
            "Project management",
            "RTL file organization",
            "Report generation"
        ]
    }
}

def get_service_info(service_name: str = None) -> dict:
    """
    Get detailed information about services
    
    Args:
        service_name: Specific service name, or None for all services
        
    Returns:
        dict: Service information
        
    Raises:
        ValueError: If service name is invalid
    """
    if service_name:
        if service_name not in SERVICE_DESCRIPTIONS:
            raise ValueError(f"Unknown service: {service_name}")
        info = SERVICE_DESCRIPTIONS[service_name].copy()
        info["status"] = "available" if SERVICES_STATUS.get(service_name) else "unavailable"
        return info
    else:
        return {
            name: {
                **desc,
                "status": "available" if SERVICES_STATUS.get(name) else "unavailable"
            }
            for name, desc in SERVICE_DESCRIPTIONS.items()
        }

# Service health check functions
async def check_rag_health() -> dict:
    """Check RAG service health"""
    try:
        count = rag_service.collection.count()
        return {
            "status": "healthy",
            "documents_count": count,
            "message": f"Knowledge base contains {count} documents"
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "error": str(e),
            "message": "RAG service is not functioning properly"
        }

async def check_llm_health() -> dict:
    """Check LLM service health"""
    try:
        if llm_service.model:
            # Try a simple generation to test the service
            test_prompt = "Say 'OK' if you are working."
            response = llm_service.model.generate_content(test_prompt)
            return {
                "status": "healthy",
                "model": "gemini-pro",
                "message": "LLM service is responding correctly"
            }
        else:
            return {
                "status": "degraded",
                "message": "LLM service is in fallback mode (no API key)"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "LLM service is not responding"
        }

async def check_file_service_health() -> dict:
    """Check file service health"""
    try:
        # Check if required directories exist and are writable
        required_dirs = [
            file_service.base_upload_dir,
            f"{file_service.base_upload_dir}/specs",
            f"{file_service.base_upload_dir}/rtl",
            f"{file_service.base_upload_dir}/testbenches"
        ]
        
        for directory in required_dirs:
            if not os.path.exists(directory):
                return {
                    "status": "unhealthy",
                    "error": f"Directory {directory} does not exist",
                    "message": "File service directories are not properly setup"
                }
            
            # Check write permission
            test_file = os.path.join(directory, "test_write.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
            except Exception:
                return {
                    "status": "unhealthy",
                    "error": f"No write permission in {directory}",
                    "message": "File service lacks write permissions"
                }
        
        return {
            "status": "healthy",
            "message": "File service directories are accessible and writable"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "File service health check failed"
        }

async def check_all_services_health() -> dict:
    """
    Comprehensive health check for all services
    
    Returns:
        dict: Health status of all services
    """
    health_results = {}
    
    # Check each service
    health_results["rag_service"] = await check_rag_health()
    health_results["llm_service"] = await check_llm_health()
    health_results["file_service"] = await check_file_service_health()
    
    # Overall status
    all_healthy = all(result["status"] in ["healthy", "degraded"] 
                     for result in health_results.values())
    
    return {
        "overall_status": "healthy" if all_healthy else "unhealthy",
        "services": health_results,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }

# Initialize services when module is imported
try:
    initialize_services()
    print("🎯 VLSI Design AI Tool Services Initialized")
except Exception as e:
    print(f"⚠️  Service initialization completed with warnings: {e}")
