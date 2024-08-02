import { TokenStorageService } from './../auth/token-storage.service';
import { AuthService } from './../auth/auth.service';
import { Router } from '@angular/router';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AdminAuthGuard  {

  constructor(
    private router: Router,
    private tokenService: TokenStorageService
  ) { }

  canActivate() {
   const roles = this.tokenService.getAuthorities();
   // tslint:disable-next-line:curly
   if (roles.includes('ROLE_ADMIN')) return true;
    this.router.navigate(['']);
    return false;
  }
}
