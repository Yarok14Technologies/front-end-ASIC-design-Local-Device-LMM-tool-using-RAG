import React, { useState, useEffect } from 'react'
import RequirementsForm from '../components/RequirementsForm'
import CodeViewer from '../components/CodeViewer'
import StatusPanel from '../components/StatusPanel'
import axios from 'axios'

const Generate = () => {
  const [specData, setSpecData] = useState(null)
  const [requirements, setRequirements] = useState({})
  const [generationResult, setGenerationResult] = useState(null)
  const [testbenchResult, setTestbenchResult] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [activeTab, setActiveTab] = useState('rtl')

  useEffect(() => {
    const storedData = localStorage.getItem('specData')
    if (storedData) {
      setSpecData(JSON.parse(storedData))
    }
  }, [])

  const generateRTL = async () => {
    if (!specData) return

    setIsGenerating(true)
    setGenerationResult(null)
    setTestbenchResult(null)

    try {
      const response = await axios.post('/api/v1/generate-rtl', {
        spec_text: specData.parsed_data.raw_text,
        requirements: requirements,
        optimization_target: 'balanced'
      })

      setGenerationResult(response.data)

      // Generate testbench for the RTL
      const tbResponse = await axios.post('/api/v1/generate-testbench', {
        rtl_code: response.data.code,
        module_name: response.data.module_name
      })

      setTestbenchResult(tbResponse.data)
      
    } catch (error) {
      console.error('Generation failed:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  if (!specData) {
    return (
      <div className="card">
        <h2>No Specification Found</h2>
        <p>Please upload a specification file first.</p>
        <button 
          className="btn" 
          onClick={() => window.location.href = '/upload'}
        >
          Go to Upload
        </button>
      </div>
    )
  }

  return (
    <div>
      <div className="card">
        <h2>Generate RTL</h2>
        
        <RequirementsForm 
          requirements={requirements}
          onChange={setRequirements}
        />

        <button 
          className="btn" 
          onClick={generateRTL}
          disabled={isGenerating}
        >
          {isGenerating ? 'Generating...' : 'Generate RTL & Testbench'}
        </button>

        {isGenerating && (
          <StatusPanel
            type="loading"
            status="Generating RTL"
            message="This may take a few moments. The AI is generating optimized RTL code based on your specification."
          />
        )}
      </div>

      {generationResult && (
        <div className="card">
          <h2>Generation Results</h2>

          {/* Tabs */}
          <div style={{ marginBottom: '1rem', borderBottom: '1px solid #334155' }}>
            <button
              style={{
                background: 'transparent',
                border: 'none',
                padding: '0.75rem 1.5rem',
                color: activeTab === 'rtl' ? '#60a5fa' : '#cbd5e1',
                borderBottom: activeTab === 'rtl' ? '2px solid #60a5fa' : 'none',
                cursor: 'pointer'
              }}
              onClick={() => setActiveTab('rtl')}
            >
              RTL Code
            </button>
            <button
              style={{
                background: 'transparent',
                border: 'none',
                padding: '0.75rem 1.5rem',
                color: activeTab === 'testbench' ? '#60a5fa' : '#cbd5e1',
                borderBottom: activeTab === 'testbench' ? '2px solid #60a5fa' : 'none',
                cursor: 'pointer'
              }}
              onClick={() => setActiveTab('testbench')}
            >
              Testbench
            </button>
            <button
              style={{
                background: 'transparent',
                border: 'none',
                padding: '0.75rem 1.5rem',
                color: activeTab === 'context' ? '#60a5fa' : '#cbd5e1',
                borderBottom: activeTab === 'context' ? '2px solid #60a5fa' : 'none',
                cursor: 'pointer'
              }}
              onClick={() => setActiveTab('context')}
            >
              RAG Context
            </button>
            <button
              style={{
                background: 'transparent',
                border: 'none',
                padding: '0.75rem 1.5rem',
                color: activeTab === 'validation' ? '#60a5fa' : '#cbd5e1',
                borderBottom: activeTab === 'validation' ? '2px solid #60a5fa' : 'none',
                cursor: 'pointer'
              }}
              onClick={() => setActiveTab('validation')}
            >
              Validation
            </button>
          </div>

          {/* RTL Code Tab */}
          {activeTab === 'rtl' && (
            <div>
              <StatusPanel
                type="success"
                status="RTL Generated Successfully"
                message={generationResult.explanation}
              />
              
              <CodeViewer
                code={generationResult.code}
                language="verilog"
                title={`Module: ${generationResult.module_name}`}
              />
            </div>
          )}

          {/* Testbench Tab */}
          {activeTab === 'testbench' && testbenchResult && (
            <CodeViewer
              code={testbenchResult.testbench_code}
              language="systemverilog"
              title={`Testbench: ${testbenchResult.module_name}`}
            />
          )}

          {/* RAG Context Tab */}
          {activeTab === 'context' && (
            <div>
              <h3>Retrieved Context from Knowledge Base</h3>
              {generationResult.rag_context.map((item, index) => (
                <div key={index} className="card" style={{ marginBottom: '1rem' }}>
                  <p>{item.text}</p>
                  <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.5rem' }}>
                    Source: {item.metadata?.source} | Type: {item.metadata?.type}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Validation Tab */}
          {activeTab === 'validation' && (
            <div>
              <h3>RTL Validation Results</h3>
              {generationResult.validation_result.valid ? (
                <StatusPanel
                  type="success"
                  status="Syntax Validation Passed"
                  message="Basic RTL syntax checks completed successfully."
                />
              ) : (
                <StatusPanel
                  type="warning"
                  status="Syntax Validation Issues"
                  message="Some basic syntax issues were detected."
                />
              )}
              
              {generationResult.validation_result.issues.length > 0 && (
                <div className="card">
                  <h4>Issues Found:</h4>
                  <ul>
                    {generationResult.validation_result.issues.map((issue, index) => (
                      <li key={index} style={{ color: '#f59e0b' }}>{issue}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              <div className="card">
                <h4>Note</h4>
                <p style={{ color: '#94a3b8' }}>
                  {generationResult.validation_result.warning}
                  For full verification, please use professional EDA tools for synthesis, 
                  static timing analysis, and formal verification.
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Generate
