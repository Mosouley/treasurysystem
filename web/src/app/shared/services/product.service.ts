import {Inject, Injectable} from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Observable} from 'rxjs';
import { DataService } from './data.service';
import { API_URLS } from '../config/app.url.config';



@Injectable()
export class ProductService extends DataService {

  constructor( @Inject(HttpClient) private _http: HttpClient) {
    super(API_URLS.PRODUCTS_URL, _http);
  }
  getProductsByCode(code: string): Observable<any> {
    return this._http.get(API_URLS.PRODUCTS_URL + `/by/${code}`);


  }
}
