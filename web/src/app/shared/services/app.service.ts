import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { Store } from '@ngrx/store';

import { API_URLS } from '../config/app.url.config';
import { PrincipalState } from '../shared/model/principal.state';
import { SAVE_PRINCIPAL } from '../shared/model/save.principal.action';


@Injectable()
export class AppService {

  authenticated = false;

  constructor(private http: HttpClient,
      private cookieService: CookieService,
      private store: Store<PrincipalState>) { }

  authenticate(credentials, callback) {
    if (credentials) {
      const token = btoa(credentials.username + ':' + credentials.password);
      this.cookieService.set('token', token);

      this.http.get(API_URLS.SINGNING_URL).subscribe(response => {
          if (response && response['name']) {
            console.log(response);
              this.authenticated = true;
              this.store.dispatch({
                type: SAVE_PRINCIPAL,
                payload: response
              });

          } else {
              this.authenticated = false;
          }
          return callback && callback();
      });
    } else {
      this.authenticated = false;
    }
  }

  logout(callback) {
    return callback && callback();
  }

}
