import "./Settings.css";

function Settings() {
  return (
    <div className="settings-page">
      <div className="page-header">
        <h1>Settings</h1>
        <p>Manage your application preferences.</p>
      </div>

      <div className="settings-card">
        <h2>Notifications</h2>
        <p>Receive reminders for your medicines.</p>

        <label className="toggle-row">
          <span>Medicine Reminders</span>
          <input type="checkbox" defaultChecked />
        </label>
      </div>

      <div className="settings-card">
        <h2>Account</h2>
        <p>Manage your account preferences.</p>

        <button className="settings-button">
          Update Profile
        </button>
      </div>
    </div>
  );
}

export default Settings;