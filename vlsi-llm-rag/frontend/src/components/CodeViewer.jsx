import React from 'react'
import { Copy, Check } from 'lucide-react'

const CodeViewer = ({ code, language = 'verilog', title = 'Code' }) => {
  const [copied, setCopied] = React.useState(false)

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  return (
    <div className="card">
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '1rem'
      }}>
        <h3>{title}</h3>
        <button 
          onClick={copyToClipboard}
          style={{
            background: 'transparent',
            border: '1px solid #475569',
            borderRadius: '0.375rem',
            padding: '0.5rem',
            cursor: 'pointer',
            color: '#cbd5e1'
          }}
        >
          {copied ? <Check size={16} /> : <Copy size={16} />}
        </button>
      </div>
      
      <div className="code-viewer">
        <pre>{code}</pre>
      </div>
    </div>
  )
}

export default CodeViewer
