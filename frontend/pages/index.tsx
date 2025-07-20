import React, { useState } from "react";
import { useRouter } from "next/router";

const IndexPage = () => {
  const router = useRouter();
  const [companyName, setCompanyName] = useState("");
  const [persona, setPersona] = useState("CTO");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!companyName || !persona) {
      alert("Please enter all fields.");
      return;
    }

    // Simulate saving input or passing it via global context / API
    // Then redirect
    router.push("/success");
  };

  return (
    <div className="min-h-screen bg-gray-50 px-4 py-10 flex items-center justify-center">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-xl font-bold mb-4 text-center">🧠 BeaconAI Intake Form (Mock)</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block font-medium text-gray-700 mb-1">Company Name</label>
            <input
              type="text"
              placeholder="e.g., FinTech360"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className="border border-gray-300 px-4 py-2 w-full rounded"
              required
            />
          </div>

          <div>
            <label className="block font-medium text-gray-700 mb-1">Persona</label>
            <select
              value={persona}
              onChange={(e) => setPersona(e.target.value)}
              className="border border-gray-300 px-4 py-2 w-full rounded"
              required
            >
              <option value="CTO">CTO</option>
              <option value="CMO">CMO</option>
              <option value="CHRO">CHRO</option>
              <option value="COO">COO</option>
              <option value="CEO">CEO</option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700"
          >
            Submit and View Insights
          </button>
        </form>
      </div>
    </div>
  );
};

export default IndexPage;
