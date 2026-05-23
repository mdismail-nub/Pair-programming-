const tag = (text, t) => (text.match(new RegExp(`<${t}>([\\s\\S]*?)</${t}>`)) || ["", ""])[1];

export default function ChatPanel({ messages, loading, onSend, language }) {
  const renderAI = (m, i) => {
    const praise = tag(m.content, "praise");
    if (praise) {
      const rating = tag(m.content, "rating");
      return <div key={i} className="bg-surface p-3 rounded border border-borderc space-y-2"><div className="bg-green-900/30 p-2 rounded">{praise}</div><div className="bg-red-900/30 p-2 rounded">{tag(m.content,"issues")}</div><div className="bg-blue-900/30 p-2 rounded">{tag(m.content,"suggestion")}</div><span className="text-xs px-2 py-1 rounded bg-gray-700">{rating}</span><p className="text-xs text-textSecondary">Model: {m.model}</p></div>;
    }
    return <div key={i} className="bg-surface p-3 rounded border border-borderc whitespace-pre-wrap">{m.content}<p className="text-xs text-textSecondary mt-2">Model: {m.model}</p></div>;
  };

  return <div className="h-full flex flex-col"><div className="text-sm mb-2">Language: <span className="bg-accent2/20 px-2 py-1 rounded">{language}</span></div><div className="flex-1 overflow-auto space-y-2">{messages.map((m,i)=>m.role==='ai'?renderAI(m,i):<div key={i} className="bg-accent2/20 p-3 rounded">{m.content}</div>)}{loading && <div className="animate-pulse bg-surface h-16 rounded"/>}</div><form className="mt-2 flex gap-2" onSubmit={(e)=>{e.preventDefault(); const val=e.target.msg.value.trim(); if(!val) return; onSend(val); e.target.reset();}}><input name="msg" className="flex-1 bg-surface border border-borderc rounded p-2" placeholder="Ask CodeMate..."/><button className="bg-accent px-3 rounded text-black">Send</button></form></div>;
}
