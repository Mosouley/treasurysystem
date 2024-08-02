import {Inject, Injectable} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from './data.service';
import { API_URLS } from '../config/app.url.config';


@Injectable()
export class CurrenciesService extends DataService {

  constructor(private _http: HttpClient) {
    super(API_URLS.CURRENCIES_URL, _http);
  }
}
