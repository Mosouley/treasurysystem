import { Inject, Injectable } from '@angular/core';
import { DataService } from './data.service';
import { HttpClient } from '@angular/common/http';
import { API_URLS } from '../config/app.url.config';

@Injectable({
  providedIn: 'root'
})
export class MetadataService extends DataService{

  constructor(@Inject(HttpClient) private _http: HttpClient) {
    super(API_URLS.MODEL_METADATA_ALL, _http);
  }
}
