import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Upload from "./pages/Upload.jsx";
import Generate from "./pages/Generate.jsx";
import Outputs from "./pages/Outputs.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <nav className="nav">
        <Link to="/">Home</Link>
        <Link to="/upload">Upload</Link>
        <Link to="/generate">Generate</Link>
        <Link to="/outputs">Outputs</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/generate" element={<Generate />} />
        <Route path="/outputs" element={<Outputs />} />
      </Routes>
    </BrowserRouter>
  );
}
