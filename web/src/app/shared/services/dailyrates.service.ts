import {Inject, Injectable} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from './data.service';
import { API_URLS } from '../config/app.url.config';


@Injectable()
export class DailyRateService extends DataService {

  constructor(@Inject(HttpClient) _http: HttpClient) {
    super(API_URLS.DAILY_RATES_URL, _http);
  }
}
