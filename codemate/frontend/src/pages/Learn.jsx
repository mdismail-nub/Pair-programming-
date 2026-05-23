import { useState } from "react";
import axios from "axios";
import Editor from "../components/Editor";
import ChatPanel from "../components/ChatPanel";
import LanguageSelector from "../components/LanguageSelector";
import useAI from "../hooks/useAI";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Learn(){
  const [language,setLanguage]=useState("python");
  const [code,setCode]=useState("print('Hello CodeMate')");
  const [output,setOutput]=useState("");
  const {messages,loading,error,explainCode,reviewCode,getHint,sendMessage}=useAI();

  const runCode=async()=>{try{const {data}=await axios.post(`${API}/challenges/run`,{code,language});setOutput(data.output||data.error);}catch(e){setOutput(e.message)}};

  return <div className='h-screen bg-bg text-textPrimary flex flex-col'><div className='p-3 border-b border-borderc flex gap-2 items-center'><LanguageSelector value={language} onChange={setLanguage}/><button onClick={()=>reviewCode({code,language})} className='bg-accent px-3 py-1 rounded text-black'>Review My Code</button><button onClick={runCode} className='bg-accent2 text-black px-3 py-1 rounded'>Run Code</button><button onClick={()=>getHint({code,problem:'Help me solve this',language})} className='bg-surface border border-borderc px-3 py-1 rounded'>Get Hint</button></div><div className='flex-1 flex flex-col md:flex-row'><div className='md:w-3/5 h-1/2 md:h-full flex flex-col'><div className='flex-1'><Editor language={language} value={code} onChange={setCode} onExplainSelection={(s)=>explainCode({code:s,question:'Explain selected code',language})}/></div><div className='h-32 border-t border-borderc p-2 overflow-auto text-sm'><strong>Output:</strong><pre>{output}</pre>{error&&<p className='text-red-400'>{error}</p>}</div></div><div className='md:w-2/5 h-1/2 md:h-full border-l border-borderc p-3'><ChatPanel messages={messages} loading={loading} onSend={(t)=>sendMessage(t,language,code)} language={language}/></div></div></div>
}
