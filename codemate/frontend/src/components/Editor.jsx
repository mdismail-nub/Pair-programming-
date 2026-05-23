import MonacoEditor from "@monaco-editor/react";
import { useState } from "react";

export default function Editor({ language, value, onChange, onExplainSelection }) {
  const [selection, setSelection] = useState("");
  return (
    <div className="relative h-full">
      <MonacoEditor
        height="100%"
        language={language === "c++" ? "cpp" : language}
        value={value}
        theme="vs-dark"
        onChange={(v) => onChange(v || "")}
        options={{ fontSize: 14, minimap: { enabled: false }, wordWrap: "on", lineNumbers: "on", quickSuggestions: true }}
        onMount={(editor) => {
          editor.onDidChangeCursorSelection((e) => setSelection(editor.getModel().getValueInRange(e.selection)));
        }}
      />
      {selection && (
        <button className="absolute top-3 right-3 bg-accent text-black px-3 py-1 rounded" onClick={() => onExplainSelection(selection)}>
          Explain This
        </button>
      )}
    </div>
  );
}
