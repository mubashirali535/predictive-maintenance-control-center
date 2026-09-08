const WS_URL = "ws://127.0.0.1:8000/ws";

export function connectWebSocket({
  onMessage,
  onOpen,
  onClose,
  onError,
}) {
  const websocket = new WebSocket(WS_URL);

  websocket.onopen = () => {
    console.log("WebSocket connected");

    if (onOpen) {
      onOpen();
    }
  };

  websocket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      console.log("WebSocket data:", data);

      if (onMessage) {
        onMessage(data);
      }
    } catch (error) {
      console.error("Invalid WebSocket data:", error);
    }
  };

  websocket.onerror = (error) => {
    console.error("WebSocket error:", error);

    if (onError) {
      onError(error);
    }
  };

  websocket.onclose = () => {
    console.log("WebSocket disconnected");

    if (onClose) {
      onClose();
    }
  };

  return websocket;
}