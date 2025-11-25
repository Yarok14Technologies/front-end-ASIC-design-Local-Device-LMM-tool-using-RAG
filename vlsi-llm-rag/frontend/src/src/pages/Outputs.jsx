import { useState, useEffect } from "react";
import axios from "axios";

export default function Outputs() {
  const [results, setResults] = useState("");

  useEffect(() => {
    axios.get("/api/results").then((res) => {
      setResults(JSON.stringify(res.data, null, 2));
    });
  }, []);

  return (
    <div className="card">
      <h2>Simulation & Verification Outputs</h2>
      <pre>{results}</pre>
    </div>
  );
}
