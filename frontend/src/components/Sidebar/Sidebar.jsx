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

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>Smart Medicine Assistant</h2>

      <ul>
        <li>
          <FaHome /> Dashboard
        </li>

        <li>
          <FaCamera /> Scan Medicine
        </li>

        <li>
          <FaPills /> My Medicines
        </li>

        <li>
          <FaBell /> Reminders
        </li>

        <li>
          <FaHistory /> History
        </li>

        <li>
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