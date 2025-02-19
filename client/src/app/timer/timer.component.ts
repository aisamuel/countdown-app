// src/app/timer/timer.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon'; 
import { TimerService } from '../services/timer.service';

@Component({
  selector: 'app-timer',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule
  ],
  templateUrl: './timer.component.html',
  styleUrls: ['./timer.component.css']
})
export class TimerComponent implements OnInit {
  timers: any[] = [];
  newEventName: string = '';
  newEventHours: number = 0;
  newEventMinutes: number = 0;
  newEventSeconds: number = 0;

  constructor(private timerService: TimerService) {}

  ngOnInit(): void {
    this.loadTimers();
  }

  /** Fetch all timers from the backend */
  loadTimers() {
    this.timerService.getTimers().subscribe((data: any) => {
      this.timers = data.map((timer: any) => ({
        ...timer,
        isRunning: false,
        remainingSeconds: timer.total_seconds
      }));

      // Open WebSocket for each timer
      this.timers.forEach((timer) => {
        this.timerService.openWebSocket(timer.id, (data) => {
          timer.remainingSeconds = data.remaining_time;
          timer.isRunning = data.is_running; // Ensure isRunning is updated correctly
        });
      });
    });
  }

  /** Create a new event with a timer */
  createEvent() {
    if (!this.newEventName.trim()) {
      alert('Please enter an event name.');
      return;
    }

    this.timerService.createTimer({
      event_name: this.newEventName,
      hours: this.newEventHours,
      minutes: this.newEventMinutes,
      seconds: this.newEventSeconds
    }).subscribe((newTimer: any) => {
      this.timers.push({
        ...newTimer,
        isRunning: false,
        remainingSeconds: newTimer.total_seconds
      });

      // Open WebSocket for the new timer
      this.timerService.openWebSocket(newTimer.id, (data) => {
        newTimer.remainingSeconds = data.remaining_time;
        newTimer.isRunning = data.is_running;
      });

      // Reset form inputs
      this.newEventName = '';
      this.newEventHours = 0;
      this.newEventMinutes = 0;
      this.newEventSeconds = 0;
    });
  }

  /** Set time for an event */
  setTime(timer: any) {
    this.timerService.sendCommand(timer.id, 'set_time', {
      hours: timer.hours,
      minutes: timer.minutes,
      seconds: timer.seconds
    });
  }

  /** Start or Pause timer */
  toggleStartPause(timer: any) {
    this.timerService.sendCommand(timer.id, 'start_pause');
  }

  /** Reset the timer */
  resetTimer(timer: any) {
    this.timerService.sendCommand(timer.id, 'reset');
  }

  /** Format time display */
  formattedTime(timer: any) {
    const hrs = Math.floor(timer.remainingSeconds / 3600);
    const mins = Math.floor((timer.remainingSeconds % 3600) / 60);
    const secs = timer.remainingSeconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
}
