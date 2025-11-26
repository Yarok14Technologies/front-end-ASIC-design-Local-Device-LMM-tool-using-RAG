// src/pages/Upload.jsx
import React, { useState } from 'react';
import FileUpload from '../components/FileUpload.jsx';

function Upload() {
  // State to hold uploaded files for each category
  const [uploads, setUploads] = useState({
    spec: [],
    tbRequirements: [],
    functionalDesign: [],
    architectureDesign: [],
    protocol: [],
  });

  const handleUpload = (category, files) => {
    setUploads(prev => ({
      ...prev,
      [category]: files,
    }));
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Upload Design Files</h1>

      {/* Specification Documents */}
      <section>
        <h2>Specification Documents</h2>
        <FileUpload
          multiple={true}
          onUpload={(files) => handleUpload('spec', files)}
        />
      </section>

      {/* Testbench Requirements */}
      <section>
        <h2>Testbench Requirements</h2>
        <FileUpload
          multiple={true}
          onUpload={(files) => handleUpload('tbRequirements', files)}
        />
      </section>

      {/* Functional Design */}
      <section>
        <h2>Functional Design</h2>
        <FileUpload
          multiple={true}
          onUpload={(files) => handleUpload('functionalDesign', files)}
        />
      </section>

      {/* Architecture Design */}
      <section>
        <h2>Architecture Design</h2>
        <FileUpload
          multiple={true}
          onUpload={(files) => handleUpload('architectureDesign', files)}
        />
      </section>

      {/* Protocol Working */}
      <section>
        <h2>Protocol Working</h2>
        <FileUpload
          multiple={true}
          onUpload={(files) => handleUpload('protocol', files)}
        />
      </section>

      {/* Optional: Show uploaded files summary */}
      <section style={{ marginTop: '20px' }}>
        <h2>Uploaded Files Summary</h2>
        <pre>{JSON.stringify(uploads, null, 2)}</pre>
      </section>
    </div>
  );
}

export default Upload;
