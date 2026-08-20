import { EventEmitter } from "node:events";

export function createPostEvents() {
  const emitter = new EventEmitter();

  return {
    publish(event) {
      emitter.emit("post-event", event);
    },

    subscribe(listener) {
      emitter.on("post-event", listener);
      return () => emitter.off("post-event", listener);
    },
  };
}
