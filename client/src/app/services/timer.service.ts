// src/app/services/timer.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TimerService {
  private apiUrl = environment.apiUrl;
  private wsUrl = environment.wsUrl;
  private sockets: { [key: number]: WebSocket } = {}; // Store WebSocket connections per timer

  constructor(private http: HttpClient) {}

  /** Fetch all available timers from the backend */
  getTimers() {
    return this.http.get(`${this.apiUrl}/timers/`);
  }

  /** Create a new timer event */
  createTimer(eventData: { event_name: string; hours: number; minutes: number; seconds: number }) {
    return this.http.post(`${this.apiUrl}/timers/`, eventData);
  }

  /** Open a WebSocket connection for a specific timer */
  openWebSocket(timerId: number, onMessage: (data: any) => void) {
    // If WebSocket already exists, do nothing
    if (this.sockets[timerId]) return;

    const socket = new WebSocket(`${this.wsUrl}/timer/${timerId}/`);
    this.sockets[timerId] = socket;

    socket.onopen = () => {
      console.log(`✅ WebSocket connected for Timer ${timerId}`);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'timer_update') {
        onMessage({
          remaining_time: data.remaining_time,
          is_running: data.is_running
        });
      }
    };

    socket.onerror = (error) => {
      console.error(`❌ WebSocket error for Timer ${timerId}:`, error);
    };

    socket.onclose = () => {
      console.log(`🔴 WebSocket closed for Timer ${timerId}`);
      delete this.sockets[timerId]; // Remove closed WebSocket from storage
    };
  }

  /** Send a WebSocket command to the backend */
  sendCommand(timerId: number, command: string, payload: any = {}) {
    const socket = this.sockets[timerId];

    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ command, ...payload }));
    } else {
      console.warn(`⚠️ WebSocket for Timer ${timerId} is not connected.`);
    }
  }
}
