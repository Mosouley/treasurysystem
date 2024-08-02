import {Inject, Injectable} from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Observable} from 'rxjs';
import { DataService } from './data.service';
import { API_URLS } from '../config/app.url.config';


@Injectable()
export class TradeService extends DataService {

  constructor(@Inject(HttpClient) private _http: HttpClient) {
    super(API_URLS.TRADES_URL, _http);
  }
  addTransactionLine(trade_id: number, trade: any): Observable<any> {
    // JSON.stringify(transax);
    return this._http.post(API_URLS.TRADES_URL + `/${trade_id}` + `/trades`, trade);
  }
}
