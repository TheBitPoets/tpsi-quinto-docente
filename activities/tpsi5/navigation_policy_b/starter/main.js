import process from "node:process";

export function decideNavigation(input) {
  // TODO: implementa la state machine descritta nella consegna.
  return { action: "allow" };
}

const raw = await new Promise((resolve) => {
  let data = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (chunk) => { data += chunk; });
  process.stdin.on("end", () => resolve(data));
});

const input = JSON.parse(raw);
process.stdout.write(JSON.stringify(decideNavigation(input)));
