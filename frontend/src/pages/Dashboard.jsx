import "./Dashboard.css";

function Dashboard() {
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <h2>Welcome to Smart Medicine Assistant</h2>
        <p>Manage your medicines, reminders, and health information.</p>
      </div>

      <div className="stats-container">
        <div className="stat-card">
          <h3>Total Medicines</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <h3>Active Reminders</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <h3>Medicines Scanned</h3>
          <p>0</p>
        </div>
      </div>

      <div className="reminders-section">
        <h2>Upcoming Reminders</h2>

        <div className="reminder-card">
          <div>
            <h3>No reminders yet</h3>
            <p>Add a medicine reminder to see it here.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;