import { delay, retryWhen, takeUntil } from 'rxjs';
import { WebSocketSubject, webSocket } from 'rxjs/webSocket';
import { Injectable } from '@angular/core';
import { catchError, tap, Observable } from 'rxjs';
import { Subject, EMPTY } from 'rxjs';
import { API_URLS, RECONNECT_INTERVAL } from '../config/app.url.config';

export const WS_ENDPOINT = API_URLS.WEBSOCKETS_TRADEFLOWS;

@Injectable({
  providedIn: 'root'
})
export class StreamService {
  private socket$!: WebSocketSubject<any>;
  private messagesSubject$ = new Subject<any>();
  public messages$: Observable<any> = this.messagesSubject$.asObservable(); // Use asObservable() to expose it as Observable
  private closeSignal$ = new Subject<void>();
  public connect(): void {
    if (!this.socket$ || this.socket$.closed) {
      this.socket$ = this.getNewWebSocket();

      // You may also want to handle errors and completion of the socket$
      this.socket$.pipe(
        catchError(error => {
          console.error('WebSocket error:', error);
          return EMPTY; // Return EMPTY observable to continue the stream
        }),
        retryWhen(errors => errors.pipe(
          tap(() => console.log('WebSocket connection lost. Reconnecting...')
          ),
          delay(RECONNECT_INTERVAL),
          takeUntil(this.closeSignal$)
        ))
      ).subscribe(
        (message) => {
          // No need to use switchAll, just pass the WebSocket observable directly
          this.messagesSubject$.next(message);
      },
      () => console.log('WebSocket disconnected'),
        () => console.log('WebSocket connection completed')
      );
    }
  }

  private getNewWebSocket(): WebSocketSubject<any> {
    return webSocket(WS_ENDPOINT);
  }

  sendMessage(msg: any): void {
    this.socket$?.next(msg);
  }

  close(): void {
    this.closeSignal$.next(); // Emit signal to stop reconnection attempts
    this.socket$?.complete();
  }
}
