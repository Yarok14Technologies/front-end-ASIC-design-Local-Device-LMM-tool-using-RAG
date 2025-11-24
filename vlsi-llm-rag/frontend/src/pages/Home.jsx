import React from 'react'
import { Cpu, Zap, Database, Code } from 'lucide-react'

const Home = () => {
  return (
    <div>
      <div className="card">
        <h1>Welcome to VLSI Design AI Tool</h1>
        <p style={{ fontSize: '1.1rem', color: '#cbd5e1', marginBottom: '2rem' }}>
          Automate your front-end VLSI design flow with AI-powered RTL generation and verification.
        </p>

        <div className="grid grid-2">
          <div style={{ textAlign: 'center', padding: '1.5rem' }}>
            <Cpu size={48} color="#60a5fa" />
            <h3 style={{ margin: '1rem 0' }}>Spec-to-RTL Generation</h3>
            <p style={{ color: '#94a3b8' }}>
              Convert natural language specifications into optimized Verilog/VHDL code
            </p>
          </div>

          <div style={{ textAlign: 'center', padding: '1.5rem' }}>
            <Zap size={48} color="#a78bfa" />
            <h3 style={{ margin: '1rem 0' }}>PPA Optimization</h3>
            <p style={{ color: '#94a3b8' }}>
              Generate RTL focused on Power, Performance, and Area efficiency
            </p>
          </div>

          <div style={{ textAlign: 'center', padding: '1.5rem' }}>
            <Database size={48} color="#f59e0b" />
            <h3 style={{ margin: '1rem 0' }}>RAG Knowledge Base</h3>
            <p style={{ color: '#94a3b8' }}>
              Context-aware generation using VLSI design patterns and protocols
            </p>
          </div>

          <div style={{ textAlign: 'center', padding: '1.5rem' }}>
            <Code size={48} color="#10b981" />
            <h3 style={{ margin: '1rem 0' }}>Verification Ready</h3>
            <p style={{ color: '#94a3b8' }}>
              Automated testbench generation and iterative verification
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h3>Getting Started</h3>
          <ol style={{ paddingLeft: '1.5rem', color: '#cbd5e1' }}>
            <li style={{ marginBottom: '0.5rem' }}>Upload your specification document</li>
            <li style={{ marginBottom: '0.5rem' }}>Define design requirements</li>
            <li style={{ marginBottom: '0.5rem' }}>Generate optimized RTL code</li>
            <li style={{ marginBottom: '0.5rem' }}>Review and download results</li>
          </ol>
        </div>

        <div className="card">
          <h3>Supported Features</h3>
          <ul style={{ paddingLeft: '1.5rem', color: '#cbd5e1' }}>
            <li style={{ marginBottom: '0.5rem' }}>Verilog/VHDL RTL generation</li>
            <li style={{ marginBottom: '0.5rem' }}>Finite State Machine (FSM) design</li>
            <li style={{ marginBottom: '0.5rem' }}>Testbench and VIP generation</li>
            <li style={{ marginBottom: '0.5rem' }}>AMBA AXI, AHB, APB protocols</li>
            <li style={{ marginBottom: '0.5rem' }}>UART, SPI, I2C interfaces</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Home
