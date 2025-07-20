import React, { useState } from "react";
import DownloadCard from "../components/DownloadCard";

const SuccessPage = () => {
  // This would normally come from a backend response or local state/context
  const [persona] = useState("CTO");
  const [companyName] = useState("FinTech360");
  const [insights] = useState({
    C1: "Your leadership is somewhat confident in AI direction, but alignment is still fragmented.",
    A2: "You have informal tool adoption but lack centralized guidance or governance.",
    R1: "AI literacy levels vary across departments, and no formal training exists yet.",
    E4: "You currently don’t have a roadmap for scaling AI company-wide."
  });

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-8 flex flex-col items-center">
      <div className="max-w-2xl w-full bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold mb-4 text-center text-green-600">🎉 Submission Successful!</h1>
        <p className="text-center mb-6 text-gray-700">
          Based on your answers, we’ve generated personalized AI readiness insights for {companyName}.
        </p>

        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-2 text-blue-700">🔍 Preview of Your Strategic Insights</h2>
          <ul className="list-disc ml-6 space-y-2 text-gray-800">
            {Object.entries(insights).map(([qid, insight]) => (
              <li key={qid}>
                <strong>{qid}</strong>: {insight}
              </li>
            ))}
          </ul>
        </div>

        <DownloadCard
          persona={persona}
          companyName={companyName}
          insights={insights}
        />
      </div>
    </div>
  );
};

export default SuccessPage;
