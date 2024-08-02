import { Inject, Injectable, Input } from '@angular/core';
import { DataService } from './data.service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class GenericService<T>  {
  constructor(private http: HttpClient) {}

  getAll(apiUrl: string): Observable<T[]> {
    return this.http.get<T[]>(apiUrl);
  }

  get(apiUrl: string, id: number): Observable<T> {
    return this.http.get<T>(`${apiUrl}${id}/`);
  }

  create(apiUrl: string, data: T): Observable<T> {
    return this.http.post<T>(apiUrl, data);
  }

  update(apiUrl: string, id: number, data: T): Observable<T> {
    return this.http.put<T>(`${apiUrl}${id}/`, data);
  }

  delete(apiUrl: string, id: number): Observable<void> {
    return this.http.delete<void>(`${apiUrl}${id}/`);
  }
}
