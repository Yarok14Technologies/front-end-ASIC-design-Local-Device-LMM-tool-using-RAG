import React from 'react'

const RequirementsForm = ({ requirements, onChange }) => {
  const updateRequirement = (key, value) => {
    onChange({
      ...requirements,
      [key]: value
    })
  }

  return (
    <div className="card">
      <h3>Design Requirements</h3>
      
      <div className="grid grid-2">
        <div className="form-group">
          <label>Interface Type</label>
          <select 
            value={requirements.interface || ''}
            onChange={(e) => updateRequirement('interface', e.target.value)}
          >
            <option value="">Select Interface</option>
            <option value="AXI4">AXI4</option>
            <option value="AXI4-Lite">AXI4-Lite</option>
            <option value="AHB">AHB</option>
            <option value="APB">APB</option>
            <option value="UART">UART</option>
            <option value="SPI">SPI</option>
            <option value="I2C">I2C</option>
            <option value="Custom">Custom</option>
          </select>
        </div>

        <div className="form-group">
          <label>Protocol</label>
          <input
            type="text"
            value={requirements.protocol || ''}
            onChange={(e) => updateRequirement('protocol', e.target.value)}
            placeholder="e.g., AMBA AXI, UART 16550"
          />
        </div>

        <div className="form-group">
          <label>Performance Target</label>
          <select 
            value={requirements.performance || ''}
            onChange={(e) => updateRequirement('performance', e.target.value)}
          >
            <option value="">Select Performance</option>
            <option value="Low Frequency (< 100MHz)">Low Frequency</option>
            <option value="Medium Frequency (100-500MHz)">Medium Frequency</option>
            <option value="High Frequency (> 500MHz)">High Frequency</option>
          </select>
        </div>

        <div className="form-group">
          <label>Power Optimization</label>
          <select 
            value={requirements.power || ''}
            onChange={(e) => updateRequirement('power', e.target.value)}
          >
            <option value="">Select Power Target</option>
            <option value="Ultra Low Power">Ultra Low Power</option>
            <option value="Low Power">Low Power</option>
            <option value="Balanced">Balanced</option>
            <option value="Performance Oriented">Performance Oriented</option>
          </select>
        </div>
      </div>

      <div className="form-group">
        <label>Additional Requirements</label>
        <textarea
          value={requirements.additional || ''}
          onChange={(e) => updateRequirement('additional', e.target.value)}
          placeholder="Enter any specific requirements, constraints, or special features..."
        />
      </div>
    </div>
  )
}

export default RequirementsForm
