import React, { useCallback, useState } from 'react'
import { Upload } from 'lucide-react'

const FileUpload = ({ onFileUpload, acceptedTypes = '.txt,.md,.yaml,.yml,.json' }) => {
  const [isDragging, setIsDragging] = useState(false)

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const handleDragIn = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }, [])

  const handleDragOut = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    
    const files = e.dataTransfer.files
    if (files && files.length > 0) {
      onFileUpload(files[0])
    }
  }, [onFileUpload])

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      onFileUpload(file)
    }
  }

  return (
    <div
      className={`file-upload ${isDragging ? 'dragover' : ''}`}
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={() => document.getElementById('file-input').click()}
    >
      <input
        id="file-input"
        type="file"
        accept={acceptedTypes}
        onChange={handleFileSelect}
        style={{ display: 'none' }}
      />
      
      <Upload size={48} color="#64748b" />
      <h3>Upload Specification File</h3>
      <p>Drag & drop or click to upload</p>
      <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.5rem' }}>
        Supported: {acceptedTypes}
      </p>
    </div>
  )
}

export default FileUpload
