import FileUpload from "../components/FileUpload.jsx";
import { useState } from "react";

export default function Upload() {
  const [output, setOutput] = useState("");

  return (
    <div>
      <FileUpload onUpload={(data) => setOutput(JSON.stringify(data, null, 2))} />

      <pre>{output}</pre>
    </div>
  );
}

