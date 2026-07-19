import { useState } from "react";
import "./ScanMedicine.css";

function ScanMedicine() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [medicineResult, setMedicineResult] = useState(null);
  const [imageFile, setImageFile] = useState(null);

  function handleImageChange(event) {
    const file = event.target.files[0];

    if (file) {
      setImageFile(file);  
      setSelectedImage(URL.createObjectURL(file));
    }
  }

  function handleAnalyze() {
  setIsAnalyzing(true);

  setTimeout(() => {
    setIsAnalyzing(false);

    setMedicineResult({
      name: "Paracetamol",
      dosage: "500 mg",
      expiry: "December 2027",
      manufacturer: "Example Pharma",
    });
  }, 2000);
}

function handleScanAgain() {
  setSelectedImage(null);
  setMedicineResult(null);
  setImageFile(null);
}

  return (
    <div className="scan-page">
      <div className="scan-header">
        <h1>Scan Medicine</h1>
        <p>Upload an image of your medicine to identify it.</p>
      </div>

      <div className="upload-card">
        <h2>Upload Medicine Image</h2>

        <p>
          Take a clear photo of the medicine strip, bottle, or packaging.
        </p>

        <label className="upload-box">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />

          {selectedImage ? (
            <img src={selectedImage} alt="Selected medicine" />
          ) : (
            <>
              <span>📷</span>
              <p>Click here to upload an image</p>
            </>
          )}
        </label>

        {selectedImage && (
        <button
          className="analyze-button"
          onClick={handleAnalyze}
          disabled={isAnalyzing}
       >
          {isAnalyzing ? "Analyzing..." : "Analyze Medicine"}
       </button>
        )}

        {medicineResult && (
  <div className="medicine-result-card">
    <h2>Medicine Details</h2>

    <div className="result-item">
      <strong>Medicine Name:</strong>
      <span>{medicineResult.name}</span>
    </div>

    <div className="result-item">
      <strong>Dosage:</strong>
      <span>{medicineResult.dosage}</span>
    </div>

    <div className="result-item">
      <strong>Expiry Date:</strong>
      <span>{medicineResult.expiry}</span>
    </div>

    <div className="result-item">
      <strong>Manufacturer:</strong>
      <span>{medicineResult.manufacturer}</span>
    </div>

    <button
  className="scan-again-button"
  onClick={handleScanAgain}
>
  Scan Another Medicine
</button>
  </div>
)}
      </div>
    </div>
  );
}

export default ScanMedicine;