import "./App.css";
import Sidebar from "./components/Sidebar/Sidebar";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <div className="app">
      <Sidebar />

      <div className="main-content">
        <Dashboard />
      </div>
    </div>
  );
}

export default App;
