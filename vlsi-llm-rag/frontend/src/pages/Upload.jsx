import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import FileUpload from '../components/FileUpload'
import StatusPanel from '../components/StatusPanel'
import axios from 'axios'

const Upload = () => {
  const navigate = useNavigate()
  const [uploadStatus, setUploadStatus] = useState(null)
  const [parsedData, setParsedData] = useState(null)

  const handleFileUpload = async (file) => {
    setUploadStatus({ type: 'loading', status: 'Uploading...', message: 'Processing your specification file' })
    
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/v1/upload-spec', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setParsedData(response.data)
      setUploadStatus({ 
        type: 'success', 
        status: 'Upload Successful', 
        message: `File "${response.data.filename}" processed successfully` 
      })

      // Store in localStorage for use in generate page
      localStorage.setItem('specData', JSON.stringify(response.data))

    } catch (error) {
      setUploadStatus({ 
        type: 'error', 
        status: 'Upload Failed', 
        message: error.response?.data?.detail || 'Failed to process file' 
      })
    }
  }

  const proceedToGenerate = () => {
    navigate('/generate')
  }

  return (
    <div>
      <div className="card">
        <h2>Upload Specification</h2>
        <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>
          Upload your design specification document. Supported formats: TXT, MD, YAML, JSON
        </p>

        <FileUpload onFileUpload={handleFileUpload} />

        {uploadStatus && (
          <StatusPanel 
            type={uploadStatus.type}
            status={uploadStatus.status}
            message={uploadStatus.message}
          />
        )}

        {parsedData && (
          <div>
            <div className="card">
              <h3>Parsed Specification</h3>
              
              {parsedData.parsed_data.interfaces.length > 0 && (
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Interfaces: </strong>
                  {parsedData.parsed_data.interfaces.join(', ')}
                </div>
              )}

              {parsedData.parsed_data.protocols.length > 0 && (
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Protocols: </strong>
                  {parsedData.parsed_data.protocols.join(', ')}
                </div>
              )}

              {Object.keys(parsedData.parsed_data.parameters).length > 0 && (
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Parameters:</strong>
                  <ul style={{ marginLeft: '1.5rem', marginTop: '0.5rem' }}>
                    {Object.entries(parsedData.parsed_data.parameters).map(([key, value]) => (
                      <li key={key}><strong>{key}:</strong> {value}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div style={{ marginTop: '1rem' }}>
                <strong>Raw Text Preview:</strong>
                <div 
                  style={{ 
                    background: '#0f172a',
                    padding: '1rem',
                    borderRadius: '0.375rem',
                    marginTop: '0.5rem',
                    fontSize: '0.9rem',
                    maxHeight: '200px',
                    overflow: 'auto'
                  }}
                >
                  {parsedData.parsed_data.raw_text.substring(0, 500)}...
                </div>
              </div>
            </div>

            <button className="btn" onClick={proceedToGenerate}>
              Proceed to Generate RTL
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Upload
