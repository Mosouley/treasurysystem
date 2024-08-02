import { Injectable } from "@angular/core";
import { Observable, ReplaySubject, retry } from "rxjs";
import { WebSocketSubject } from "rxjs/webSocket";
import { webSocketMessage } from "../../model/webSocketMessage";



@Injectable()
export class WebsocketService {

  private socket$!: WebSocketSubject<webSocketMessage>;

  public status: ReplaySubject<boolean> = new ReplaySubject<boolean>(1);

  connect(url: string): WebSocketSubject<webSocketMessage> {
    if (!this.socket$ || this.socket$.closed) {
      this.socket$ = new WebSocketSubject(url);
       // Add reconnection logic using retryWhen
       this.socket$.pipe(
        retry(2000)
      )
      .subscribe({
        next: () => this.status.next(true),
        error: (e: any) => {
          console.error('WebSocket reconnection error:', e)
          this.status.next(false)},
          complete:() => console.log('complete')

    })
  }
  return  this.socket$
}
  getMessages(): Observable<any> {
    // Return the observable to listen for messages
    return this.socket$.asObservable();
  }
  disconnect(): void {
    if (this.socket$ && !this.socket$.closed) {
      this.socket$.complete();
      this.status.next(false); // Connection is closed
    }
  }

}
