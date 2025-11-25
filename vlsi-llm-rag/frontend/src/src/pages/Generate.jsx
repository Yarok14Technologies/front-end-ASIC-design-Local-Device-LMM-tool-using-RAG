import { useState } from "react";
import RequirementsForm from "../components/RequirementsForm.jsx";
import CodeViewer from "../components/CodeViewer.jsx";
import axios from "axios";

export default function Generate() {
  const [rtl, setRTL] = useState("");

  const generateRTL = async (req) => {
    const res = await axios.post("/api/generate", req);
    setRTL(res.data.rtl_code);
  };

  return (
    <div>
      <RequirementsForm onSubmit={generateRTL} />
      <CodeViewer title="Generated RTL" code={rtl} />
    </div>
  );
}
