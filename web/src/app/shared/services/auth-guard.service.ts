import { State } from './../reducers/index';
import { AuthService } from './../auth/auth.service';
import { Injectable } from '@angular/core';
import { Router, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard  {
  constructor(private router: Router,
    private authService: AuthService) { }

  canActivateChild(next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> | Promise<boolean> | boolean {

    // const allowedRoles = next.data.allowedRoles;
    const isAuthorized = this.authService.isAdmin();

    if (!isAuthorized) {
      console.log(state.url);

      // this.router.navigate(['/access-denied']);
    }

    return isAuthorized;
  }


  canActivate(route, state: RouterStateSnapshot) {

    // tslint:disable-next-line:curly
    if (this.authService.isAdmin()) return true;
    this.router.navigate(
      ['/dashboard'], {
        queryParams: {
          returnUrl: state.url
        }
      });
      return false;
  }
  // canActivate(
  //   next: ActivatedRouteSnapshot,
  //   state: RouterStateSnapshot
  // ): Observable<boolean> | Promise<boolean> | boolean {
  //   const allowedRoles = next.data.allowedRoles;
  //   const isAuthorized = this.authService.isAuthorized(allowedRoles);

  //   if (!isAuthorized) {
  //     this.router.navigate(['accessdenied']);
  //   }
  //   this.router.navigate(['/dashboard']);
  //   return isAuthorized;
  // }

}

