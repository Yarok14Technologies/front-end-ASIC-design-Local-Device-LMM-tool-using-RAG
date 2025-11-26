// src/components/FileUpload.jsx
import React, { useState } from 'react';

function FileUpload({ 
  label = 'Select Files', 
  accept = '*', 
  multiple = true, 
  onUploadFiles 
}) {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles(files);
    setUploadStatus('');
    if (onUploadFiles) onUploadFiles(files); // optional immediate callback
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      alert('Please select files to upload.');
      return;
    }

    setUploadStatus('Uploading...');
    
    try {
      // Simulate API call (replace with real API logic)
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      console.log('Files submitted:', selectedFiles.map(f => f.name));
      setUploadStatus(`Successfully uploaded ${selectedFiles.length} files.`);
      
      // Optional: clear selected files after upload
      // setSelectedFiles([]);
      // if (onUploadFiles) onUploadFiles([]);
    } catch (error) {
      setUploadStatus(`Upload failed: ${error.message}`);
    }
  };

  return (
    <div className="file-upload-container" style={{ marginBottom: '20px' }}>
      <label>
        <strong>{label}</strong>
      </label>
      <input 
        type="file" 
        multiple={multiple} 
        accept={accept} 
        onChange={handleFileChange} 
        style={{ display: 'block', margin: '10px 0' }}
      />

      {selectedFiles.length > 0 && (
        <div>
          <h4>Files Selected:</h4>
          <ul>
            {selectedFiles.map((file, index) => (
              <li key={index}>
                {file.name} ({Math.round(file.size / 1024)} KB)
              </li>
            ))}
          </ul>
          <button 
            onClick={handleUpload} 
            disabled={uploadStatus === 'Uploading...'}
          >
            {uploadStatus === 'Uploading...' ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      )}

      {uploadStatus && <p style={{ marginTop: '10px' }}>Status: {uploadStatus}</p>}
    </div>
  );
}

export default FileUpload;
