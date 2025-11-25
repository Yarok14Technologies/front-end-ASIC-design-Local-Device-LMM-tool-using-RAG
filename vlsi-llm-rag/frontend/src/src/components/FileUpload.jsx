import axios from "axios";
import { useState } from "react";

export default function FileUpload({ onUpload }) {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("spec_file", file);

    const res = await axios.post("/api/upload", formData);

    onUpload(res.data);
  };

  return (
    <div className="card">
      <h2>Upload Document</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={uploadFile}>Upload</button>
    </div>
  );
}
