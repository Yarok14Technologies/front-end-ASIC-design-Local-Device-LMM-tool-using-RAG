export default function CodeViewer({ title, code }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <pre style={{ whiteSpace: "pre-wrap", background: "#222", color: "#0f0", padding: "10px" }}>
        {code || "// No code generated yet"}
      </pre>
    </div>
  );
}
