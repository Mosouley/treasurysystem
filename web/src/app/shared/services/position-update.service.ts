import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { API_URLS } from '../config/app.url.config';
import { DataService } from './data.service';

@Injectable({
  providedIn: 'root'
})
export class PositionUpdateService extends DataService {

  constructor(@Inject(HttpClient) _http: HttpClient) {
    super(API_URLS.POSITIONS_UPDATE_URL, _http);
}
}
