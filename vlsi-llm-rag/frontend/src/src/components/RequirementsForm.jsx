export default function RequirementsForm({ onSubmit }) {
  const handleSubmit = (e) => {
    e.preventDefault();

    const data = {
      module: e.target.module.value,
      protocol: e.target.protocol.value,
      constraints: e.target.constraints.value
    };

    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h2>Define RTL Requirements</h2>

      <label>Module Name:</label>
      <input name="module" required />

      <label>Protocol:</label>
      <input name="protocol" />

      <label>Constraints / Notes:</label>
      <textarea name="constraints" />

      <button>Generate RTL</button>
    </form>
  );
}
