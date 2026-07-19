import "./Sidebar.css";

import {
  FaHome,
  FaCamera,
  FaPills,
  FaBell,
  FaHistory,
  FaCog,
  FaSignOutAlt,
} from "react-icons/fa";

function Sidebar({ setActivePage }) {
  return (
    <div className="sidebar">
      <h2>Smart Medicine Assistant</h2>

      <ul>
        <li onClick={() => setActivePage("dashboard")}>
          <FaHome /> Dashboard
        </li>

        <li onClick={() => setActivePage("scan")}>
          <FaCamera /> Scan Medicine
        </li>

        <li onClick={() => setActivePage("medicines")}>
          <FaPills /> My Medicines
        </li>

        <li onClick={() => setActivePage("reminders")}>
          <FaBell /> Reminders
        </li>

        <li onClick={() => setActivePage("history")}>
          <FaHistory /> History
        </li>

        <li onClick={() => setActivePage("settings")}>
          <FaCog /> Settings
        </li>
      </ul>

      <div className="logout">
        <FaSignOutAlt /> Logout
      </div>
    </div>
  );
}

export default Sidebar;