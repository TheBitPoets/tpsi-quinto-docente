import { useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);
  const doubled = count * 2;

  return (
    <main>
      <h1>React translation microscope</h1>
      <p>count: {count}</p>
      <p>doubled: {doubled}</p>
      <button
        type="button"
        onClick={() => setCount((value) => value + 1)}
      >
        +1
      </button>
    </main>
  );
}
