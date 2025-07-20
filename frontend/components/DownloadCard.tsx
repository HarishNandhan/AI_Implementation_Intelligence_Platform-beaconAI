import React, { useState } from "react";
import axios from "axios";

type Props = {
  persona: string;
  companyName: string;
  insights: Record<string, string>; // CARE question IDs → insights
};

const DownloadCard: React.FC<Props> = ({ persona, companyName, insights }) => {
  const [email, setEmail] = useState("");
  const [pdfPath, setPdfPath] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleDownload = async () => {
    try {
      setLoading(true);
      // Step 1: Generate PDF
      const reportRes = await axios.post("http://localhost:8000/report/generate", {
        persona,
        company_name: companyName,
        insights
      });

      const path = reportRes.data.filepath;
      setPdfPath(path);

      // Step 2: Send via email
      await axios.post("http://localhost:8000/email/send", {
        email_address: email,
        filepath: path
      });

      setSubmitted(true);
    } catch (error) {
      console.error("Error generating or sending report:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-md w-full max-w-lg">
      <h2 className="text-xl font-bold mb-4">Download Your Insight Report</h2>

      {!submitted ? (
        <>
          <input
            type="email"
            placeholder="Enter your email"
            className="border border-gray-300 rounded-md px-4 py-2 w-full mb-3"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button
            className="bg-blue-600 text-white font-semibold px-4 py-2 rounded-md w-full"
            onClick={handleDownload}
            disabled={loading || !email.includes("@")}
          >
            {loading ? "Generating..." : "Send and Download PDF"}
          </button>
        </>
      ) : (
        <>
          <p className="text-green-600 mb-2">✅ Report sent to: {email}</p>
          <a
            href={`http://localhost:8000/${pdfPath}`}
            target="_blank"
            rel="noreferrer"
            className="text-blue-500 underline font-medium"
            download
          >
            Download PDF
          </a>
        </>
      )}
    </div>
  );
};

export default DownloadCard;
