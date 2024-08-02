import {Inject, Injectable} from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Observable} from 'rxjs';
import { DataService } from './data.service';
import { API_URLS } from '../config/app.url.config';


@Injectable()
export class CustomerService extends DataService {

  constructor(@Inject(HttpClient) _http: HttpClient) {
    super(API_URLS.CUSTOMERS_URL, _http);
  }
}
