import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { MedicineProvider } from "./context/MedicineContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <MedicineProvider>
      <App />
    </MedicineProvider>
  </StrictMode>
);