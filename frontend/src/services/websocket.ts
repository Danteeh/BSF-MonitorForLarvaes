type TelemetryListener = (event: any) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private listeners: Set<TelemetryListener> = new Set();
  private statusListeners: Set<(connected: boolean) => void> = new Set();
  private reconnectInterval: number = 3000;
  private isIntentionalClose: boolean = false;

  constructor() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    this.url = `${protocol}//${host}/ws/telemetry`;
  }

  public connect() {
    this.isIntentionalClose = false;
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.notifyStatus(true);
      };

      this.ws.onclose = () => {
        this.notifyStatus(false);
        if (!this.isIntentionalClose) {
          setTimeout(() => this.connect(), this.reconnectInterval);
        }
      };

      this.ws.onerror = () => {
        this.notifyStatus(false);
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.listeners.forEach((listener) => listener(data));
        } catch (e) {
          console.error('Error parsing WebSocket frame:', e);
        }
      };
    } catch (e) {
      this.notifyStatus(false);
      setTimeout(() => this.connect(), this.reconnectInterval);
    }
  }

  public subscribe(listener: TelemetryListener) {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  public onStatusChange(callback: (connected: boolean) => void) {
    this.statusListeners.add(callback);
    callback(this.isConnected());
    return () => {
      this.statusListeners.delete(callback);
    };
  }

  public isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  public disconnect() {
    this.isIntentionalClose = true;
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  private notifyStatus(status: boolean) {
    this.statusListeners.forEach((cb) => cb(status));
  }
}

export const wsClient = new WebSocketClient();
