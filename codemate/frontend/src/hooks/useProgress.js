import { useEffect, useState } from "react";

const KEY = "codemate_progress";

const initial = { completedChallenges: [], points: 0, streak: 1, weakAreas: ["loops", "recursion"], activity: [] };

export default function useProgress() {
  const [progress, setProgress] = useState(initial);

  useEffect(() => {
    const raw = localStorage.getItem(KEY);
    if (raw) setProgress(JSON.parse(raw));
  }, []);

  const persist = (next) => { setProgress(next); localStorage.setItem(KEY, JSON.stringify(next)); };

  const markComplete = (id) => {
    if (progress.completedChallenges.includes(id)) return;
    persist({ ...progress, completedChallenges: [...progress.completedChallenges, id], activity: [`Completed ${id}`, ...progress.activity].slice(0, 10) });
  };

  const addPoints = (pts) => persist({ ...progress, points: progress.points + pts });
  const updateWeakAreas = (areas) => persist({ ...progress, weakAreas: areas });

  return { ...progress, markComplete, addPoints, updateWeakAreas };
}
