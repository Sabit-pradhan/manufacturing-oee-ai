"use client";

import { useState } from "react";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

interface Source {
  document_name: string;
  chunk_index: number;
  similarity: number;
}

interface Message {
  question: string;
  answer: string;
  sources?: Source[];
}

const sampleQuestions = [
  "What are the important limitations of the manufacturing dataset?",
  "Explain how OEE is calculated.",
  "What does low availability mean?",
];

export default function CopilotChat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askCopilot(value?: string) {
    const currentQuestion = (value ?? question).trim();

    if (!currentQuestion || loading) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/copilot/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: currentQuestion,
            top_k: 3,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data: Message = await response.json();

      setMessages((previous) => [...previous, data]);
      setQuestion("");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mt-6 rounded-xl border border-cyan-900/60 bg-slate-950 p-5 shadow-lg">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-cyan-400">
            Manufacturing AI Copilot
          </h2>
          <p className="mt-1 text-xs text-slate-400">
            Ask questions about manufacturing documentation and dataset insights.
          </p>
        </div>

        <span className="rounded-full border border-emerald-700/50 bg-emerald-950/40 px-3 py-1 text-xs text-emerald-400">
          AI ASSISTANT
        </span>
      </div>

      <div className="mb-4 flex flex-wrap gap-2">
        {sampleQuestions.map((item) => (
          <button
            key={item}
            onClick={() => askCopilot(item)}
            disabled={loading}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-left text-xs text-slate-300 transition hover:border-cyan-500 hover:text-cyan-400 disabled:opacity-50"
          >
            {item}
          </button>
        ))}
      </div>

      <div className="mb-4 max-h-[450px] min-h-[120px] space-y-4 overflow-y-auto rounded-lg border border-slate-800 bg-slate-900/60 p-4">
        {messages.length === 0 && (
          <p className="py-8 text-center text-sm text-slate-500">
            Ask your first manufacturing question to get started.
          </p>
        )}

        {messages.map((message, index) => (
          <div key={index} className="space-y-3">
            <div className="ml-auto max-w-[90%] rounded-lg border border-cyan-800/50 bg-cyan-950/40 p-3">
              <p className="mb-1 text-xs font-semibold text-cyan-400">
                YOU
              </p>
              <p className="text-sm text-slate-200">
                {message.question}
              </p>
            </div>

            <div className="max-w-[95%] rounded-lg border border-slate-700 bg-slate-800/70 p-3">
              <p className="mb-2 text-xs font-semibold text-emerald-400">
                AI COPILOT
              </p>
              <p className="whitespace-pre-wrap text-sm leading-6 text-slate-200">
                {message.answer}
              </p>

              {message.sources && message.sources.length > 0 && (
                <div className="mt-4 border-t border-slate-700 pt-3">
                  <p className="mb-2 text-xs font-semibold text-slate-400">
                    RETRIEVED SOURCES
                  </p>

                  {message.sources.map((source, sourceIndex) => (
                    <div
                      key={sourceIndex}
                      className="mb-2 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-400"
                    >
                      <span>
                        {source.document_name} · Chunk {source.chunk_index}
                      </span>
                      <span>
                        Similarity:{" "}
                        {(source.similarity * 100).toFixed(1)}%
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <p className="animate-pulse text-sm text-cyan-400">
            Copilot is analyzing your question...
          </p>
        )}
      </div>

      {error && (
        <p className="mb-3 rounded-lg border border-red-800/50 bg-red-950/30 p-3 text-sm text-red-400">
          {error}
        </p>
      )}

      <form
        onSubmit={(event) => {
          event.preventDefault();
          askCopilot();
        }}
        className="flex flex-col gap-3 sm:flex-row"
      >
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask about OEE, machines, production, or dataset..."
          disabled={loading}
          className="min-w-0 flex-1 rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-cyan-500"
        />

        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="rounded-lg bg-cyan-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Ask Copilot"}
        </button>
      </form>
    </section>
  );
}