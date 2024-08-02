import { CrudService } from './crud.service';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, catchError, of } from 'rxjs';
import { expand, toArray } from 'rxjs/operators';

export class DataService implements CrudService {

  // Set the content type for POST and PUT requests
  private readonly headers = { 'Content-Type': 'application/json' };

  // Constructor with dependencies injection
  constructor(private readonly url: string, private readonly http: HttpClient) {}

  fetchData(params?: any): Observable<any> {
    let queryParams = new HttpParams();
    if (params) {
      for (const key in params) {
        if (params.hasOwnProperty(key)) {
          queryParams = queryParams.set(key, params[key]);
        }
      }
    }
    return this.http.get<any>(this.url, { params: queryParams });


}


 listByPage(page: number=1): Observable<any> {
  return this.http.get<any>(`${this.url}?page=${page}`);
}
 listByUrl(url?: string): Observable<any> {
  if (url) {
    return this.http.get<any>(url)
  } else {
    return this.http.get<any>(`${this.url}`);
  }
  }


  // Method to retrieve all resources
  list(limit: number, offset: number): Observable<any[]> {
    // Create a new HttpParams object and set the 'page_size' parameter
    const params = new HttpParams().set('offset', limit.toString());
    return this.http.get<any[]>(this.url, { params}).pipe(
      catchError(error => {
        return of(error.resp);
      })
    );
  }
  listAll(): Observable<any[]> {
    return this.http.get<any[]>(this.url).pipe(
      catchError(error => {
        return of(error.resp);
      })
    );
  }
  // Method to retrieve a specific resource by ID
  get(id: any): Observable<any> {
    return this.http.get<any>(`${this.url}${id}`+'/');
  }

    // Method to retrieve a specific resource by ID
    getByName(name: string): Observable<any> {
      return this.http.get<any>(`${this.url}${name}`+'/');
    }

  // Method to create a new resource
  add(resource: any): Observable<any> {
    return this.http.post<any>(this.url, resource).pipe(
      catchError(error => {
        return of(error.resp);
      }));
  }

  // Method to update an existing resource
  update(resource: any): Observable<any> {
    return this.http.put<any>(this.url, resource);
  }

  // Method to delete an existing resource by ID
  remove(id: number): Observable<any> {
    return this.http.delete<any>(`${this.url}${id}`);
  }

  // Method to create multiple resources at once
  addMany(resources: any[]): Observable<any[]> {
    return this.http.post<any[]>(`${this.url}`, resources);
  }
}

