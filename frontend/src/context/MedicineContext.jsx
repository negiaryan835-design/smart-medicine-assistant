import { createContext, useContext, useState } from "react";

const MedicineContext = createContext();

export function MedicineProvider({ children }) {
  const [medicines, setMedicines] = useState([]);

  function addMedicine(medicine) {
    setMedicines((previousMedicines) => [
      ...previousMedicines,
      medicine,
    ]);
  }

  return (
    <MedicineContext.Provider
      value={{
        medicines,
        addMedicine,
      }}
    >
      {children}
    </MedicineContext.Provider>
  );
}

export function useMedicines() {
  return useContext(MedicineContext);
}