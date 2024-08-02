import { MaterialModule } from './../../material/material.module';
import { SharedModule } from './../../shared/shared.module';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { LogoutComponent } from './../logout/logout.component';
import { UserLoginComponent } from './../user-login/user-login.component';
import { Component, OnInit, Output, EventEmitter, Inject } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { Subscription } from 'rxjs';
import { MenuNode } from './menu-node';
import { CommonModule } from '@angular/common';
import { NavItem1Component } from './nav-item1/nav-item1.component';
import { NavItem2Component } from './nav-item2/nav-item2.component';
import { NavLoginComponent } from './nav-login/nav-login.component';





@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  standalone: true,
  imports: [
    CommonModule,
    MaterialModule,
    NavItem1Component,
    NavItem2Component,
    NavLoginComponent,
    RouterModule
  ],
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit  {
    isSidebarOpen = false;
    routeQueryParams$: Subscription | undefined;

    username!: string;
    password!: string;
    remember = false;

    @Output() toggleSideNav: EventEmitter<boolean> = new EventEmitter<boolean>();

    links: MenuNode[] = [
      {
        name: 'User',
        url: 'home/login',
        icon: 'speed',
        action: false,
        expandable: true,
        children: [
          {
            name: 'Login',
            url: 'home/login',
            icon: 'category',
            action: false,
            expandable: true
          },
          {
            name: 'Register',
            url: 'profile',
            icon: 'category',
            action: false,
            expandable: true,
          }
        ]
      }



    ];

    constructor(
      public dialog: MatDialog,

    ) {

    }

    ngOnInit(): void {
      this.isSidebarOpen = false;
    }
    loginOpen() {

      let dialogConfig = new MatDialogConfig();
      // dialogConfig.disableClose = false;
      dialogConfig = {
        height: '450px',
        width: '600px',
        data:  {
          username: this.username,
          password: this.password,
          remember: this.remember
        }};
      //  dialogConfig.autoFocus = true;
       let dialogRef = this.dialog.open(UserLoginComponent, dialogConfig);

       dialogRef.afterClosed().subscribe( result => {

        this.username = result.username
        this.password = result.password
        this.remember = result.remember
        console.log( 'User connected with ' + this.username + ' --- ' + this.password + ' + . ' + this.remember) ;

        // router.navigate(['.'], {relativeTo: this.route})
       });
    }

    dialogLogout() {
      let dialogConfig = new MatDialogConfig();
      // dialogConfig.disableClose = false;
      dialogConfig = {
        height: '600px',
        width: '500px',

      }
      dialogConfig.autoFocus = true;
      this.dialog.open(LogoutComponent, dialogConfig);

    }

    ngOnDestroy(): void {
      this.routeQueryParams$?.unsubscribe();
    }
}
