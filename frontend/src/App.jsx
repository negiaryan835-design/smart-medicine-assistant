import { useState } from "react";

import "./App.css";
import Sidebar from "./components/Sidebar/Sidebar";
import Dashboard from "./pages/Dashboard";
import ScanMedicine from "./pages/ScanMedicine";
import MedicineDetails from "./pages/MedicineDetails";
import Reminder from "./pages/Reminder";
import History from "./pages/History";
import Settings from "./pages/Settings";

function App() {
  const [activePage, setActivePage] = useState("dashboard");
  return (
    <div className="app">
      <Sidebar setActivePage={setActivePage}/>

      <div className="main-content">
        {activePage === "dashboard" && <Dashboard />}

        {activePage === "scan" && <ScanMedicine />}
        
        {activePage === "medicines" && <MedicineDetails />}

        {activePage === "reminders" && <Reminder />}

        {activePage === "history" && <History />}

        {activePage === "settings" && <Settings />}


      </div>
    </div>
  );
}

export default App;
