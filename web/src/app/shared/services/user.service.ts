import { API_URLS } from './../config/app.url.config';
import { DataService } from './data.service';
import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class UserService extends DataService {
  constructor( @Inject(HttpClient) _http: HttpClient) {
    super(API_URLS.USER_URL, _http);
  }
}
