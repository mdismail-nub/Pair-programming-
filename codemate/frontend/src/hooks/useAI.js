import { useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function useAI() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const safeCall = async (fn) => {
    setLoading(true); setError("");
    try { return await fn(); } catch (e) { setError(e?.response?.data?.detail || e.message); throw e; } finally { setLoading(false); }
  };

  const explainCode = async (payload) => safeCall(async () => {
    const { data } = await axios.post(`${API}/ai/explain`, payload);
    setMessages((prev) => [...prev, { role: "ai", type: "explain", content: data.response, model: data.model_used }]);
    return data;
  });

  const reviewCode = async (payload) => safeCall(async () => {
    const { data } = await axios.post(`${API}/ai/review`, payload);
    const xml = `<praise>${data.praise}</praise><issues>${data.issues}</issues><suggestion>${data.suggestion}</suggestion><rating>${data.rating}</rating>`;
    setMessages((prev) => [...prev, { role: "ai", type: "review", content: xml, model: data.model_used }]);
    return data;
  });

  const getHint = async (payload) => safeCall(async () => {
    const { data } = await axios.post(`${API}/ai/hint`, payload);
    setMessages((prev) => [...prev, { role: "ai", type: "hint", content: data.hint, model: data.model_used }]);
    return data;
  });

  const sendMessage = async (text, language, context = "") => safeCall(async () => {
    const next = [...messages, { role: "user", content: text }];
    setMessages(next);
    const { data } = await axios.post(`${API}/ai/chat`, { messages: next.map(m => ({ role: m.role === 'ai' ? 'assistant' : m.role, content: m.content })), language, context });
    setMessages((prev) => [...prev, { role: "ai", content: data.response, model: "routed" }]);
  });

  return { messages, loading, error, explainCode, reviewCode, getHint, sendMessage, setMessages };
}
