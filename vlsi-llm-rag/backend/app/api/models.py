"""
Pydantic models for VLSI Design AI Tool API

This module contains all request and response models for the FastAPI endpoints.
These models provide type safety, validation, and automatic API documentation.
"""

from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum

# Enums for type safety
class OptimizationTarget(str, Enum):
    """Optimization targets for RTL generation"""
    POWER = "power"
    PERFORMANCE = "performance"
    AREA = "area"
    BALANCED = "balanced"

class RTLanguage(str, Enum):
    """Supported RTL languages"""
    VERILOG = "verilog"
    VHDL = "vhdl"
    SYSTEM_VERILOG = "systemverilog"

class ProtocolType(str, Enum):
    """Supported protocol types"""
    AXI = "axi"
    AXI_LITE = "axi_lite"
    AHB = "ahb"
    APB = "apb"
    UART = "uart"
    SPI = "spi"
    I2C = "i2c"
    PCIE = "pcie"
    ETHERNET = "ethernet"
    CUSTOM = "custom"

class FileType(str, Enum):
    """Supported file types"""
    SPECIFICATION = "specification"
    RTL = "rtl"
    TESTBENCH = "testbench"
    CONSTRAINT = "constraint"
    DOCUMENTATION = "documentation"

class ServiceStatus(str, Enum):
    """Service status types"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNAVAILABLE = "unavailable"

# Request Models
class GenerateRequest(BaseModel):
    """
    Request model for RTL generation endpoint
    """
    spec_text: str = Field(
        ...,
        description="Natural language specification text",
        example="Design an AXI4-Lite interface controller with 32-bit data bus, support for read and write transactions, and 4 configurable registers.",
        min_length=10,
        max_length=10000
    )
    
    requirements: Optional[Dict[str, Any]] = Field(
        default={},
        description="Structured design requirements and constraints",
        example={
            "interface": "AXI4-Lite",
            "data_width": 32,
            "address_width": 32,
            "clock_frequency": "100MHz",
            "power_optimization": "low",
            "target_technology": "TSMC 28nm"
        }
    )
    
    optimization_target: OptimizationTarget = Field(
        default=OptimizationTarget.BALANCED,
        description="Primary optimization target for RTL generation"
    )
    
    language: RTLanguage = Field(
        default=RTLanguage.VERILOG,
        description="Target RTL language"
    )
    
    include_testbench: bool = Field(
        default=True,
        description="Whether to generate accompanying testbench"
    )
    
    custom_instructions: Optional[str] = Field(
        default=None,
        description="Additional custom instructions for the LLM",
        max_length=2000
    )
    
    @validator('spec_text')
    def validate_spec_text(cls, v):
        """Validate specification text"""
        if len(v.strip()) < 10:
            raise ValueError('Specification text must be at least 10 characters long')
        return v.strip()
    
    @validator('requirements')
    def validate_requirements(cls, v):
        """Validate requirements structure"""
        if v is None:
            return {}
        return v

class TestbenchRequest(BaseModel):
    """
    Request model for testbench generation endpoint
    """
    rtl_code: str = Field(
        ...,
        description="RTL code for which to generate testbench",
        example="module my_module(input clk, input rst, output reg [7:0] data); ... endmodule",
        min_length=10,
        max_length=50000
    )
    
    module_name: str = Field(
        ...,
        description="Name of the module under test",
        example="axi_controller",
        min_length=1,
        max_length=100
    )
    
    test_scenarios: Optional[List[str]] = Field(
        default=None,
        description="Specific test scenarios to include",
        example=["reset sequence", "normal operation", "error conditions"]
    )
    
    verification_methodology: str = Field(
        default="basic",
        description="Verification methodology to use",
        example="UVM, OVM, or basic testbench"
    )
    
    coverage_requirements: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Coverage requirements for the testbench",
        example={"code_coverage": True, "functional_coverage": False}
    )
    
    @validator('rtl_code')
    def validate_rtl_code(cls, v):
        """Validate RTL code"""
        if 'module' not in v.lower() and 'entity' not in v.lower():
            raise ValueError('RTL code must contain module or entity declaration')
        return v
    
    @validator('module_name')
    def validate_module_name(cls, v):
        """Validate module name"""
        if not v.replace('_', '').isalnum():
            raise ValueError('Module name must be alphanumeric with underscores')
        return v

class ProjectCreateRequest(BaseModel):
    """
    Request model for project creation endpoint
    """
    name: str = Field(
        ...,
        description="Project name",
        example="AXI4-Lite Controller",
        min_length=1,
        max_length=100
    )
    
    description: Optional[str] = Field(
        default=None,
        description="Project description",
        example="High-performance AXI4-Lite interface controller with configurable registers",
        max_length=1000
    )
    
    technology_node: Optional[str] = Field(
        default=None,
        description="Target technology node",
        example="TSMC 28nm"
    )
    
    constraints: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Design constraints",
        example={
            "clock_frequency": "100MHz",
            "power_budget": "10mW",
            "area_target": "10000 um²"
        }
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional project metadata"
    )
    
    @validator('name')
    def validate_name(cls, v):
        """Validate project name"""
        if not v.strip():
            raise ValueError('Project name cannot be empty')
        # Remove any problematic characters
        cleaned_name = ''.join(c for c in v if c.isalnum() or c in (' ', '-', '_'))
        return cleaned_name.strip()

class AnalysisRequest(BaseModel):
    """
    Request model for RTL analysis endpoint
    """
    rtl_code: str = Field(
        ...,
        description="RTL code to analyze",
        min_length=10,
        max_length=50000
    )
    
    analysis_type: List[str] = Field(
        default=["syntax", "complexity"],
        description="Types of analysis to perform",
        example=["syntax", "complexity", "ppa_estimation"]
    )
    
    constraints: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Analysis constraints"
    )

# Response Models
class RAGContextItem(BaseModel):
    """
    Individual RAG context item
    """
    text: str = Field(..., description="Retrieved context text")
    metadata: Dict[str, Any] = Field(..., description="Context metadata")
    similarity_score: Optional[float] = Field(None, description="Similarity score")
    source: Optional[str] = Field(None, description="Source of the context")

class ValidationResult(BaseModel):
    """
    RTL validation results
    """
    valid: bool = Field(..., description="Whether the RTL is valid")
    issues: List[str] = Field(default=[], description="Validation issues found")
    warnings: List[str] = Field(default=[], description="Validation warnings")
    score: Optional[float] = Field(None, description="Validation score (0-100)")

class PPAMetrics(BaseModel):
    """
    Power-Performance-Area metrics
    """
    power_estimate: Optional[float] = Field(None, description="Power estimate")
    performance_estimate: Optional[float] = Field(None, description="Performance estimate")
    area_estimate: Optional[float] = Field(None, description="Area estimate")
    complexity_score: Optional[float] = Field(None, description="Complexity score")
    optimization_suggestions: List[str] = Field(default=[], description="Optimization suggestions")

class RTLResponse(BaseModel):
    """
    Response model for RTL generation endpoint
    """
    module_name: str = Field(..., description="Generated module name")
    code: str = Field(..., description="Generated RTL code")
    explanation: str = Field(..., description="Explanation of the generated design")
    language: RTLanguage = Field(..., description="RTL language used")
    
    # Additional metadata
    rag_context: List[RAGContextItem] = Field(
        default=[],
        description="RAG context used for generation"
    )
    
    validation_result: ValidationResult = Field(
        ...,
        description="RTL validation results"
    )
    
    ppa_metrics: Optional[PPAMetrics] = Field(
        None,
        description="PPA metrics and estimates"
    )
    
    requirements: Optional[Dict[str, Any]] = Field(
        None,
        description="Requirements used for generation"
    )
    
    generation_time: float = Field(
        ...,
        description="Generation time in seconds"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Response timestamp"
    )

class TestbenchResponse(BaseModel):
    """
    Response model for testbench generation endpoint
    """
    testbench_code: str = Field(..., description="Generated testbench code")
    module_name: str = Field(..., description="Testbench module name")
    test_scenarios: List[str] = Field(..., description="Implemented test scenarios")
    verification_components: List[str] = Field(default=[], description="Verification components included")
    
    # Additional metadata
    coverage_points: Optional[List[str]] = Field(
        None,
        description="Coverage points defined"
    )
    
    assertions: Optional[List[str]] = Field(
        None,
        description="Assertions included"
    )
    
    generation_time: float = Field(
        ...,
        description="Generation time in seconds"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Response timestamp"
    )

class FileUploadResponse(BaseModel):
    """
    Response model for file upload endpoint
    """
    filename: str = Field(..., description="Original filename")
    saved_filename: str = Field(..., description="Saved filename on server")
    file_path: str = Field(..., description="Server file path")
    file_size: int = Field(..., description="File size in bytes")
    file_type: str = Field(..., description="File type/extension")
    
    # Parsed content
    parsed_data: Dict[str, Any] = Field(
        ...,
        description="Parsed specification data"
    )
    
    # Metadata
    upload_time: datetime = Field(
        default_factory=datetime.now,
        description="Upload timestamp"
    )
    
    content_preview: Optional[str] = Field(
        None,
        description="Content preview (first 500 characters)"
    )
    
    @validator('content_preview', always=True)
    def create_content_preview(cls, v, values):
        """Create content preview from parsed data"""
        if 'parsed_data' in values and 'raw_text' in values['parsed_data']:
            raw_text = values['parsed_data']['raw_text']
            return raw_text[:500] + ('...' if len(raw_text) > 500 else '')
        return v

class ProjectResponse(BaseModel):
    """
    Response model for project operations
    """
    project_id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    
    # Project structure
    directories: List[str] = Field(
        ...,
        description="Project directory structure"
    )
    
    file_count: Dict[str, int] = Field(
        default={},
        description="File counts by type"
    )
    
    # Metadata
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    # Project statistics
    total_files: int = Field(
        default=0,
        description="Total number of files in project"
    )
    
    total_size: int = Field(
        default=0,
        description="Total project size in bytes"
    )
    
    recent_activity: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Recent project activity"
    )

class ServiceHealth(BaseModel):
    """
    Individual service health information
    """
    status: ServiceStatus = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    last_check: datetime = Field(..., description="Last health check timestamp")
    
    # Additional details
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional service details"
    )

class HealthResponse(BaseModel):
    """
    Response model for health check endpoint
    """
    status: ServiceStatus = Field(..., description="Overall system status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Health check timestamp")
    
    # Service health
    services: Dict[str, ServiceHealth] = Field(
        ...,
        description="Health status of individual services"
    )
    
    # System information
    system_info: Dict[str, Any] = Field(
        ...,
        description="System information and metrics"
    )
    
    # Uptime and statistics
    uptime_seconds: float = Field(..., description="System uptime in seconds")
    total_requests: int = Field(..., description="Total requests processed")
    
    @validator('system_info', always=True)
    def add_system_info(cls, v):
        """Add system information if not provided"""
        import psutil
        import datetime
        
        if not v:
            v = {}
        
        # Add basic system metrics
        v.update({
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat()
        })
        
        return v

class AnalysisResponse(BaseModel):
    """
    Response model for RTL analysis endpoint
    """
    analysis_id: str = Field(..., description="Analysis identifier")
    analysis_type: List[str] = Field(..., description="Types of analysis performed")
    
    # Analysis results
    results: Dict[str, Any] = Field(
        ...,
        description="Analysis results by type"
    )
    
    # Summary and recommendations
    summary: Dict[str, Any] = Field(
        ...,
        description="Analysis summary"
    )
    
    recommendations: List[str] = Field(
        default=[],
        description="Design recommendations"
    )
    
    # Metadata
    analysis_time: float = Field(..., description="Analysis time in seconds")
    timestamp: datetime = Field(..., description="Analysis timestamp")

class ErrorResponse(BaseModel):
    """
    Standard error response model
    """
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[Dict[str, Any]] = Field(None, description="Error details")
    
    # Request information
    request_id: Optional[str] = Field(None, description="Request identifier")
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Error timestamp"
    )
    
    # Suggested actions
    suggestion: Optional[str] = Field(
        None,
        description="Suggested action to resolve the error"
    )

class SearchResponse(BaseModel):
    """
    Response model for knowledge base search
    """
    query: str = Field(..., description="Search query")
    results: List[RAGContextItem] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total results found")
    search_time: float = Field(..., description="Search time in seconds")

class ProjectListResponse(BaseModel):
    """
    Response model for project listing
    """
    projects: List[ProjectResponse] = Field(..., description="List of projects")
    total_projects: int = Field(..., description="Total number of projects")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total number of pages")

class FileInfo(BaseModel):
    """
    File information model
    """
    filename: str = Field(..., description="File name")
    file_path: str = Field(..., description="File path")
    file_type: FileType = Field(..., description="File type")
    size: int = Field(..., description="File size in bytes")
    created: datetime = Field(..., description="Creation timestamp")
    modified: datetime = Field(..., description="Last modification timestamp")
    
    # Additional metadata
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="File metadata"
    )
    
    content_hash: Optional[str] = Field(
        None,
        description="File content hash"
    )

class ProjectFilesResponse(BaseModel):
    """
    Response model for project files listing
    """
    project_id: str = Field(..., description="Project identifier")
    files: Dict[str, List[FileInfo]] = Field(
        ...,
        description="Files organized by category"
    )
    
    # Summary statistics
    total_files: int = Field(..., description="Total number of files")
    total_size: int = Field(..., description="Total size in bytes")
    
    # File type breakdown
    file_type_breakdown: Dict[str, int] = Field(
        ...,
        description="File count by type"
    )

# Batch operation models
class BatchGenerateRequest(BaseModel):
    """
    Request model for batch RTL generation
    """
    specifications: List[GenerateRequest] = Field(
        ...,
        description="List of generation requests",
        min_items=1,
        max_items=10
    )
    
    parallel: bool = Field(
        default=False,
        description="Whether to process requests in parallel"
    )

class BatchGenerateResponse(BaseModel):
    """
    Response model for batch RTL generation
    """
    results: List[RTLResponse] = Field(..., description="Generation results")
    total_processed: int = Field(..., description="Total specifications processed")
    successful: int = Field(..., description="Number of successful generations")
    failed: int = Field(..., description="Number of failed generations")
    
    # Batch metadata
    batch_id: str = Field(..., description="Batch identifier")
    processing_time: float = Field(..., description="Total processing time in seconds")

# Configuration models
class ServiceConfig(BaseModel):
    """
    Service configuration model
    """
    llm_provider: str = Field(..., description="LLM provider")
    llm_model: str = Field(..., description="LLM model name")
    rag_enabled: bool = Field(..., description="Whether RAG is enabled")
    max_file_size: int = Field(..., description="Maximum file size in bytes")
    allowed_extensions: List[str] = Field(..., description="Allowed file extensions")

class APIInfoResponse(BaseModel):
    """
    Response model for API information endpoint
    """
    name: str = Field(..., description="API name")
    version: str = Field(..., description="API version")
    description: str = Field(..., description="API description")
    
    # Features and capabilities
    features: List[str] = Field(..., description="Available features")
    supported_languages: List[str] = Field(..., description="Supported RTL languages")
    supported_protocols: List[str] = Field(..., description="Supported protocols")
    
    # Service configuration
    service_config: ServiceConfig = Field(..., description="Service configuration")
    
    # API endpoints
    endpoints: List[Dict[str, Any]] = Field(..., description="Available endpoints")
    
    # Statistics
    uptime: float = Field(..., description="API uptime in seconds")
    total_requests: int = Field(..., description="Total requests processed")

# WebSocket models (for future real-time updates)
class GenerationProgress(BaseModel):
    """
    Model for generation progress updates
    """
    task_id: str = Field(..., description="Task identifier")
    progress: float = Field(..., description="Progress percentage (0-100)")
    status: str = Field(..., description="Current status")
    message: str = Field(..., description="Progress message")
    estimated_time_remaining: Optional[float] = Field(None, description="Estimated time remaining in seconds")

class GenerationComplete(BaseModel):
    """
    Model for generation completion notification
    """
    task_id: str = Field(..., description="Task identifier")
    result: RTLResponse = Field(..., description="Generation result")
    success: bool = Field(..., description="Whether generation was successful")

# Example data for documentation
EXAMPLE_RTL_RESPONSE = RTLResponse(
    module_name="axi_lite_controller",
    code="""
module axi_lite_controller (
    input wire clk,
    input wire rst_n,
    // AXI4-Lite interface
    input wire [31:0] awaddr,
    input wire awvalid,
    output reg awready,
    // ... more ports
);
    // Implementation here
endmodule
    """.strip(),
    explanation="AXI4-Lite controller with configurable registers and support for read/write transactions.",
    language=RTLanguage.VERILOG,
    rag_context=[],
    validation_result=ValidationResult(
        valid=True,
        issues=[],
        warnings=[],
        score=95.0
    ),
    generation_time=2.5,
    timestamp=datetime.now()
)

EXAMPLE_ERROR_RESPONSE = ErrorResponse(
    error="VALIDATION_ERROR",
    message="Specification text is too short",
    detail={"min_length": 10, "actual_length": 5},
    suggestion="Please provide a more detailed specification with at least 10 characters."
)

print("✅ VLSI Design AI Tool API Models loaded successfully!")
